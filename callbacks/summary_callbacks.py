from dash import Input, Output, html, dcc, dash, ctx
from dash.exceptions import PreventUpdate
import pandas as pd
from utils.common_util import (calculate_totals_per_period, extract_all_line_items)

from components.views_code import KPISection, MainChart

from components.summary_page import  get_top5_tables, plot_net_revenue_ebitda, create_waterfall_chart






def register_summary_callbacks(app, all_store_data, all_store_data_region):
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
