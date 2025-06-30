from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate

from components.rag_page import search_index, build_prompt, ask_together  # your chatbot logic

def register_rag_callbacks(app):
    @app.callback(
        Output("rag-answer-output", "children"),
        Input("submit-query", "n_clicks"),
        State("user-question", "value"),
        prevent_initial_call=True
    )
    def handle_rag_question(n_clicks, question):
        if not question:
            raise PreventUpdate
        try:
            top_chunks = search_index(question, top_k=5)
            prompt = build_prompt(top_chunks, question)
            answer = ask_together(prompt)
            return html.Div([
                html.H5("📣 Answer:"),
                html.P(answer),
            ])
        except Exception as e:
            return html.Div(f"❌ Error: {str(e)}", style={"color": "red"})
