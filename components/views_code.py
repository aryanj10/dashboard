
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
from plotly.subplots import make_subplots
import re

import dash_bootstrap_components as dbc




def Header():
    return html.Div([
        html.H3("Welcome Back!", style={"fontWeight": "bold"}),
        html.P("Here's what's happening with your stores this period")
    ])


def AreaSelector( default_area=None):
    return dcc.Dropdown(
            id='area-coach-dropdown',
            placeholder="Select Area Coach",
            value=None,
            style={'width': '205px', 'margin-bottom': '20px'}
        )
def StoreSelector(default_store=None):
    return dcc.Dropdown(
            id='store-dropdown',
            placeholder="Select Store",
            value=None,
            style={'width': '205px', 'margin-bottom': '20px'}
        )
def get_kpi_deltas(current, previous):
    if previous == 0:
        return "N/A", "text-muted"
    delta = ((current - previous) / previous) * 100
    delta_text = f"{delta:+.1f}% this Period"
    delta_class = "text-success" if delta >= 0 else "text-danger"
    return delta_text, delta_class

def KPISection(cogs, cogs_prev, revenue, revenue_prev, ebitda, ebitda_prev):
    cogs_delta, cogs_class = get_kpi_deltas(cogs, cogs_prev)
    rev_delta, rev_class = get_kpi_deltas(revenue, revenue_prev)
    ebitda_delta, ebitda_class = get_kpi_deltas(ebitda, ebitda_prev)

    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"${cogs:,.0f}", className="card-title"),
                html.P("Total Cost of Sales"),
                html.Small(cogs_delta, className=cogs_class)
            ])
        ]), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"${revenue:,.0f}", className="card-title"),
                html.P("Total Revenue"),
                html.Small(rev_delta, className=rev_class)
            ])
        ]), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"${ebitda:,.0f}", className="card-title"),
                html.P("EBITDA"),
                html.Small(ebitda_delta, className=ebitda_class)
            ])
        ]), width=4),
    ], style={"marginTop": "20px"})

def MainChart(fig):
    return html.Div([
        html.Hr(),
        #html.H5("Net Revenue vs EBITDA vs Expense (Percentage View)", style={"marginTop": "2px"}),
        dcc.Graph(figure=fig, config={"responsive": True},style={"height": "600px", "width": "100%"})
    ])





