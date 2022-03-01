import pandas as pd
import altair as alt

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

data = pd.read_csv("data/processed/survey.csv")
logo = "https://cdn-icons-png.flaticon.com/512/2017/2017231.png"

def tabs():
    tabs_layout = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Summary Overview", tab_id="tab-1"),
                    dbc.Tab(label="Interactive View", tab_id="tab-2"),
                    dbc.Tab(label="Map View", tab_id="tab-3"),
                ],
                id="tabs",
                active_tab="tab-1",
            ),
            html.Div(
                id="tabs-content",
                className="contents",
                style={"text-align": "left", "margin": "auto"},
            )
        ]
    )
    return tabs_layout

  
def tab1():
    """Layout structure for Summary Overview"""
    summary_overview = html.Div(
        [
            dbc.Col([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P(
                    children=[
                        html.H3("Loremipsum"),
                        html.Br(),
                        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                        html.Br(),
                        html.H3("Loremipsum"),
                        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),                
                    ]
                )
            ], width=2)           
        ]
    )
    
    return summary_overview
    
def tab2():
    """Layout structure for Interactive View"""
    interactive_view = html.Div(
        [
            dbc.Col([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P(
                    children=[
                        html.H3("Controls"),
                    ]
                )
            ], width=2)           
        ]
    )
    
    return interactive_view
    
def tab3():
    """Layout structure for Map View"""
    map_view = html.Div(
        [
            dbc.Col([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P(
                    children=[
                        html.H3("Controls"),
                    ]
                )
            ], width=2)           
        ]
    )
    
    return map_view

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Mental Health in Tech Dashboard", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="https://github.com/UBC-MDS/mental_health_in_tech_dashboard",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="dark",
    dark=True,
)
  
app.layout = html.Div([
    dbc.Row([
        navbar,
        tabs(),
    ])
])

@app.callback(
    Output("tabs-content", "children"), [Input("tabs", "active_tab")]
)

def select_tab(active_tab):
    if active_tab == "tab-1":
        return tab1()
    elif active_tab == "tab-2":
        return tab2()
    elif active_tab == "tab-3":
        return tab3()

    
if __name__ == '__main__':
    app.run_server(debug=True)