import pandas as pd
import altair as alt
import numpy as np

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from vega_datasets import data as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

data = pd.read_csv("data/processed/survey.csv")
data = data.drop(index = data[data["Q14"] == "Female"].index)
logo = "https://cdn-icons-png.flaticon.com/512/2017/2017231.png"

# static sources needed for map plot
source = dt.unemployment.url
states = alt.topo_feature(dt.us_10m.url, 'states')
us_state_abbrev = {
'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

state_id_dict = {'AL': 1, 'AK': 2, 'AZ': 4, 'AR': 5, 'CA': 6, 'CO': 8, 'CT': 9, 'DE': 10,
    'DC': 11, 'FL': 12, 'GA': 13, 'HI': 15, 'ID': 16, 'IL': 17, 'IN': 18, 'IA': 19, 'KS': 20,
    'KY': 21, 'LA': 22, 'ME': 23, 'MD': 24, 'MA': 25, 'MI': 26, 'MN': 27, 'MS': 28, 'MO': 29,
    'MT': 30, 'NE': 31, 'NV': 32, 'NH': 33, 'NJ': 34, 'NM': 35, 'NY': 36, 'NC': 37, 'ND': 38,
    'OH': 39, 'OK': 40, 'OR': 41, 'PA': 42, 'RI': 44, 'SC': 45, 'SD': 46, 'TN': 47, 'TX': 48,
    'UT': 49, 'VT': 50, 'VA': 51, 'WA': 53, 'WV': 54, 'WI': 55, 'WY': 56, 'PR': 72}

# data wrangling for plots

# create employer size df
size = data.copy()

# create gender count and percentage df
gender = data.copy()
gender[gender["Gender"] == "Woman"] = "Female"
gender[gender["Gender"] == "woman"] = "Female"

gender = pd.DataFrame(gender["Gender"].value_counts())

gender["Gender"] = gender["Gender"].astype(int)
gender["Pctg"] = round((gender["Gender"] / np.sum(gender["Gender"]))*100, 2)
gender["Count"] = gender["Gender"]
gender["Gender"] = gender.index

# create age df
age = data.copy()

# create benefit count and percentage df
benefit = data.copy()
benefit = pd.DataFrame(data["Q8"].value_counts())

benefit["Benefit"] = benefit["Q8"].astype(int)
benefit["Pctg"] = round((benefit["Benefit"] / np.sum(benefit["Benefit"]))*100, 2)
benefit["Count"] = benefit["Q8"]
benefit["Answer"] = benefit.index

# data wrangling for map view
surv_data = data.loc[data['Country'] == "United States"]
surv_data.dropna(subset = ["state"], inplace=True)
surv_data['state_id'] = surv_data['state'].map(state_id_dict).fillna(surv_data['state'])
surv_data_grouped = surv_data.groupby(['state', 'state_id'], as_index=False)['Q3'].value_counts(normalize=True)
surv_data_grouped = pd.DataFrame(surv_data_grouped)
surv_data_grouped = surv_data_grouped.loc[surv_data_grouped['Q3'] == 'Yes']


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
                        html.H3("Introduction"),
                        html.Br(),
                        html.P("In this dashboard we want explore the attitude towards mental health in tech companies. We assume that the gender, age, company size, whether the company provides mental health benefits are likely to be correlated with our research question. We also explore the geographical distribution of respondents."),
                        html.Br(),
                        html.H3("Data Source"),
                        html.P("The data set used in this dashboard is from the link below "),
                        dcc.Link(
                            href="https://www.kaggle.com/osmi/mental-health-in-tech-2016",
                            title="Data set"
                        )            
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
qdict = {"Q14": "Do you think that discussing a mental health issue with your employer would have negative consequences?",
    "Q15": "Do you think that discussing a physical health issue with your employer would have negative consequences?",
    "Q21": "Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?"}    
def tab2():
    """Layout structure for Interactive View"""
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
                            options = [{'label': q, 'value': p} for p, q in qdict.items()],
                            optionHeight = 100
                        ),
                        html.Br(),
                        html.H4("Gender"),
                        dcc.Dropdown(
                            id = 'gender-widget',
                            value = genderlist,
                            options = [{'label': gender, 'value': gender} for gender in genderlist],
                            multi = True
                        ),
                        html.Br(),
                        html.H4("Age"),
                        dcc.Dropdown(
                            id = 'age-widget',
                            value = agelist,
                            options = [{'label': age, 'value': age} for age in agelist],
                            multi = True
                        ),
                        html.Br(),
                        html.H4("Company size"),
                        dcc.Dropdown(
                            id = 'size-widget',
                            value = sizelist,
                            options = [{'label': size, 'value': size} for size in sizelist],
                            multi = True
                        ),
                    ]
                )
            ], width=3),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Iframe(
                        id = 'interactive',
                        style = {'border-width': '500', 'width': '200%', 'height': '800px'})
                ])
        ])
        ]
    )
    
    return interactive_view
    
def tab3():
    """Layout structure for Map View"""

    chloropleth = alt.Chart(states).mark_geoshape().encode(
        color='proportion:Q',
        tooltip=['state:N', 'proportion:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(surv_data_grouped, 'state_id', ['state', 'proportion'])
    ).project(
        type='albersUsa'
    ).properties(
        width=500,
        height=300,
        title="Proportion of Those who have Seeked Mental Health Help by State"
    )

    map_view = html.Div(
        [
            dbc.Row([
                dbc.Col([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P(
                        children=[
                            html.H3("Controls"),
                        ]
                    )
                ], width=2),
                dbc.Col([
                        html.Iframe(
                            id = 'chloropleth',
                            srcDoc = chloropleth.to_html(),
                            style={'border-width': '0', 'width': '100%', 'height': '400px'}
                        )
                    ])
            ])
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
        ).properties(
        title=qdict[question]
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
        ).properties(
        width=500,
        height=300,
        title=question
    )

        chart = chart + text
        
        return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)