import pandas as pd
import altair as alt
import numpy as np

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from vega_datasets import data as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server


logo = "https://cdn-icons-png.flaticon.com/512/2017/2017231.png"
data = pd.read_csv("data/processed/survey.csv")
data_ref = pd.read_csv("data/processed/survey_column.csv")
us_state = pd.read_csv("src/assets/US_States.csv")

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


# data wrangling for map view
surv_data = data.loc[data['Country'] == "United States"]
surv_data.dropna(subset = ["state"], inplace=True)
surv_data['state_id'] = surv_data['state'].map(state_id_dict).fillna(surv_data['state'])
surv_data_grouped = surv_data.groupby(['state', 'state_id'], as_index=False)['Q3'].value_counts(normalize=True)
surv_data_grouped = pd.DataFrame(surv_data_grouped)
surv_data_grouped = surv_data_grouped.loc[surv_data_grouped['Q3'] == 'Yes']


def pie_chart(df, col, colors=None, title=None):
    """Create Pie Chart"""
    df_p = pd.DataFrame(df.groupby(col)[col].agg("count") / len(df))
    if title == None:
        title = col
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=df_p.index, values=df_p.iloc[:,0]))
    if colors == None:
        fig.update_traces(hoverinfo='label+percent', textinfo='label+percent')
    else:
        fig.update_traces(hoverinfo='label+percent', textinfo='label+percent',
                  marker=dict(colors=colors))
        
    fig.update_layout(title=f'<b>{title}</b>', title_x=0.5,)
    fig.update_layout(
    margin=dict(l=20, r=20, t=100, b=50)
    )
    return fig


def bar_chart(df, col, orientation="h", title=None, order=None):
    """Create Bar Chart"""
    df_p = pd.DataFrame(df.groupby(col)[col].agg("count") / len(df))
    if order != None:
        df_p = df_p.reindex(index = order)
        df_p = df_p.dropna()

    if title == None:
        title = col

    x=df_p.index.tolist()
    y=df_p[[col]].values.flatten().tolist()

    if orientation == "h":
        fig = go.Figure(go.Bar(x=y, y=x,orientation=orientation))
        fig.update_yaxes(title=None)
        fig.update_xaxes(title="Percentage of Respondent (%)", tickformat=".0%")

    if orientation == "v":
        x=df_p.index.tolist()
        y=df_p[[col]].values.flatten().tolist()
        fig = go.Figure(go.Bar(x=x, y=y,orientation=orientation))
        fig.update_xaxes(title=None)
        fig.update_yaxes(title="Percentage of Respondent (%)", tickformat=".0%")

    fig.update_traces(marker_color='lightskyblue')
    fig.update_layout(title=f'<b>{title}</b>', title_x=0.5)#, autosize=True)
    fig.update_layout(
    margin=dict(l=20, r=20, t=100, b=50)
    )
    
    return fig


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
    """Summary Overview"""
    # pie plot for gender    
    colors = ['pink','lightskyblue','lightgray']
    pg = pie_chart(data,col="Gender",colors=colors)

    # bar plot for size
    order = ["1-5", "6-25", "26-100", "100-500","500-1000","More than 1000"]
    title = "Company Size (Number of Employee)"
    bar_size = bar_chart(data,"Q5",title=title,order=order)
    
    # bar plot for age
    bar_age = bar_chart(data,"Age", orientation="v")
    
    # pie plot for benefit
    title = "Percentage whose knowledge about their <br> company's offer for mental health benefits"
    colors = ['skyblue','navy','lightgray']
    pb = pie_chart(data,col="Q8",title=title,colors=colors)
    
    
    layout = html.Div([
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Toast([
                        html.H1(children="Mental Health in Tech Dashboard"), 
                        html.Br(),
                        html.P([
                                html.H2("Introduction"),
                                html.Br(),
                                html.P("In this dashboard we want explore the attitude towards mental health in tech companies. We assume that the gender, age, company size, whether the company provides mental health benefits are likely to be correlated with our research question. We also explore the geographical distribution of respondents."),
                                html.Br(),
                                html.H3("Data Source"),
                                html.P("The data set used in this dashboard is from the link below "),
                                dcc.Link(
                                href="https://www.kaggle.com/osmi/mental-health-in-tech-2016",
                                title="Data set")
                            ]),
                    ]),
                ], width=3,style={'margin-right': '0px', 'margin-left': '20px'}),
                dbc.Col([            
                    dbc.Row([
                             dbc.Col([
                                dbc.Toast([
                                    dcc.Graph(id="pg", figure=pg),
                                    ], style={"width": "90%","height": "100%"}),
                                ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                             dbc.Col([
                                dbc.Toast([
                                    dcc.Graph(id="bar_age", figure=bar_age),
                                    ], style={"width": "90%","height": "100%"}),
                                ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                            ]),
                    dbc.Row([    
                             dbc.Col([
                                dbc.Toast([
                                    dcc.Graph(id="bar_size", figure=bar_size),
                                    ], style={"width": "90%","height": "100%"}),
                               ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                             dbc.Col([
                                dbc.Toast([
                                    dcc.Graph(id="pb", figure=pb),
                                    ], style={"width": "90%","height": "100%"}),
                               ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                            ]),
                    ]),
                ]),
        ],fluid=True)
    ])
    return layout
    
qdict = {"Q14": "Do you think that discussing a mental health issue with your employer would have negative consequences?",
         "Q15": "Do you think that discussing a physical health issue with your employer would have negative consequences?",
         "Q21": "Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?"}    
def tab2():
    """Layout structure for Interactive View"""
    chart_tpye = ["Bar", "Pie"]
    genderlist = ["Male", "Female", "Other"]
    sizelist = ["1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"]
    agelist = ["18-24", "25-34", "35-44", "45-54", "55+"]

    layout = html.Div([
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Toast([
                        html.H1(children="Mental Health in Tech Dashboard"), 
                        html.Br(),
                            html.P([
                                html.H4("Plot type"),
                                html.Br(),
                                dcc.Dropdown(
                                    id = 'chart-widget',
                                    value = "Bar",
                                    options = [{'label': t, 'value': t} for t in chart_tpye]),
                                html.Br(),
                                html.H4("Survey questions"),
                                dcc.Dropdown(
                                    id = 'q-widget',
                                    value = 'Q14',
                                    options = [{'label': q, 'value': p} for p, q in qdict.items()],
                                    optionHeight = 100),
                                html.Br(),
                                html.H4("Gender"),
                                dcc.Dropdown(
                                    id = 'gender-widget',
                                    value = genderlist,
                                    options = [{'label': gender, 'value': gender} for gender in genderlist],
                                    multi = True),
                                html.Br(),
                                html.H4("Age"),
                                dcc.Dropdown(
                                    id = 'age-widget',
                                    value = agelist,
                                    options = [{'label': age, 'value': age} for age in agelist],
                                    multi = True),
                                html.Br(),
                                html.H4("Company size"),
                                dcc.Dropdown(
                                    id = 'size-widget',
                                    value = sizelist,
                                    options = [{'label': size, 'value': size} for size in sizelist],
                                    multi = True),
                            ]),
                        ]),
                ], width=5,style={'margin-right': '0px', 'margin-left': '20px'}),
                dbc.Col([
                    dbc.Toast([
                        html.Iframe(
                            id = 'interactive',
                            style = {'border-width': '500', 'width': '100%', 'height': '800px'}
                        )
                        #dcc.Graph(id="interactive"),
                        ], style={"width": "90%","height": "100%"}),
                        ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                    ]),
                ])
            ])

    return layout
    
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

    layout = html.Div([
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Toast([
                    html.H1(children="Mental Health in Tech Dashboard"), 
                    html.Br(),
                    html.P([
                            html.H3("Controls"),
                        ]),
                    ])
                ], width=3,style={'margin-right': '0px', 'margin-left': '20px'}),
                dbc.Col([
                    dbc.Toast([
                            html.Iframe(
                                id = 'chloropleth',
                                srcDoc = chloropleth.to_html(),
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                            )
                    ])
                ])
            ])
        ]
    )
    
    return layout

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
    color="lightskyblue",
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
    df_p = data[data.Gender.isin(gender) &
          data.Q5.isin(size) &
          data.Age.isin(age)]

    qdict = {"Q14": "Do you think: discussing a mental health issue <br> with your employer would have <br> negative consequences?",
         "Q15": "Do you think that discussing a physical health issue <br> with your employer would have negative consequences?",
         "Q21": "Have you heard of or observed negative consequences <br> for coworkers with mental health <br> conditions in your workplace?"}    

    if chart_type == "Bar":
        order = ["Yes", "No", "Maybe"]
        fig = bar_chart(df_p, question, orientation="v", title=qdict[question], order=order)
        return fig.to_html()
    
    if chart_type == "Pie":       
        fig = pie_chart(df_p, question, colors=['skyblue','navy','lightgray'], title=qdict[question])        
        return fig.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)