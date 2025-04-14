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
