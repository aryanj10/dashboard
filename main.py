from flask import Flask, session, redirect, url_for, request, render_template
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import io
from dash.exceptions import PreventUpdate
import base64
from plotly.subplots import make_subplots
import re
import dash_table
from dash.dash_table.Format import Format, Group, Scheme
from scipy.stats import zscore
import dash_bootstrap_components as dbc
from dashboard_utils import ( plot_comparison_by_period,plot_comparison_by_period_multi,
     percentage_plot, percentage_plot_multi, convert_to_weekly,aum_rgm, return_table, extract_data_zscore,
    extract_data_zscore_store,get_cell_style, update_period_comparison_graph
)
from common_util import calculate_totals_per_period, extract_all_line_items, preprocess_comparison_data, convert_to_weekly

from views_code import KPISection, MainChart, AreaSelector, StoreSelector, Header

from summary_page import  get_top5_tables, plot_net_revenue_ebitda, create_waterfall_chart

from revenue_page_utils import important_metrics

# ---------- Styles ----------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "56px",
    "left": 0,
    "bottom": 0,
    "width": "250px",
    "padding": "1rem",
    "backgroundColor": "#f8f9fa",
    "zIndex": 1000,
    "transition": "margin-left .3s",
    "overflowY": "auto"
}

SIDEBAR_HIDDEN_STYLE = SIDEBAR_STYLE.copy()
SIDEBAR_HIDDEN_STYLE["marginLeft"] = "-250px"

CONTENT_STYLE = {
    "marginTop": "35px",
    "marginLeft": "250px",
    "marginRight": "1rem",
    "padding": "2rem",
    "transition": "margin-left .3s"
}

CONTENT_EXPANDED_STYLE = CONTENT_STYLE.copy()
CONTENT_EXPANDED_STYLE["marginLeft"] = "0"


# Initialize the app
# Load your data
with open('Data/all_store_data_enriched.json', 'r') as f:
    all_store_data = json.load(f)

with open('Data/all_store_data_region.json', 'r') as f:
    all_store_data_region = json.load(f)

ps = [key for key in all_store_data['Store_1000'].keys() if key != 'metadata' and not key.endswith("B")]


def PeriodSelector(periods, default_period=ps[-1]):
    return dcc.Dropdown(
        id='period-dropdown',
        options=[{'label': period, 'value': period} for period in ps[::-1]],
        value=default_period,
        placeholder='Select Period',
        style={'width': '205px', 'margin-bottom': '20px'}
    )
def RegionSelector(region, default_region=None):
    return dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in all_store_data_region.keys()],
        value=None,
        placeholder='Select Region',
        style={'width': '205px', 'margin-bottom': '20px'}
    )




server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.LUX])


@app.callback(
    [Output('area-coach-dropdown', 'options'),
     Output('area-coach-dropdown', 'value'),
     Output('store-dropdown', 'options'),
     Output('store-dropdown', 'value')],
    [Input('region-dropdown', 'value'),
     Input('area-coach-dropdown', 'value')]
)
def update_area_coach_and_store_dropdown(selected_region, selected_area_coach):
    if not selected_region:
        return [], None, [], None
    area_coaches = list(all_store_data_region[selected_region].keys())
    if selected_area_coach:
        stores = list(all_store_data_region[selected_region][selected_area_coach].keys())
    else:
        stores = []
    return ([{'label': coach, 'value': coach} for coach in area_coaches], selected_area_coach,
            [{'label': store, 'value': store} for store in stores], None)



app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # enables page-based routing
    # Navbar
    dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Button("\u2630", outline=True, color="primary", id="sidebar-toggle", className="me-2", size="sm")),
                dbc.Col(html.H4("QSR DASHBOARD", className="text-dark mb-0"), style={"paddingTop": "5px"})
            ], align="center", className="g-0", style={"width": "100%"})
        ]),
        color="light",
        dark=False,
        fixed="top",
        style={"height": "56px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}
    ),

    # Sidebar
    html.Div([

        html.H5("Navigation"),
        dcc.Link("Summary View", href="/", style={"display": "block", "margin-bottom": "10px"}),
        dcc.Link("Revenue", href="/revenue-graphs", style={"display": "block", "margin-bottom": "10px"}),
        dcc.Link("Cost of Sales", href="/cost-graphs", style={"display": "block", "margin-bottom": "10px"}),
        html.Hr(),

        html.H5("Filters"),
        
        html.Label("Select Period"),
        PeriodSelector(ps, ps[-1]),
        html.Label("Select Region"),
        RegionSelector(all_store_data_region.keys(), 'All'),
        html.Label("Select Area Coach"),
        AreaSelector('All'),
        html.Label("Select Store"),
        StoreSelector('All'),
        
    ], id="sidebar", style=SIDEBAR_HIDDEN_STYLE),

    # Content
    html.Div([
        Header(),
        html.Div(id='current-selections'),
        html.Div(id='kpi-container'),
        html.Div(id='chart-container2'),
        html.Div(id='chart-container'),
        html.Div(id='top5-container'),
    ], id="page-content", style=CONTENT_EXPANDED_STYLE)
])


# ------------- Callbacks -------------




@app.callback([
    Output('kpi-container', 'children'),
    Output('chart-container', 'children'),
    Output('chart-container2', 'children'),
    Output('top5-container', 'children')
], [
    Input('period-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('area-coach-dropdown', 'value'),
    Input('store-dropdown', 'value')
])

def update_dashboard(period, region, area_coach, store):
    if not period:
        raise dash.exceptions.PreventUpdate

    prev_period = f"{period.split('-')[0]}-{int(period.split('-')[1])-1:02d}"

    if not region and not area_coach and not store:
        data_type = 'All'
        data = all_store_data
        totals = calculate_totals_per_period(data, 'All', 'All')
        store_data = extract_all_line_items(data, period, data_type="All")

    elif store:
        data_type = 'Store'
        data = all_store_data_region[region][area_coach][store]
        totals = calculate_totals_per_period(data, 'Store', 'All')
        store_data = extract_all_line_items(all_store_data_region[region][area_coach], period, data_type="All")
    elif area_coach:
        data_type = 'All'
        data = all_store_data_region[region][area_coach]
        totals = calculate_totals_per_period(data, 'All', 'All')
        store_data = extract_all_line_items(data, period, data_type="All")
    else:
        data_type = 'Region'
        data = all_store_data_region[region]
        totals = calculate_totals_per_period(data, 'Region', 'All')
        store_data = extract_all_line_items(data, period, data_type="Region")
    #totals = calculate_totals_per_period(all_store_data, 'All', 'All')
    df = pd.DataFrame.from_dict(store_data, orient='index')
    current = totals.get(period, {})
    previous = totals.get(prev_period, {})

    # Extract metrics
    revenue = current.get("Net Revenue", 0)
    revenue_prev = previous.get("Net Revenue", 0)

    cogs = current.get("Total Cost of Sales", 0)
    cogs_prev = previous.get("Total Cost of Sales", 0)

    ebitda = current.get("EBITDA", 0)
    ebitda_prev = previous.get("EBITDA", 0)
    
    # KPI and Chart
    kpi_section = KPISection(cogs, cogs_prev, revenue, revenue_prev, ebitda, ebitda_prev)
    #store_data = extract_all_line_items(all_store_data, period, data_type="All")
    chart = MainChart(plot_net_revenue_ebitda(df, 'Percentage'))
    chart2 = MainChart(create_waterfall_chart(totals[period], period))
    table= get_top5_tables(df)


    return kpi_section, chart2, chart, table

@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/" or pathname == "/summary":
        return html.Div([
            Header(),
            html.Div(id='current-selections'),
            html.Div(id='kpi-container'),
            html.Div(id='chart-container'),
            html.Div(id='chart-container2'),
            html.Div(id='top5-container'),
        ])
    elif pathname == "/revenue-graphs":
        return html.Div([
            html.Div(id="resize-trigger", style={"display": "none"}),
            html.Script("window.addEventListener('load', () => { window.dispatchEvent(new Event('resize')); });"),
            Header(),
            html.Div(id='current-selections'),
            html.Div(id='revenue-graphs-container')  # ⬅️ where we'll render the period graphs
        ])
    elif pathname == "/cost-graphs":
        return html.Div([
            html.Div(id="resize-trigger", style={"display": "none"}),
            html.Script("window.addEventListener('load', () => { window.dispatchEvent(new Event('resize')); });"),
            Header(),
            html.Div(id='current-selections'),
            html.Div(id='cost-graphs-container')  # ⬅️ where we'll render the period graphs
        ])
    else:
        return html.H1("404 - Page not found", style={"textAlign": "center"})
@app.callback(
    Output('revenue-graphs-container', 'children'),
    [
        Input('period-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('area-coach-dropdown', 'value'),
        Input('store-dropdown', 'value')
    ]
)
def update_period_graphs(period, region, area_coach, store):
    if not period:
        raise PreventUpdate

    if not region and not area_coach and not store:
        data = all_store_data
        totals = calculate_totals_per_period(data, 'All', 'All')
    elif store:
        data = all_store_data_region[region][area_coach][store]
        totals = calculate_totals_per_period(data, 'Store', 'All')
    elif area_coach:
        data = all_store_data_region[region][area_coach]
        totals = calculate_totals_per_period(data, 'All', 'All')
    else:
        data = all_store_data_region[region]
        totals = calculate_totals_per_period(data, 'Region', 'All')

    df = pd.DataFrame.from_dict(totals, orient='index')
    df['Period'] = df.index
    single_cache = preprocess_comparison_data(totals)
    weekly_cache = preprocess_comparison_data(convert_to_weekly(totals))

    return important_metrics(df, single_cache, weekly_cache,'revenue')

@app.callback(
    Output('cost-graphs-container', 'children'),
    [
        Input('period-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('area-coach-dropdown', 'value'),
        Input('store-dropdown', 'value')
    ]
)
def update_cost_graphs(period, region, area_coach, store):
    if not period:
        raise PreventUpdate

    if not region and not area_coach and not store:
        data = all_store_data
        totals = calculate_totals_per_period(data, 'All', 'All')
    elif store:
        data = all_store_data_region[region][area_coach][store]
        totals = calculate_totals_per_period(data, 'Store', 'All')
    elif area_coach:
        data = all_store_data_region[region][area_coach]
        totals = calculate_totals_per_period(data, 'All', 'All')
    else:
        data = all_store_data_region[region]
        totals = calculate_totals_per_period(data, 'Region', 'All')

    df = pd.DataFrame.from_dict(totals, orient='index')
    df['Period'] = df.index
    single_cache = preprocess_comparison_data(totals)
    weekly_cache = preprocess_comparison_data(convert_to_weekly(totals))

    return important_metrics(df, single_cache, weekly_cache, 'cost')

@app.callback(
    [Output("sidebar", "style"),
     Output("page-content", "style")],
    [Input("sidebar-toggle", "n_clicks")]
)
def toggle_sidebar(n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        # Sidebar hidden
        return SIDEBAR_HIDDEN_STYLE, CONTENT_EXPANDED_STYLE
    else:
        # Sidebar shown
        return SIDEBAR_STYLE, CONTENT_STYLE

@app.callback(
    Output('top5-cost-table', 'data'),
    Output('top5-cost-table', 'columns'),
    [
        Input('cost-component-dropdown', 'value'),
        Input('period-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('area-coach-dropdown', 'value'),
        Input('store-dropdown', 'value')
    ]
)
def update_top5_cost_table(component, period, region, area_coach, store):
    if not component or not period:
        raise PreventUpdate

    # Scope the data
    if not region and not area_coach and not store:
        data = all_store_data
        data_type = 'All'
    elif store:
        data = all_store_data_region[region][area_coach][store]
        data_type = 'Store'
    elif area_coach:
        data = all_store_data_region[region][area_coach]
        data_type = 'All'
    else:
        data = all_store_data_region[region]
        data_type = 'Region'

    store_data = extract_all_line_items(data, period, data_type=data_type)
    df = pd.DataFrame.from_dict(store_data, orient='index')
    df = df[[component, 'Net Revenue']].dropna()
    df = df[df['Net Revenue'] > 0]
    df['% of Revenue'] = (df[component] / df['Net Revenue']) * 100
    df = df.sort_values(by=component, ascending=False).head(5).reset_index().rename(columns={'index': 'Store'})

    columns = [{'name': col, 'id': col} for col in df.columns]
    return df.to_dict('records'), columns


@app.callback(
    Output('top5-revenue-table', 'data'),
    Output('top5-revenue-table', 'columns'),
    [
        Input('revenue-component-dropdown', 'value'),
        Input('period-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('area-coach-dropdown', 'value'),
        Input('store-dropdown', 'value')
    ]
)
def update_top5_cost_table(component, period, region, area_coach, store):
    if not component or not period:
        raise PreventUpdate

    # Scope the data
    if not region and not area_coach and not store:
        data = all_store_data
        data_type = 'All'
    elif store:
        data = all_store_data_region[region][area_coach][store]
        data_type = 'Store'
    elif area_coach:
        data = all_store_data_region[region][area_coach]
        data_type = 'All'
    else:
        data = all_store_data_region[region]
        data_type = 'Region'

    store_data = extract_all_line_items(data, period, data_type=data_type)
    df = pd.DataFrame.from_dict(store_data, orient='index')
    df = df[[component, 'Net Revenue']].dropna()
    df = df[df['Net Revenue'] > 0]
    df['% of Revenue'] = (df[component] / df['Net Revenue']) * 100
    df = df.sort_values(by=component, ascending=False).head(5).reset_index().rename(columns={'index': 'Store'})

    columns = [{'name': col, 'id': col} for col in df.columns]
    return df.to_dict('records'), columns


app.clientside_callback(
    """
    function(n_clicks) {
        setTimeout(() => {
            window.dispatchEvent(new Event("resize"));
        }, 100);
        return "";
    }
    """,
    Output("resize-trigger", "children"),
    Input("sidebar-toggle", "n_clicks")
)
# ------------- Run Server -------------
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=7000, debug=True)

