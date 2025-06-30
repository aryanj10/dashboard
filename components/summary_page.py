import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Group, Scheme
import dash_table


def make_table(title, data, column_name):
    return html.Div([
        html.Div(title, style={
            'textAlign': 'center',
            'fontWeight': '600',
            'fontSize': '18px',
            'marginBottom': '10px'
        }),
        dash_table.DataTable(
            columns=[
                {"name": "Store", "id": "Store"},
                {"name": column_name, "id": column_name, "type": "numeric",
                 "format": Format(precision=2, scheme=Scheme.fixed, group=Group.yes)}
            ],
            data=data[['Store', column_name]].to_dict('records'),
            style_table={
                'overflowX': 'auto',
                'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                'borderRadius': '8px',
            },
            style_header={
                'backgroundColor': '#f8f9fa',
                'color': '#495057',
                'fontWeight': 'bold',
                'fontSize': '14px'
            },
            style_data={
                'backgroundColor': 'white',
                'color': '#212529',
                'fontSize': '14px'
            },
            style_cell={
                'textAlign': 'center',
                'padding': '8px',
                'border': '1px solid #dee2e6',
            },
        )
    ], style={
        'flex': '1',
        'padding': '15px',
        'maxWidth': '350px',
        'minWidth': '250px',
    })


def get_top5_tables(df):
    #df = pd.DataFrame.from_dict(store_data, orient='index')
    df = df[['Net Revenue', 'Total Cost of Sales', 'EBITDA']].fillna(0)
    df = df[df['Net Revenue'] > 0]

    # Sort and take top 5
    top_revenue = df['Net Revenue'].sort_values( ascending=False).head(5).reset_index().rename(columns={'index': 'Store'})
    top_cogs = df['Total Cost of Sales'].sort_values( ascending=False).head(5).reset_index().rename(columns={'index': 'Store','Total Cost of Sales': 'Cost of Sales'})
    top_ebitda = df['EBITDA'].sort_values( ascending=False).head(5).reset_index().rename(columns={'index': 'Store'})

    return html.Div([
        make_table("Top 5 by Revenue", top_revenue, 'Net Revenue'),
        make_table("Top 5 by COGS", top_cogs, 'Cost of Sales'),
        make_table("Top 5 by EBITDA", top_ebitda, 'EBITDA')
    ], style={
    'display': 'flex',
    'justifyContent': 'center',
    'gap': '25px',
    'flexWrap': 'wrap',
    'marginTop': '30px'
})



def plot_net_revenue_ebitda(df, plot_type):


    # Convert store_data to a pandas DataFrame
    
    df = df[['Net Revenue', 'EBITDA', 'Total Cost of Sales', 'Store Level Payroll & Benefits']].fillna(0)
    df.index.name = 'Store'
    df.reset_index(inplace=True)
    df = df[df['Net Revenue'] > 0]
    df = df.sort_values(by='Net Revenue', ascending=False)

    # Calculate percentages
    df['Total Cost of Sales (%)'] = (df['Total Cost of Sales'] / df['Net Revenue']) * 100
    df['Payroll & Benefits (%)'] = (df['Store Level Payroll & Benefits'] / df['Net Revenue']) * 100

    fig = go.Figure()

    # Common traces (always visible)
    fig.add_trace(go.Bar(
        x=df['Store'], y=df['Net Revenue'],
        name='Net Revenue',
        marker_color='blue',
        hovertemplate='%{y:$,.2f}',
        visible=True
    ))

    ebitda_colors = ['green' if val >= 0 else 'red' for val in df['EBITDA']]
    fig.add_trace(go.Bar(
        x=df['Store'], y=df['EBITDA'],
        name='EBITDA',
        marker_color=ebitda_colors,
        hovertemplate='%{y:$,.2f}',
        visible=True
    ))

    # Percentage traces
    fig.add_trace(go.Scatter(
        x=df['Store'], y=df['Total Cost of Sales (%)'],
        name='Total Cost of Sales (%)',
        mode='lines',
        line=dict(color='orange'),
        yaxis='y2',
        hovertemplate='%{y:.2f}%',
        visible=True
    ))

    fig.add_trace(go.Scatter(
        x=df['Store'], y=df['Payroll & Benefits (%)'],
        name='Payroll & Benefits (%)',
        mode='lines',
        line=dict(color='purple'),
        yaxis='y2',
        hovertemplate='%{y:.2f}%',
        visible=True
    ))

    # Dollar traces
    fig.add_trace(go.Scatter(
        x=df['Store'], y=df['Total Cost of Sales'],
        name='Total Cost of Sales',
        mode='lines',
        line=dict(color='orange', dash='dot'),
        yaxis='y2',
        hovertemplate='%{y:.2f}',
        visible=False
    ))

    fig.add_trace(go.Scatter(
        x=df['Store'], y=df['Store Level Payroll & Benefits'],
        name='Store Level Payroll & Benefits',
        mode='lines',
        line=dict(color='purple', dash='dot'),
        yaxis='y2',
        hovertemplate='%{y:.2f}',
        visible=False
    ))

    # Update layout
    fig.update_layout(
        title='Net Revenue, EBITDA, and Expense',
        xaxis=dict(title='Stores', tickangle=45),
        yaxis=dict(
            title='Dollar Values ($)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Percentages (%)',
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange'),
            overlaying='y',
            side='right'
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
        ),
        updatemenus=[dict(
            type="buttons",
            direction="right",
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.2,
            yanchor="top",
            buttons=[
                dict(
                    label="Percentage",
                    method="update",
                    args=[
                        {"visible": [True, True, True, True, False, False]},
                        {"yaxis2.title": "Percentages (%)"}
                    ]
                ),
                dict(
                    label="Dollar",
                    method="update",
                    args=[
                        {"visible": [True, True, False, False, True, True]},
                        {"yaxis2.title": "Value ($)"}
                    ]
                )
            ]
        )]
    )

    return fig




def create_waterfall_chart(store_data, period):
    """
    Create a waterfall chart for a single store and specific period.
    """
    data = {
        #'Total Gross Revenue': store_data['Total Gross Revenue'],
        'Net Revenue': store_data['Net Revenue'],
        'Total Cost of Sales':-store_data['Total Cost of Sales'],
        'Store Level Payroll & Benefits':-store_data['Store Level Payroll & Benefits'],
        'Total Utilities': -store_data['Total Utilities'],
        'Total Maintenance': -store_data['Total Maintenance'],
        'Total Operating Costs': -store_data['Total Operating Costs'],
        'Total Occupancy Costs': -store_data['Total Occupancy Costs'],
        'Total Advertising & Marketing Expense': -store_data['Total Advertising & Marketing Expense'],
        'Total Royalties': -store_data['Total Royalties'],
        'Total General & Admin Expenses': -store_data['Total General & Admin Expenses'],
        'Other (Income) & Expense':-store_data['Other (Income) & Expense'],
        'EBITDA': store_data['EBITDA'],
}

    labels = list(data.keys())
    values = list(data.values())
    measure = ['absolute'] + ['relative'] * (len(values) - 2) + ['total']
    ebitda_color = "lightgreen" if data['EBITDA'] >= 0 else "crimson"

    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=measure,
        x=labels,
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "crimson"}},
        increasing={"marker": {"color": "lightgreen"}},
        totals={"marker": {"color": ebitda_color}}
    ))

    fig.update_layout(
        title=f"Waterfall Chart of Store Financials – {period}",
        autosize=True,
        height=None,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_white",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )


    return fig
