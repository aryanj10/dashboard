from dash import Input, Output, html, dcc, dash, ctx
from dash.exceptions import PreventUpdate
import pandas as pd
from utils.common_util import (calculate_totals_per_period, extract_all_line_items,
                        preprocess_comparison_data, convert_to_weekly, tables_page)

from components.views_code import KPISection, MainChart, AreaSelector, StoreSelector, Header

from components.summary_page import  get_top5_tables, plot_net_revenue_ebitda, create_waterfall_chart

from components.revenue_page import important_metrics

from components.style_comp import SIDEBAR_STYLE, SIDEBAR_HIDDEN_STYLE, CONTENT_STYLE, CONTENT_EXPANDED_STYLE



def register_page_callbacks(app, all_store_data, all_store_data_region,graph):
    @app.callback(
        Output(f'{graph}-graphs-container', 'children'),
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

        return important_metrics(df, single_cache, weekly_cache, graph)
    
    @app.callback(
        Output(f'top5-{graph}-table', 'data'),
        Output(f'top5-{graph}-table', 'columns'),
        [
            Input(f'{graph}-component-dropdown', 'value'),
            Input('period-dropdown', 'value'),
            Input('region-dropdown', 'value'),
            Input('area-coach-dropdown', 'value'),
            Input('store-dropdown', 'value')
        ]
    )
    def update_top5_graph_table(component, period, region, area_coach, store):
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
        

        return tables_page(df, component)
