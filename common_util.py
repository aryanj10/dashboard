import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import zscore
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


####################################################
def convert_to_weekly(period_totals):
    for period, line_items in period_totals.items():
        # Extract the prefix (e.g., 'P3' from 'P3-23')
        period_prefix = period.split('-')[0]
        divisor = 5 if period_prefix in {'P3', 'P6', 'P9', 'P12'} else 4
        for line_item in line_items:
            line_items[line_item] /= divisor
    return period_totals

def calculate_totals_per_period(all_store_data,data_type,div_type):
    period_totals = {}
    
    if data_type=='All':
    
        for store, periods_data in all_store_data.items():
            for period, line_items in periods_data.items():
                if period == 'metadata' or period.endswith('B'):
                    continue
                if period not in period_totals:
                    period_totals[period] = {}
                for line_item, value in line_items.items():
                    value_to_add = round(value)
                    if line_item in period_totals[period]:
                        period_totals[period][line_item] += value_to_add
                    else:
                        period_totals[period][line_item] = value_to_add
    elif data_type=='Region':
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                for period, line_items in periods_data.items():
                    if period == 'metadata' or period.endswith('B'):
                        continue
                    if period not in period_totals:
                        period_totals[period] = {}
                    for line_item, value in line_items.items():
                        value_to_add = round(value)
                        if line_item in period_totals[period]:
                            period_totals[period][line_item] += value_to_add
                        else:
                            period_totals[period][line_item] = value_to_add    
    
    elif data_type == 'Store':
        period_totals = {
            period: line_items for period, line_items in all_store_data.items()
            if not period.endswith('B')
        }
            
            
    else:
        period_totals={}
    
    if div_type=='Weekly':
        for period, line_items in period_totals.items():
        # Extract the prefix (e.g., 'P3' from 'P3-23')
            period_prefix = period.split('-')[0]
            divisor = 5 if period_prefix in {'P3', 'P6', 'P9', 'P12'} else 4
            for line_item in line_items:
                line_items[line_item] /= divisor
    
    return period_totals



def extract_all_line_items(all_store_data, period,data_type):
    store_data = {}
    if data_type=='All':
    # Loop through each store's data in all_store_data
        for store, periods_data in all_store_data.items():
        # Check if the period exists in the store's data
            if period in periods_data:
            # Store all line items for the given period
                store_data[store] = periods_data[period]
    elif data_type=='Region':
        for coach, coachs_data in all_store_data.items(): 
            for store, periods_data in coachs_data.items():
                if period in periods_data:
            # Store all line items for the given period
                    store_data[store] = periods_data[period]
    else:
        store_data={}
    return store_data




def plot_stacked_bar(revenue_df, columns_to_plot, title, legend_title):
    """
    Plots a stacked bar chart for a specific cluster and specified revenue columns.

    Parameters:
    - revenue_df: DataFrame containing the revenue data.
    - columns_to_plot: A list of column names to plot.

    Returns:
    - None (displays the plot).
    """
    # Create figure
    fig = go.Figure()

    # Filter data for the specified cluster
    color_map=['blue','lightblue','orange','lightcoral','green','lightgreen',
               'purple','pink','red','gray','yellow','blue','lightblue','orange','lightcoral','green','lightgreen',
               'purple','pink','red','gray','yellow']
    # Add traces for each specified column
    i=0
    for column in columns_to_plot:
        
        fig.add_trace(go.Bar(
            x=revenue_df['Period'],
            y=revenue_df[column],
            name=column,
            marker=dict(color=color_map[i])  # Cycle through a colormap
        ))
        i=i+1
    
    # Update the layout to display as a stacked bar chart
    fig.update_layout(
        barmode='stack',  # Stacked bar mode
        title=title,
        xaxis_title='Store',
        yaxis_title='Amount ($)',
        height=600,
        template='plotly',
        legend_title=f'{legend_title} Components',
        hovermode='x unified'
    )

    # Show the plot
    return fig


def preprocess_comparison_data(period_totals, trailing_periods=12):
    """
    Precomputes current and previous period values for all line items.
    Returns a dictionary: {line_item: (periods, current_values, prev_values)}
    """
    comparison_data = {}
    all_line_items = set()

    # Gather all possible line items
    for period_data in period_totals.values():
        all_line_items.update(period_data.keys())

    for line_item in all_line_items:
        periods = []
        current_values = []
        prev_values = []

        for period in period_totals:
            if line_item not in period_totals[period]:
                continue

            current_value = period_totals[period][line_item]
            current_values.append(current_value)
            periods.append(period)

            # Get previous period
            prev_period = None
            if '-' in period:
                p_parts = period.split('-')
                if len(p_parts) == 2 and p_parts[1].isdigit():
                    prev_period = f"{p_parts[0]}-{int(p_parts[1]) - 1:02d}"

            if prev_period and prev_period in period_totals and line_item in period_totals[prev_period]:
                prev_value = period_totals[prev_period][line_item]
            else:
                prev_value = 0

            prev_values.append(prev_value)

        # Store last N periods only
        comparison_data[line_item] = (
            periods[-trailing_periods:],
            current_values[-trailing_periods:],
            prev_values[-trailing_periods:]
        )

    return comparison_data

def plot_comparison_by_period_from_cache(cached_data, line_item, title):
    periods, current_values, prev_values = cached_data.get(line_item, ([], [], []))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=periods, y=prev_values, name=f'{line_item} (Previous)',
                         text=[f"{v:,.2f}" for v in prev_values], textposition='inside',
                         marker_color='orange', hovertemplate='%{y:$,.2f}'))
    fig.add_trace(go.Bar(x=periods, y=current_values, name=f'{line_item} (Current)',
                         text=[f"{v:,.2f}" for v in current_values], textposition='inside',
                         marker_color='blue', hovertemplate='%{y:$,.2f}'))

    # Add trendline
    x_indices = np.arange(len(current_values))
    trend = np.polyval(np.polyfit(x_indices, current_values, 1), x_indices)
    fig.add_trace(go.Scatter(x=periods, y=trend, mode='lines',
                             line=dict(color='red', width=2, dash='dot'), name='Trendline'))

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
