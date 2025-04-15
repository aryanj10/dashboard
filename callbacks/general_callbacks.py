from dash import Input, Output, html, dcc, dash, ctx
from dash.exceptions import PreventUpdate
import pandas as pd
from utils.common_util import (calculate_totals_per_period, extract_all_line_items,
                        preprocess_comparison_data, convert_to_weekly, tables_page)

from components.views_code import KPISection, MainChart, AreaSelector, StoreSelector, Header

from components.summary_page import  get_top5_tables, plot_net_revenue_ebitda, create_waterfall_chart

from components.revenue_page import important_metrics

from components.style_comp import SIDEBAR_STYLE, SIDEBAR_HIDDEN_STYLE, CONTENT_STYLE, CONTENT_EXPANDED_STYLE


def register_general_callbacks(app, all_store_data, all_store_data_region):
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
        elif pathname == "/control-graphs":
            return html.Div([
                html.Div(id="resize-trigger", style={"display": "none"}),
                html.Script("window.addEventListener('load', () => { window.dispatchEvent(new Event('resize')); });"),
                Header(),
                html.Div(id='current-selections'),
                html.Div(id='control-graphs-container')  # ⬅️ where we'll render the period graphs
            ])
        elif pathname == "/askAI":
            return html.Div([
                html.Hr(),
                html.H4("💬 Ask the Dashboard Anything"),
                dcc.Textarea(
                id="user-question",
                placeholder="Ask about Net Revenue, EBITDA, Utilities, Area Coaches, etc.",
                style={"width": "100%", "height": "100px"}
                ),
                html.Button("Submit", id="submit-query", n_clicks=0),
                html.Div(id="rag-answer-output", style={"marginTop": "20px"})
                ])  
        
        else:
            return html.H1("404 - Page not found", style={"textAlign": "center"})








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






