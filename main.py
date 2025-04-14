from flask import Flask, session, redirect, url_for, request, render_template
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import plotly.express as px
import io
from dash.exceptions import PreventUpdate
import base64
import re
import dash_table
import dash_bootstrap_components as dbc

from utils.common_util import (calculate_totals_per_period, extract_all_line_items,
                        preprocess_comparison_data, convert_to_weekly, tables_page)

from components.views_code import KPISection, MainChart, AreaSelector, StoreSelector, Header

from components.summary_page import  get_top5_tables, plot_net_revenue_ebitda, create_waterfall_chart

from components.revenue_page import important_metrics

from components.style_comp import SIDEBAR_STYLE, SIDEBAR_HIDDEN_STYLE, CONTENT_STYLE, CONTENT_EXPANDED_STYLE



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
        dcc.Link("Controllable Store Level Payroll", href="/control-graphs", style={"display": "block", "margin-bottom": "10px"}),
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


from callbacks.general_callbacks import register_general_callbacks
register_general_callbacks(app, all_store_data, all_store_data_region)

from callbacks.summary_callbacks import register_summary_callbacks
register_summary_callbacks(app, all_store_data, all_store_data_region)

from callbacks.page_callbacks import register_page_callbacks

for page_type in ['revenue', 'cost', 'control']:
    register_page_callbacks(app, all_store_data, all_store_data_region, page_type)


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

