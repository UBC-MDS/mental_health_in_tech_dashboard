import pandas as pd
import altair as alt
import numpy as np

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

data = pd.read_csv("data/processed/survey.csv")
data = data.drop(data[data["Q8"] == "Female"].index)
logo = "https://cdn-icons-png.flaticon.com/512/2017/2017231.png"

# data wrangling for plots

# create employer size df
size = data.drop(data[data["Q5"] == "Female"].index)

# create gender count and percentage df
gender = data
gender[gender["Gender"] == "Woman"] = "Female"
gender[gender["Gender"] == "woman"] = "Female"

gender = pd.DataFrame(gender["Gender"].value_counts())

gender["Gender"] = gender["Gender"].astype(int)
gender["Pctg"] = round((gender["Gender"] / np.sum(gender["Gender"]))*100, 2)
gender["Count"] = gender["Gender"]
gender["Gender"] = gender.index

# create age df
age = data.drop(data[data["Age"] == "Female"].index)
age = age.dropna()

# create benefit count and percentage df
data = data.drop(data[data["Q8"] == "Female"].index)
benefit = pd.DataFrame(data["Q8"].value_counts())

benefit["Benefit"] = benefit["Q8"].astype(int)
benefit["Pctg"] = round((benefit["Benefit"] / np.sum(benefit["Benefit"]))*100, 2)
benefit["Count"] = benefit["Q8"]
benefit["Answer"] = benefit.index


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
    
    """Test plot"""
    
    
    # pie plot for gender
    pie_gender = alt.Chart(gender).mark_arc(outerRadius = 120).encode(
        theta = alt.Theta("Count:Q", stack = True), 
        color = alt.Color("Gender:N")
    )

    text = pie_gender.mark_text(radius = 140, size = 20).encode(
        text = "Pctg:Q",
        color = "Gender")

    pg = pie_gender + text
    
    
    # bar plot for size
    bar_size = alt.Chart(size).mark_bar().encode(
        alt.X("count():Q"),
        alt.Y("Q5:N", sort = "-x", axis=alt.Axis(title='Company Size'))
     )

    # bar plot for age
    bar_age = alt.Chart(age).mark_bar().encode(
        alt.X("count():Q"),
        alt.Y("Age:N", sort = "-x")
    )
    
    # pie plot for benefit
    pie_benefit = alt.Chart(benefit).mark_arc(outerRadius = 100).encode(
        theta = alt.Theta("Count:Q", stack = True), 
        color = alt.Color("Answer:N")
    )

    text = pie_benefit.mark_text(radius = 140, size = 20).encode(
        text = "Pctg:Q",
        color = "Answer")

    pb = pie_benefit + text


    summary_overview = html.Div(
        [dbc.Row([
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
            ], width=3),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Iframe(
                            id = 'pg',
                            srcDoc = pg.to_html(),
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        )
                    ]),
                    dbc.Col([
                        html.Iframe(
                            id = 'bar_size',
                            srcDoc = bar_size.to_html(),
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        )
                    ])

                ]),
                dbc.Row([
                    dbc.Col([
                        html.Iframe(
                            id = 'bar_age',
                            srcDoc = bar_age.to_html(),
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        )
                    ]),
                    dbc.Col([
                        html.Iframe(
                            id = 'pb',
                            srcDoc = pb.to_html(),
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        )
                    ])
                ])
            ])
        ])
        ]
    )
    

    
    return summary_overview
    
def tab2():
    """Layout structure for Interactive View"""
    qlist = ["Q14", "Q15", "Q21"]
    chart_tpye = ["bar", "pie"]
    genderlist = ["Male", "Female", "Other"]
    sizelist = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
    agelist = ["18-24", "25-34", "35-44", "45-54", "55+"]

    interactive_view = html.Div(
        [dbc.Row([
                dbc.Col([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P(
                    children=[
                        html.H3("Controls"),
                        html.Br(),
                        html.H4("Plot type"),
                        html.Br(),
                        dcc.Dropdown(
                            id = 'chart-widget',
                            value = "bar",
                            options = [{'label': t, 'value': t} for t in chart_tpye]
                        ),
                        html.Br(),
                        html.H4("Survey questions"),
                        dcc.Dropdown(
                            id = 'q-widget',
                            value = 'Q14',
                            options = [{'label': q, 'value': q} for q in qlist]
                        ),
                        html.Br(),
                        html.H4("Gender"),
                        dcc.Checklist(
                            id = 'gender-widget',
                            value = genderlist,
                            options = [{'label': gender, 'value': gender} for gender in genderlist]
                        ),
                        html.Br(),
                        html.H4("Age"),
                        dcc.Checklist(
                            id = 'age-widget',
                            value = agelist,
                            options = [{'label': age, 'value': age} for age in agelist]
                        ),
                        html.Br(),
                        html.H4("Company size"),
                        dcc.Checklist(
                            id = 'size-widget',
                            value = sizelist,
                            options = [{'label': size, 'value': size} for size in sizelist]
                        ),
                    ]
                )
            ], width=2),
                dbc.Col([
                    html.Iframe(
                        id = 'interactive',
                        style = {'border-width': '0', 'width': '100%', 'height': '400px'})
                ])
        ])
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


@app.callback(
    Output("interactive", "srcDoc"),
    inputs = dict(question = Input('q-widget', "value"),
                  chart_type = Input('chart-widget', "value"),
                  gender = Input('gender-widget', "value"),
                  age = Input('age-widget', "value"),
                  size = Input('size-widget', "value"))
)

def interactive(question, chart_type, gender, size, age):
    data = pd.read_csv("data/processed/survey.csv")
    data = data.drop(data[data["Q8"] == "Female"].index)
    df = data[data.Gender.isin(gender) &
              data.Q5.isin(size) &
              data.Age.isin(age)]
    
    df_pie = pd.DataFrame(df[question].value_counts())
    df_pie["Count"] = df_pie.iloc[:, 0].astype(int)
    df_pie["Pctg"] = round(df_pie .iloc[:, 0] / np.sum(df_pie.iloc[:, 0]) * 100, 2)
    df_pie["Answer"] = df_pie.index
    if chart_type == "bar":
        chart = alt.Chart(df).mark_bar().encode(
            alt.X("count():Q"),
            alt.Y(f"{question}:N", sort = "-x")
        )

        return chart.to_html()
    
    if chart_type == "pie":
        chart = alt.Chart(df_pie).mark_arc(outerRadius = 100).encode(
            theta = alt.Theta("Count:Q", stack = True), 
            color = alt.Color("Answer:N")
        )
        text = chart.mark_text(radius = 140, size = 20).encode(
            text = "Pctg:Q",
            color = "Answer"
        )
        chart = chart + text
        
        return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)