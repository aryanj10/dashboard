import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Group, Scheme
import dash_table
import dash_bootstrap_components as dbc
from common_util import convert_to_weekly, plot_stacked_bar,plot_comparison_by_period_from_cache, preprocess_comparison_data, percentage_plot




def plot_net_ebitda(revenue_df, title):
    fig = go.Figure()
    
    # Add Net Revenue trace
    fig.add_trace(go.Bar(
        x=revenue_df['Period'],
        y=revenue_df['Net Revenue'],
        name='Net Revenue',
        marker=dict(color='blue'),
        hovertemplate='%{y:$,.2f}'
    ))

    # Add EBITDA trace
    fig.add_trace(go.Bar(
        x=revenue_df['Period'],
        y=revenue_df['EBITDA'],
        name='EBITDA',
        marker=dict(color=revenue_df['EBITDA'].apply(lambda x: 'green' if x >= 0 else 'red')),
        hovertemplate='%{y:$,.2f}'
    ))

    avg_revenue = revenue_df['Net Revenue'].mean()

    # Add a line for average revenue
    fig.add_trace(go.Scatter(
        x=revenue_df['Period'],
        y=[avg_revenue] * len(revenue_df),  # Repeat the average for all periods
        mode='lines',
        name='Average Revenue',
        line=dict(color='black', dash='dash'),
        hovertemplate=f'Average Revenue: ${avg_revenue:,.2f}'
    ))

    fig.update_layout(
        barmode='group',  # Grouped bar mode to display bars side by side
        title=title,
        xaxis_title='Period',
        yaxis_title='Amount ($)',
        height=600,
        template='plotly',
        legend_title='Metrics',
        hovermode='x unified'
    )
    return fig



def important_metrics(df, single_cache, weekly_cache, path):

    if path == 'revenue':
        components =["KFC Revenue", "Taco Bell Revenue", 
                    "LJS Revenue", "Digital Revenue",
                    "Co-Brand Locations Revenue", "Philly Beverage Revenue", 
                    "Coupons - KFC", "Coupons - TB"
                    , "Coupons - LJS", "Coupons - Co-Brand Locations",
                    "Other Discounts", "Total Coupons & Discounts"]
        return dbc.Container([
            html.H4("Revenue Trends", className="mt-4 mb-4 text-primary",style={'textAlign': 'center'}),

        # Net Revenue
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_net_ebitda(df, 'Net Revenue vs EBITDA'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_stacked_bar(df, components,'Revenue Breakdown','Revenue Breakdown'),
                    config={"responsive": True},
                    style={'height': '450px'}
                                            ))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_comparison_by_period_from_cache(single_cache, 'Net Revenue', 'Net Revenue'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ))
            ]),

        # Weekly Revenue
            dbc.Row([
                dbc.Col(dcc.Graph(
                figure=plot_comparison_by_period_from_cache(weekly_cache, 'Net Revenue', 'Weekly Revenue'),
                config={"responsive": True},
                style={'height': '450px'}
            ), width=12)
        ]),

        # EBITDA
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_comparison_by_period_from_cache(single_cache, 'EBITDA', 'EBITDA'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ), width=12)
            ]),
                    dbc.Row([
            dbc.Col([
                html.H5("Top 5 Stores by Selected Cost Component"),
                dcc.Dropdown(
                    id='revenue-component-dropdown',
                    options=[{'label': comp, 'value': comp} for comp in components],
                    value=components[0],
                    clearable=False,
                    style={'width': '300px', 'marginBottom': '20px'}
                ),
                dash_table.DataTable(
                    id='top5-revenue-table',
                    columns=[],  # will be filled by callback
                    data=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'center'},
                    style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'}
                )
            ])
        ])

            ], fluid=True)
    
    
    elif path == 'cost':
        components = ["Poultry", "Other Food", "Drinks", "Paper",
                    "F&P Cost of Sales", "Philly Beverage Tax",
                    "Beverage Rebates", "COGS Discounts", "F&P Rebates & Discounts"]

        return dbc.Container([
            html.H4("Cost of Sales", className="mt-4 mb-4 text-primary", style={'textAlign': 'center'}),

            # Stacked Bar
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_stacked_bar(df, components, 'Cost of Sales Breakdown', 'Breakdown'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ))
            ]),

            # Comparison by Period
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=plot_comparison_by_period_from_cache(single_cache, 'Total Cost of Sales', 'Total Cost of Sales ($)'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ))
            ]),

            # Percentage Plot
            dbc.Row([
                dbc.Col(dcc.Graph(
                    figure=percentage_plot(df, 'Total Cost of Sales', 'Total Cost of Sales (%)'),
                    config={"responsive": True},
                    style={'height': '450px'}
                ))
            ]),

            # Dropdown and Top 5 Table
            dbc.Row([
                dbc.Col([
                    html.H5("Top 5 Stores by Selected Cost Component"),
                    dcc.Dropdown(
                        id='cost-component-dropdown',
                        options=[{'label': comp, 'value': comp} for comp in components],
                        value=components[0],
                        clearable=False,
                        style={'width': '300px', 'marginBottom': '20px'}
                    ),
                    dash_table.DataTable(
                        id='top5-cost-table',
                        columns=[],  # will be filled by callback
                        data=[],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center'},
                        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'}
                    )
                ])
            ])
        ], fluid=True)
