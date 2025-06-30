import pandas as pd
import numpy as np
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from common_util import convert_to_weekly
"""def update_period_comparison_graph(period_totals):

    # Generate the comparison graph

    fig_rev = plot_comparison_by_period(period_totals, 'Net Revenue','Net Revenue')
    fig_ebit = plot_comparison_by_period(period_totals, 'EBITDA','EBITDA')

    #period_totals_weekly = calculate_totals_per_period_weekly(all_store_data)
    period_totals_weekly=convert_to_weekly(period_totals)
# Specify the line item you want to plot (e.g., 'Net Revenue')
    fig_weekly_rev=plot_comparison_by_period(period_totals_weekly, 'Net Revenue','Weekly Revenue')

    fig_tcos = plot_comparison_by_period(period_totals, 'Total Cost of Sales','Total Cost of Sales ($)')

    fig_tcos_per=percentage_plot(period_totals,'Total Cost of Sales','Total Cost of Sales (%)')

    fig_control = plot_comparison_by_period(period_totals, 'Controllable Store Level Payroll','Controllable Store Level Payroll ($)')

    fig_control_per=percentage_plot(period_totals,'Controllable Store Level Payroll','Controllable Store Level Payroll (%)')

    fig_rgm = plot_comparison_by_period(period_totals, 'Restaurant General Managers','Restaurant General Managers')

    fig_rgm_agm=aum_rgm(period_totals)

    line_items = ['Team Labor', 'Shift Supervisors', 'Assistant Managers', 'Assistant Managers OT']
    fig_non_grm=plot_comparison_by_period_multi(period_totals, line_items,'Non-RGM Labor ($)')
    fig_non_grm_per=percentage_plot_multi(period_totals, line_items,'Non-RGM Labor')
    
    line_items = ['Assistant Managers', 'Assistant Managers OT']
    fig_aum=plot_comparison_by_period_multi(period_totals, line_items,'Total AUM + OT ($)')    
    fig_aum_per=percentage_plot_multi(period_totals, line_items,'Total AUM + OT')
    
    line_items = ['Team Labor OT', 'Shift Supervisors OT', 'Assistant Managers OT']
    fig_ot=plot_comparison_by_period_multi(period_totals, line_items,'Total OT ($)')

    line_items = ['Shift Supervisors', 'Shift Supervisors OT']
    fig_ss_ot=plot_comparison_by_period_multi(period_totals, line_items,'Shift Supervisors + OT ($)')
    fig_ss_per=percentage_plot_multi(period_totals, line_items,'Shift Supervisors + OT')
    fig_ss = plot_comparison_by_period(period_totals, 'Shift Supervisors OT','Shift Supervisors + OT ($)')

    line_items = ['Team Labor', 'Team Labor OT']
    fig_tb_ot=plot_comparison_by_period_multi(period_totals, line_items,'Team Labor + OT ($)')
    fig_tb_per=percentage_plot_multi(period_totals, line_items,'Team Labor + OT')
    fig_tb = plot_comparison_by_period(period_totals, 'Team Labor OT','Team Labor + OT ($)')

    fig_st = plot_comparison_by_period(period_totals, 'Store Training','Store Training ($)')
    fig_pto = plot_comparison_by_period(period_totals, 'PTO','PTO ($)')

    fig_tu = plot_comparison_by_period(period_totals, 'Total Utilities','Total Utilities ($)')

    fig_tu_per=percentage_plot(period_totals,'Total Utilities','Total Utilities (%)')

    fig_ue = plot_comparison_by_period(period_totals, 'Utilities - Electric','Utilities - Electric ($)')
    fig_ug = plot_comparison_by_period(period_totals, 'Utilities - Gas','Utilities - Gas ($)')
    fig_uw = plot_comparison_by_period(period_totals, 'Utilities - Water/Sewer','Utilities - Water/Sewer ($)')
    fig_ut = plot_comparison_by_period(period_totals, 'Utilities - Trash','Utilities - Trash ($)')

    fig_rm = plot_comparison_by_period(period_totals, 'Repairs & Maintenance','Repairs & Maintenance ($)')
    
    fig_pm = plot_comparison_by_period(period_totals, 'Planned Maintenance','Planned Maintenance ($)')
    fig_pm_per=percentage_plot(period_totals,'Planned Maintenance','Planned Maintenance (%)')

    # Return the graph
    return [dcc.Graph(figure=fig_rev,style={'width': '33%'}),dcc.Graph(figure=fig_ebit,style={'width': '33%'}),dcc.Graph(figure=fig_weekly_rev,style={'width': '33%'}),
            dcc.Graph(figure=fig_tcos,style={'width': '45%'}),dcc.Graph(figure=fig_tcos_per,style={'width': '45%'}),
            dcc.Graph(figure=fig_control,style={'width': '45%'}),dcc.Graph(figure=fig_control_per,style={'width': '45%'}),
            dcc.Graph(figure=fig_rgm,style={'width': '45%'}),dcc.Graph(figure=fig_rgm_agm,style={'width': '45%'}),
            dcc.Graph(figure=fig_non_grm,style={'width': '45%'}),dcc.Graph(figure=fig_non_grm_per,style={'width': '45%'}),
            dcc.Graph(figure=fig_aum,style={'width': '33%'}),dcc.Graph(figure=fig_aum_per,style={'width': '33%'}),dcc.Graph(figure=fig_ot,style={'width': '33%'}),
            dcc.Graph(figure=fig_ss_ot,style={'width': '33%'}),dcc.Graph(figure=fig_ss_per,style={'width': '33%'}),dcc.Graph(figure=fig_ss,style={'width': '33%'}),
            dcc.Graph(figure=fig_tb_ot,style={'width': '33%'}),dcc.Graph(figure=fig_tb_per,style={'width': '33%'}),dcc.Graph(figure=fig_tb,style={'width': '33%'}),
            dcc.Graph(figure=fig_st,style={'width': '45%'}),dcc.Graph(figure=fig_pto,style={'width': '45%'}),
            dcc.Graph(figure=fig_tu,style={'width': '45%'}),dcc.Graph(figure=fig_tu_per,style={'width': '45%'}),
            dcc.Graph(figure=fig_ue,style={'width': '45%'}),dcc.Graph(figure=fig_ug,style={'width': '45%'}),
            dcc.Graph(figure=fig_uw,style={'width': '45%'}),dcc.Graph(figure=fig_ut,style={'width': '45%'}),
            dcc.Graph(figure=fig_rm,style={'width': '33%'}),dcc.Graph(figure=fig_pm,style={'width': '33%'}),dcc.Graph(figure=fig_pm_per,style={'width': '33%'}),
            ]"""

















def update_period_comparison_graph(period_totals):
    # Preprocess once for all single-item plots
    single_cache = preprocess_comparison_data(period_totals)
    
    # Preprocess for weekly plots
    weekly_cache = preprocess_comparison_data(convert_to_weekly(period_totals))

    df = pd.DataFrame.from_dict(period_totals, orient='index')

    # Preprocess multi-line combinations
    multi_cache = preprocess_multi_line_data(period_totals, [
        ['Team Labor', 'Shift Supervisors', 'Assistant Managers', 'Assistant Managers OT'],
        ['Assistant Managers', 'Assistant Managers OT'],
        ['Team Labor OT', 'Shift Supervisors OT', 'Assistant Managers OT'],
        ['Shift Supervisors', 'Shift Supervisors OT'],
        ['Team Labor', 'Team Labor OT']
    ])

    return [
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Net Revenue', 'Net Revenue'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'EBITDA', 'EBITDA'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(weekly_cache, 'Net Revenue', 'Weekly Revenue'), style={'width': '33%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Total Cost of Sales', 'Total Cost of Sales ($)'), style={'width': '45%'}),
        dcc.Graph(figure=percentage_plot(df, 'Total Cost of Sales', 'Total Cost of Sales (%)'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Controllable Store Level Payroll', 'Controllable Store Level Payroll ($)'), style={'width': '45%'}),
        dcc.Graph(figure=percentage_plot(df, 'Controllable Store Level Payroll', 'Controllable Store Level Payroll (%)'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Restaurant General Managers', 'Restaurant General Managers'), style={'width': '45%'}),
        dcc.Graph(figure=aum_rgm(df), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_multi_cached(multi_cache, 'Team Labor + Shift Supervisors + Assistant Managers + Assistant Managers OT', 'Non-RGM Labor ($)'), style={'width': '45%'}),
        dcc.Graph(figure=percentage_plot_multi_cached(df, ['Team Labor', 'Shift Supervisors', 'Assistant Managers', 'Assistant Managers OT'], 'Non-RGM Labor'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_multi_cached(multi_cache, 'Assistant Managers + Assistant Managers OT', 'Total AUM + OT ($)'), style={'width': '33%'}),
        dcc.Graph(figure=percentage_plot_multi_cached(df, ['Assistant Managers', 'Assistant Managers OT'], 'Total AUM + OT'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_multi_cached(multi_cache, 'Team Labor OT + Shift Supervisors OT + Assistant Managers OT', 'Total OT ($)'), style={'width': '33%'}),

        dcc.Graph(figure=plot_comparison_by_period_multi_cached(multi_cache, 'Shift Supervisors + Shift Supervisors OT', 'Shift Supervisors + OT ($)'), style={'width': '33%'}),
        dcc.Graph(figure=percentage_plot_multi_cached(df, ['Shift Supervisors', 'Shift Supervisors OT'], 'Shift Supervisors + OT'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Shift Supervisors OT', 'Shift Supervisors + OT ($)'), style={'width': '33%'}),

        dcc.Graph(figure=plot_comparison_by_period_multi_cached(multi_cache, 'Team Labor + Team Labor OT', 'Team Labor + OT ($)'), style={'width': '33%'}),
        dcc.Graph(figure=percentage_plot_multi_cached(df, ['Team Labor', 'Team Labor OT'], 'Team Labor + OT'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Team Labor OT', 'Team Labor + OT ($)'), style={'width': '33%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Store Training', 'Store Training ($)'), style={'width': '45%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'PTO', 'PTO ($)'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Total Utilities', 'Total Utilities ($)'), style={'width': '45%'}),
        dcc.Graph(figure=percentage_plot(df, 'Total Utilities', 'Total Utilities (%)'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Utilities - Electric', 'Utilities - Electric ($)'), style={'width': '45%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Utilities - Gas', 'Utilities - Gas ($)'), style={'width': '45%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Utilities - Water/Sewer', 'Utilities - Water/Sewer ($)'), style={'width': '45%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Utilities - Trash', 'Utilities - Trash ($)'), style={'width': '45%'}),

        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Repairs & Maintenance', 'Repairs & Maintenance ($)'), style={'width': '33%'}),
        dcc.Graph(figure=plot_comparison_by_period_from_cache(single_cache, 'Planned Maintenance', 'Planned Maintenance ($)'), style={'width': '33%'}),
        dcc.Graph(figure=percentage_plot(df, 'Planned Maintenance', 'Planned Maintenance (%)'), style={'width': '33%'}),
    ]



def preprocess_multi_line_data(period_totals, line_items_list, trailing_periods=12):
    """
    Precomputes current and previous period totals for multiple line item combinations.
    Returns a dictionary: {label: (periods, current_totals, previous_totals)}
    """
    multi_data = {}

    for line_items in line_items_list:
        label = ' + '.join(line_items) if isinstance(line_items, list) else line_items
        periods = []
        current_values = []
        prev_values = []

        for period in period_totals:
            current_total = sum(period_totals[period].get(item, 0) for item in line_items)

            # Skip periods with no meaningful data
            if current_total == 0:
                continue

            periods.append(period)
            current_values.append(current_total)

            # Calculate previous total
            prev_total = 0
            if '-' in period:
                p_parts = period.split('-')
                if len(p_parts) == 2 and p_parts[1].isdigit():
                    prev_period = f"{p_parts[0]}-{int(p_parts[1]) - 1:02d}"
                    if prev_period in period_totals:
                        prev_total = sum(period_totals[prev_period].get(item, 0) for item in line_items)

            prev_values.append(prev_total)

        multi_data[label] = (
            periods[-trailing_periods:],
            current_values[-trailing_periods:],
            prev_values[-trailing_periods:]
        )

    return multi_data

def plot_comparison_by_period_multi_cached(cached_data, label, title):
    periods, current_values, prev_values = cached_data.get(label, ([], [], []))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=periods,
        y=prev_values,
        name='Previous Period Totals',
        text=[f"{val:,.2f}" for val in prev_values],
        textposition='inside',
        marker_color='orange',
        hovertemplate='%{y:$,.2f}'
    ))
    fig.add_trace(go.Bar(
        x=periods,
        y=current_values,
        name='Current Period Totals',
        text=[f"{val:,.2f}" for val in current_values],
        textposition='inside',
        marker_color='blue',
        hovertemplate='%{y:$,.2f}'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Periods',
        yaxis_title='Total Values ($)',
        barmode='group',
        template='plotly_white',
        xaxis_tickangle=45,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def percentage_plot_multi_cached(df, line_items, title):
    #df = pd.DataFrame.from_dict(period_totals, orient='index')
    df = df[['Net Revenue'] + line_items].fillna(0)
    df['Period'] = df.index

    df[title] = df[line_items].sum(axis=1)
    df[f'{title} (%)'] = (df[title] / df['Net Revenue']) * 100

    df = df[-12:]

    x_indices = np.arange(len(df))
    trend_y = np.polyval(np.polyfit(x_indices, df[f'{title} (%)'], 1), x_indices)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Net Revenue'],
        name='Net Revenue',
        marker_color='grey',
        hovertemplate='%{y:$,.2f}'
    ))
    fig.add_trace(go.Scatter(
        x=df['Period'],
        y=df[f'{title} (%)'],
        name=f'{title} (%)',
        mode='lines+markers+text',
        text=df[f'{title} (%)'].round(2),
        textposition='top center',
        line=dict(color='orange'),
        yaxis='y2',
        hovertemplate='%{y:.2f}%'
    ))
    fig.add_trace(go.Scatter(
        x=df['Period'],
        y=trend_y,
        mode='lines',
        line=dict(color='red', width=2, dash='dot'),
        yaxis='y2',
        name='Trendline'
    ))

    fig.update_layout(
        title=f'{title} (%)',
        xaxis=dict(title='Period', tickangle=45),
        yaxis=dict(title='Dollar Values ($)', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
        yaxis2=dict(title='Value (%)', titlefont=dict(color='orange'), tickfont=dict(color='orange'), overlaying='y', side='right'),
        barmode='group',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    return fig



def plot_comparison_by_period(period_totals, line_item,title):
    # Sort periods and prepare for plotting
    sorted_periods = period_totals.keys()

    # Initialize lists to store the values and period labels
    current_values = []
    prev_values = []
    periods = []

    # Loop through each period and add the value for the specified line item
    for period in sorted_periods:
        # Extract the totals for the current period
        current_period_data = period_totals[period]
        
        # Check if the specified line item is available for the current period
        if line_item in current_period_data:
            current_value = current_period_data[line_item]
            current_values.append(current_value)
            periods.append(period)
            
            # Check if the previous period exists and extract its value for comparison
            prev_value = None
            prev_period = None
            if 'P' in period:
                period_parts = period.split('-')
                if len(period_parts) > 1:
                    prev_period = f"{period_parts[0]}-{int(period_parts[1])-1:02d}"
            
            # If previous period exists and has data for the line item, fetch its value
            if prev_period and prev_period in period_totals and line_item in period_totals[prev_period]:
                prev_value = period_totals[prev_period][line_item]
            else:
                prev_value = 0  # If no previous value, set to 0

            prev_values.append(prev_value)
    
    current_values = current_values[-12:]
    prev_values = prev_values[-12:]
    periods = periods[-12:]
    # Create the bar plot
    fig = go.Figure()

    # Add bars for the current period values
    fig.add_trace(go.Bar(
        x=periods,
        y=prev_values,
        name=f'{line_item} (Previous)',
        text=[f"{val:,.2f}" for val in prev_values],  # Add text values
        textposition='inside',
        marker_color='orange',
        hovertemplate='%{y:$,.2f}'
    ))
    fig.add_trace(go.Bar(
        x=periods,
        y=current_values,
        name=f'{line_item} (Current)',
        text=[f"{val:,.2f}" for val in current_values],  # Add text values
        textposition='inside',
        marker_color='blue',
        hovertemplate='%{y:$,.2f}'
    ))

    # Add bars for the previous period values
    all_values = current_values
    x_indices = np.arange(len(all_values))  # Numeric indices for regression

    # Perform linear regression for trendline
    trend_coeffs = np.polyfit(x_indices, all_values, deg=1)  # Linear trendline
    trend_y = np.polyval(trend_coeffs, x_indices)  # Calculate trend line values

    # Add the trendline
    fig.add_trace(go.Scatter(
        x=periods,  # Use the same periods for alignment
        y=trend_y,
        mode='lines',
        line=dict(color='red', width=2,dash='dot'),
        name='Trendline'
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Periods',
        yaxis_title='Total Values ($)',
        barmode='group',  # Grouped bars for comparison
        template='plotly_white',
        xaxis_tickangle=45,
        hovermode='x unified',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend to bottom of the graph
            y=-0.4,  # Position below the graph
            xanchor="center",  # Center legend horizontally
            x=0.5  # Center align with the graph
        )
    )

    return fig

def percentage_plot(df,line_item,title):
    
    df = df[['Net Revenue', line_item]].fillna(0)  # Ensure relevant columns exist, fill missing with 0
    df['Period'] = df.index
    # Calculate percentages for Total Cost of Sales and Store Level Payroll & Benefits
    df[f'{line_item} (%)'] = (df[line_item] / df['Net Revenue']) * 100
    
    df=df[-12:]
    
    all_values = df[f'{line_item} (%)']
    x_indices = np.arange(len(all_values))  # Numeric indices for regression

    # Perform linear regression for trendline
    trend_coeffs = np.polyfit(x_indices, all_values, deg=1)  # Linear trendline
    trend_y = np.polyval(trend_coeffs, x_indices)  # Calculate trend line values
    
    fig = go.Figure()

    # Add Net Revenue bars
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Net Revenue'],
        name='Net Revenue',
        marker_color='grey',#'#f2f2f2',
        hovertemplate='%{y:$,.2f}'
    ))  
    
    fig.add_trace(go.Scatter(
            x=df['Period'],
            y=df[f'{line_item} (%)'],
            name=f'{line_item} (%)',
            mode='lines+markers+text',
            text=df[f'{line_item} (%)'].round(2),
            textposition='top center',
            line=dict(color='orange'),
            yaxis='y2',  # Map to secondary y-axis
            hovertemplate='%{y:.2f}%'
        ))
    fig.add_trace(go.Scatter(
        x=df['Period'],  # Use the same periods for alignment
        y=trend_y,
        mode='lines',
        line=dict(color='red', width=2,dash='dot'),
        yaxis='y2',
        name='Trendline'
    ))
    fig.update_layout(
            title=title,
            xaxis=dict(title='Period', tickangle=45),
            yaxis=dict(
                title='Dollar Values ($)',
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title='Value (%)',
                titlefont=dict(color='orange'),
                tickfont=dict(color='orange'),
                overlaying='y',
                side='right'  # Place on the right side
            ),
            barmode='group',  # Grouped bar plot
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend to bottom of the graph
            y=-0.4,  # Position below the graph
            xanchor="center",  # Center legend horizontally
            x=0.5  # Center align with the graph
        )  # Adjust legend position
        )
    

    return fig

def aum_rgm(df):
    #df = pd.DataFrame.from_dict(period_totals, orient='index')
    
    df = df[['Net Revenue','Restaurant General Managers','Assistant Managers','Assistant Managers OT']].fillna(0)  # Ensure relevant columns exist, fill missing with 0
    df['Period'] = df.index
    df=df[-12:]
    df['Total AUM + OT ($)']=df['Assistant Managers']+df['Assistant Managers OT']
    df['Total AUM + OT (%)']=(df['Total AUM + OT ($)']/df['Net Revenue'])*100
    
    #df['AUM+RGM ($)']=df['Total AUM + OT ($)']+df['Restaurant General Managers']
    df['AUM+RGM (%)']=((df['Restaurant General Managers'])/df['Net Revenue'])*100
    
    fig=go.Figure()
    
    fig.add_trace(go.Scatter(
            x=df['Period'],
            y=df[f'Net Revenue'],
            name=f'Net Revenue',
            mode='lines',
            line=dict(color='blue'),
            yaxis='y2',  # Map to secondary y-axis
            hovertemplate='%{y:.2f}%'
        ))
    
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Total AUM + OT (%)'],
        name='Total AUM + OT (%)',
        marker_color='grey',#'#f2f2f2',
        text=[f"{val:,.2f}" for val in df['Total AUM + OT (%)']],  # Add text values
        textposition='inside',
        hovertemplate='%{y:%,.2f}'
    ))  
    
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['AUM+RGM (%)'],
        name='AUM+RGM (%)',
        marker_color='pink',#'#f2f2f2',
        text=[f"{val:,.2f}" for val in df['AUM+RGM (%)']],  # Add text values
        textposition='inside',        
        hovertemplate='%{y:%,.2f}'
    ))  
    
    fig.update_layout(
            title=f'AUM+RGM',
            xaxis=dict(title='Period', tickangle=45),
            yaxis=dict(
                title='Value (%)',
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title='Dollar Values ($)',
                titlefont=dict(color='orange'),
                tickfont=dict(color='orange'),
                overlaying='y',
                side='right'  # Place on the right side
            ),
            barmode='stack',  # Grouped bar plot
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend to bottom of the graph
            y=-0.4,  # Position below the graph
            xanchor="center",  # Center legend horizontally
            x=0.5  # Center align with the graph
        )  # Adjust legend position
        )   
    
    return fig

def plot_comparison_by_period_multi(period_totals, line_items,title):
    """
    Plots a comparison of the total values for specified line items across periods.

    Args:
        period_totals (dict): Dictionary where keys are period names and values are dictionaries of line item totals.
        line_items (list): List of line items to sum and compare.
    """
    # Sort periods and prepare for plotting
    sorted_periods = period_totals.keys()  # Sort periods to plot them sequentially

    # Initialize lists to store the values and period labels
    current_values = []
    prev_values = []
    periods = []

    # Loop through each period and calculate the total value for the specified line items
    for period in sorted_periods:
        if period.endswith('B'):
            continue
        # Extract the totals for the current period
        current_period_data = period_totals[period]
        
        # Calculate the total for the specified line items
        current_total = sum(current_period_data.get(item, 0) for item in line_items)
        current_values.append(current_total)
        periods.append(period)
        
        # Determine the previous period
        prev_value = 0  # Default to 0 if no previous data is available
        prev_period = None
        if 'P' in period:
            period_parts = period.split('-')
            if len(period_parts) > 1:
                prev_period = f"{period_parts[0]}-{int(period_parts[1])-1:02d}"
        
        # Calculate the total for the specified line items in the previous period
        if prev_period and prev_period in period_totals:
            prev_value = sum(period_totals[prev_period].get(item, 0) for item in line_items)
        prev_values.append(prev_value)
    
    # Restrict data to the last 12 periods
    current_values = current_values[-12:]
    prev_values = prev_values[-12:]
    periods = periods[-12:]
    
    # Create the bar plot
    fig = go.Figure()

    # Add bars for the previous period values
    fig.add_trace(go.Bar(
        x=periods,
        y=prev_values,
        name='Previous Period Totals',
        text=[f"{val:,.2f}" for val in prev_values],  # Add text values
        textposition='inside',
        marker_color='orange',
        hovertemplate='%{y:$,.2f}'
    ))
    
    # Add bars for the current period values
    fig.add_trace(go.Bar(
        x=periods,
        y=current_values,
        name='Current Period Totals',
        text=[f"{val:,.2f}" for val in current_values],  # Add text values
        textposition='inside',
        marker_color='blue',
        hovertemplate='%{y:$,.2f}'
    ))

    # Perform linear regression for trendline
    # Update layout
    fig.update_layout(
        title=f'{title}',
        xaxis_title='Periods',
        yaxis_title='Total Values ($)',
        barmode='group',  # Grouped bars for comparison
        template='plotly_white',
        xaxis_tickangle=45,
        hovermode='x unified',
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",  # Align legend to bottom of the graph
            y=-0.4,  # Position below the graph
            xanchor="center",  # Center legend horizontally
            x=0.5  # Center align with the graph
        )
    )

    return fig

def percentage_plot_multi(period_totals, line_items,title):
    """
    Plots percentage contribution of specified line items to Net Revenue along with Net Revenue values.

    Args:
        period_totals (dict): Dictionary where keys are period names and values are dictionaries of line item totals.
        line_items (list): List of line items to sum and calculate percentage for.
    """
    # Convert the period_totals dictionary to a DataFrame
    df = pd.DataFrame.from_dict(period_totals, orient='index')
    
    # Ensure relevant columns exist and fill missing values with 0
    df = df[['Net Revenue'] + line_items].fillna(0)
    df['Period'] = df.index

    # Calculate the total for the specified line items
    df[f'{title}'] = df[line_items].sum(axis=1)

    # Calculate percentages for the total line items as a fraction of Net Revenue
    df[f'{title} (%)'] = (df[f'{title}'] / df['Net Revenue']) * 100

    # Restrict to the last 12 periods
    df = df[-12:]

    # Calculate trendline for the percentage
    all_values = df[f'{title} (%)']
    x_indices = np.arange(len(all_values))  # Numeric indices for regression
    trend_coeffs = np.polyfit(x_indices, all_values, deg=1)  # Linear trendline
    trend_y = np.polyval(trend_coeffs, x_indices)  # Calculate trend line values

    # Create the plot
    fig = go.Figure()

    # Add Net Revenue bars
    fig.add_trace(go.Bar(
        x=df['Period'],
        y=df['Net Revenue'],
        name='Net Revenue',
        marker_color='grey',
        hovertemplate='%{y:$,.2f}'
    ))

    # Add Total Line Items (%) as a line plot
    fig.add_trace(go.Scatter(
        x=df['Period'],
        y=df[f'{title} (%)'],
        name=f'{title} (%)',
        mode='lines+markers+text',
        text=df[f'{title} (%)'].round(2),
        textposition='top center',
        line=dict(color='orange'),
        yaxis='y2',  # Map to secondary y-axis
        hovertemplate='%{y:.2f}%'
    ))

    # Add the trendline
    fig.add_trace(go.Scatter(
        x=df['Period'],
        y=trend_y,
        mode='lines',
        line=dict(color='red', width=2, dash='dot'),
        yaxis='y2',
        name='Trendline'
    ))

    # Update the layout
    fig.update_layout(
        title=f'{title} (%)',
        xaxis=dict(title='Period', tickangle=45),
        yaxis=dict(
            title='Dollar Values ($)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Value (%)',
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange'),
            overlaying='y',
            side='right'  # Place on the right side
        ),
        barmode='group',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    # Show the plot
    return fig

####################################################
def convert_to_weekly(period_totals):
    for period, line_items in period_totals.items():
        # Extract the prefix (e.g., 'P3' from 'P3-23')
        period_prefix = period.split('-')[0]
        divisor = 5 if period_prefix in {'P3', 'P6', 'P9', 'P12'} else 4
        for line_item in line_items:
            line_items[line_item] /= divisor
    return period_totals




def calculate_ytd_totals_auto(all_store_data, peri, year, data_type, period_suffix=""):
    ytd_totals = {}
    periods = set()
    if data_type == 'All':
    # Gather all periods for the given year, including optional suffix
        for store, periods_data in all_store_data.items():
            for period in periods_data.keys():
            # Match periods like "P1-23" or "P1-23B" based on the suffix
                if period.endswith(f"{year}{period_suffix}"):
                    periods.add(period)

    # Sort periods to determine the range
        sorted_periods = sorted(periods)  # Sorting ensures periods are in order
    
    
        if not sorted_periods:
            raise ValueError(f"No periods found for year {year}{period_suffix}.")

    # Calculate YTD totals for the identified range
    
        for store, periods_data in all_store_data.items():
            for period, line_items in periods_data.items():
                if period in sorted_periods:
                    if int(period.split('-')[0][1:]) > int(peri[1:]):
                        continue
                    for line_item, value in line_items.items():
                        value_to_add = round(value)
                        if line_item in ytd_totals:
                            ytd_totals[line_item] += value_to_add
                        else:
                            ytd_totals[line_item] = value_to_add
    elif data_type=='Region':
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                for period, line_items in periods_data.items():
                    if period.endswith(f"{year}{period_suffix}"):
                        periods.add(period)
        
        sorted_periods = sorted(periods)  # Sorting ensures periods are in order
    
    
        if not sorted_periods:
            raise ValueError(f"No periods found for year {year}{period_suffix}.")
            
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                for period, line_items in periods_data.items():
                    if period in sorted_periods:
                        if int(period.split('-')[0][1:]) > int(peri[1:]):
                            continue
                        for line_item, value in line_items.items():
                            value_to_add = round(value)
                            if line_item in ytd_totals:
                                ytd_totals[line_item] += value_to_add
                            else:
                                ytd_totals[line_item] = value_to_add     
                                
    elif data_type=='Store':        
            for period in all_store_data.keys():
                if period.endswith(f"{year}{period_suffix}"):
                    periods.add(period)
                
            sorted_periods = sorted(periods)
        
        
            for period, line_items in all_store_data.items():
                if period in sorted_periods:
                    if int(period.split('-')[0][1:]) > int(peri[1:]):
                        continue
                    for line_item, value in line_items.items():
                        value_to_add = round(value)
                        if line_item in ytd_totals:
                            ytd_totals[line_item] += value_to_add
                        else:
                            ytd_totals[line_item] = value_to_add
    
    return {'YTD':ytd_totals}

def calculate_last_12_month_totals(all_store_data, peri, data_type):
    totals_last_12_months = {}
    valid_periods = []
    if data_type == 'All':
    # Gather all periods and sort them
        for period in all_store_data[list(all_store_data.keys())[0]].keys():
            # Match periods with the same year and suffix
            if not period.endswith("B") and period!='metadata':
                valid_periods.append(period)

    
    # Sort periods to determine chronological order
    #print("Available sorted periods:", sorted_periods)
    
        last_12_periods = valid_periods[valid_periods.index(peri)-11:valid_periods.index(peri)+1]

    # Calculate totals for the last 12 months
    
        for store, periods_data in all_store_data.items():
            for period, line_items in periods_data.items():
                if period in last_12_periods:
                    for line_item, value in line_items.items():
                        value_to_add = round(value)
                        if line_item in totals_last_12_months:
                            totals_last_12_months[line_item] += value_to_add
                        else:
                            totals_last_12_months[line_item] = value_to_add
                            
    elif data_type=='Region':
        first_region_key = list(all_store_data.keys())[0]
        
        first_store_key = list(all_store_data[first_region_key].keys())[0]
        
        for period in all_store_data[first_region_key][first_store_key].keys():
            if not period.endswith("B") and period!='metadata':
                valid_periods.append(period)
        
        last_12_periods = valid_periods[valid_periods.index(peri)-11:valid_periods.index(peri)+1]
        
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                for period, line_items in periods_data.items():
                    if period in last_12_periods:
                        for line_item, value in line_items.items():
                            value_to_add = round(value)
                            if line_item in totals_last_12_months:
                                totals_last_12_months[line_item] += value_to_add
                            else:
                                totals_last_12_months[line_item] = value_to_add
        
    elif data_type=='Store':
        for period in all_store_data.keys():
            # Match periods with the same year and suffix
            if not period.endswith("B") and period!='metadata':
                valid_periods.append(period)      
        
        last_12_periods = valid_periods[valid_periods.index(peri)-11:valid_periods.index(peri)+1]
        
        for period, line_items in all_store_data.items():
            if period in last_12_periods:
                for line_item, value in line_items.items():
                    value_to_add = round(value)
                    if line_item in totals_last_12_months:
                        totals_last_12_months[line_item] += value_to_add
                    else:
                        totals_last_12_months[line_item] = value_to_add 
                
            
        

    return {'Last_12_Months': totals_last_12_months}



def calculate_totals_side_by_side_period(all_store_data, period, data_type):
    period_totals = {}
    
    if data_type == 'All':
        # Loop through all stores' data
        for store, periods_data in all_store_data.items():
            # Check if the current period matches the desired period
            if period in periods_data:
                line_items = periods_data[period]
                # Initialize the period in the totals dictionary if not already done
                if period not in period_totals:
                    period_totals[period] = {}
                for line_item, value in line_items.items():
                    value_to_add = round(value)
                    # Add the values for the line items in the specific period
                    if line_item in period_totals[period]:
                        period_totals[period][line_item] += value_to_add
                    else:
                        period_totals[period][line_item] = value_to_add
    
    elif data_type=='Region':
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                if period in periods_data:
                    line_items = periods_data[period]
                # Initialize the period in the totals dictionary if not already done
                if period not in period_totals:
                    period_totals[period] = {}
                for line_item, value in line_items.items():
                    value_to_add = round(value)
                    # Add the values for the line items in the specific period
                    if line_item in period_totals[period]:
                        period_totals[period][line_item] += value_to_add
                    else:
                        period_totals[period][line_item] = value_to_add        
                    
    elif data_type=='Store':
        period_totals={period:all_store_data[period]}
    
    return period_totals



def return_table(all_store_data,pp,data_type):
    abc = calculate_totals_side_by_side_period(all_store_data, period=pp, data_type=data_type)
    df_actual = pd.DataFrame.from_dict(abc[pp], orient='index', columns=['Actual'])
# Get the budget data for 'P10-24B' (calculate_totals_side_by_side_period for budget)
    abc_budget = calculate_totals_side_by_side_period(all_store_data, period=f'{pp}B', data_type=data_type)

# Create the Budget column
    df_actual['Budget'] = pd.Series(abc_budget[f'{pp}B'])

    df_actual['Bud. Var($)']=df_actual['Actual']-df_actual['Budget']
    df_actual['Bud. Var(%)']=(df_actual['Bud. Var($)']/df_actual['Budget'])*100
    abc_budget = calculate_totals_side_by_side_period(all_store_data
                                                  ,period=pp.split('-')[0]+'-'+str(int(pp.split('-')[1])-1)
                                                  , data_type=data_type)
# Create the Budget column
    df_actual['Prior Year'] = pd.Series(abc_budget[pp.split('-')[0]+'-'+str(int(pp.split('-')[1])-1)])
    df_actual['PY Var($)'] = df_actual['Actual']-df_actual['Prior Year']
    df_actual['PY Var(%)']=(df_actual['PY Var($)']/df_actual['Prior Year'])*100
    df_actual['Actual(%)']=(df_actual['Actual']/df_actual['Actual']['Net Revenue'])*100
    df_actual['Budget(%)']=(df_actual['Budget']/df_actual['Budget']['Net Revenue'])*100
    df_actual['PY(%)']=(df_actual['Prior Year']/df_actual['Prior Year']['Net Revenue'])*100

    abc_ytd_24=calculate_ytd_totals_auto(all_store_data, peri=pp.split('-')[0], year=pp.split('-')[1], data_type=data_type, period_suffix="")
    df_actual['YTD Actual']=pd.Series(abc_ytd_24['YTD'])

    abc_ytd_24B=calculate_ytd_totals_auto(all_store_data, peri=pp.split('-')[0], year=pp.split('-')[1], data_type=data_type, period_suffix="B")
    df_actual['YTD Budget']=pd.Series(abc_ytd_24B['YTD'])

    df_actual['Bud. Var YTD($)']=df_actual['YTD Actual']-df_actual['YTD Budget']
    df_actual['Bud. Var YTD(%)']=(df_actual['Bud. Var YTD($)']/df_actual['YTD Budget'])*100


    abc_ytd_23=calculate_ytd_totals_auto(all_store_data, peri=pp.split('-')[0], year=str(int(pp.split('-')[1])-1), data_type=data_type, period_suffix="")
    df_actual['YTD PY']=pd.Series(abc_ytd_23['YTD'])

    df_actual['YTD PY Var($)'] = df_actual['YTD Actual']-df_actual['YTD PY']
    df_actual['YTD PY Var(%)']=(df_actual['YTD PY Var($)']/df_actual['YTD PY'])*100

    abc_ltm_24=calculate_last_12_month_totals(all_store_data, peri=pp, data_type=data_type)
    df_actual['LTM']=pd.Series(abc_ltm_24['Last_12_Months'])

    abc_ltm_23=calculate_last_12_month_totals(all_store_data, peri=pp.split('-')[0]+'-'+str(int(pp.split('-')[1])-1)
                                          , data_type=data_type)
    df_actual['LTM PY']=pd.Series(abc_ltm_23['Last_12_Months'])

    df_actual['LTM Var($)']=df_actual['LTM']-df_actual['LTM PY']

    df_actual['LTM Var(%)']=(df_actual['LTM Var($)']/df_actual['LTM PY'])*100


    df_actual['YTD Actual(%)']=(df_actual['YTD Actual']/df_actual['YTD Actual']['Net Revenue'])*100
    df_actual['YTD Budget(%)']=(df_actual['YTD Budget']/df_actual['YTD Budget']['Net Revenue'])*100
    df_actual['YTD PY(%)']=(df_actual['YTD PY']/df_actual['YTD PY']['Net Revenue'])*100
    df_actual['LTM(%)']=(df_actual['LTM']/df_actual['LTM']['Net Revenue'])*100

    if data_type=='All':
        columns = [pd.Series(all_store_data[store][pp], name=store) for store in all_store_data.keys()]
        stores= pd.concat(columns, axis=1)
        df_actual = pd.concat([df_actual, stores], axis=1)
    elif data_type=='Region':
        for coach,coach_data in all_store_data.items():
            columns=[pd.Series(coach_data[store][pp], name=store) for store in coach_data.keys()]
            stores=pd.concat(columns,axis=1)
            df_actual = pd.concat([df_actual, stores], axis=1)
    return df_actual




def extract_data_zscore(all_store_data,selected_line_item,data_type):
    data = {}
    
    if data_type=='All':
    # Build the data dictionary
        for store, store_data in all_store_data.items():
            for period, period_data in store_data.items():
                if period == 'metadata' or period.endswith("B"):
                    continue
                if store not in data:
                    data[store] = {}
                data[store][period] = period_data.get(selected_line_item, None)
    
    elif data_type=='Region':
        for coach, coach_data in all_store_data.items():
            for store, store_data in coach_data.items():
                for period, period_data in store_data.items():
                    if period == 'metadata' or period.endswith("B"):
                        continue
                    if store not in data:
                        data[store] = {}
                    data[store][period] = period_data.get(selected_line_item, None)  

    # Convert data dictionary to DataFrame
    df = pd.DataFrame(data)
    return df.T  # Transpose to have stores as rows and periods as columns

def extract_data_zscore_store(all_store_data,store,selected_line_item):
    data={}
    for period, period_data in all_store_data.items():
        if period == 'metadata' or period.endswith("B"):
            continue
        if store not in data:
            data[store] = {}
        data[store][period] = period_data.get(selected_line_item, None)  
    
    df = pd.DataFrame(data)
    return df.T  # Transpose to have stores as rows and periods as columns  

def get_cell_style(z_store, z_period, max_store_zscore, max_period_zscore,min_store_zscore, min_period_zscore, threshold):
    style = {}

    if z_store>threshold:
        if z_store==max_store_zscore:
            style['backgroundColor'] = '#FFD700' 
            style['color'] = 'white'
        else:
            style['backgroundColor'] = '#FFB6B6' 
            style['color'] = 'black'

    elif z_period>threshold:
        if z_period==max_period_zscore:
            style['backgroundColor'] = '#FFA500'
            style['color'] = 'white'
        else:
            style['backgroundColor'] = '#FF0000' 
            style['color'] = 'white'
    
    elif z_store==min_store_zscore:
        style['backgroundColor'] = '#ADD8E6'  
        style['color'] = 'black'

    elif z_period==min_period_zscore:
        style['backgroundColor'] = '#87CEEB'  
        style['color'] = 'black'
    else:
        style['backgroundColor'] = 'white'
        style['color'] = 'black'


    """if abs(z_store) > threshold and abs(z_period) > threshold:

    elif abs(z_period) > threshold:
        style['backgroundColor'] = '#FFB6B6'  # Light Red
        style['color'] = 'black'
    elif abs(z_store) > threshold:
        if z_store == max_store_zscore:
            style['backgroundColor'] = '#FFA500'  # Dark Orange
            style['color'] = 'white'
        else:
            style['backgroundColor'] = '#FFD700'  # Orange
            style['color'] = 'black'
    elif z_store == min_store_zscore:
        style['backgroundColor'] = '#ADD8E6'  # Light Blue
        style['color'] = 'black'
    elif z_period == min_period_zscore:"""


        
    return style