import pandas as pd
import altair as alt
import numpy as np

import json
from vega_datasets import data as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from urllib.request import urlopen

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

server = app.server

logo = "https://cdn-icons-png.flaticon.com/512/2017/2017231.png"
data = pd.read_csv("data/processed/survey.csv")


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
                    ],color='lightskyblue'),
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
    
qdict = {"Q11":"Does your employer provide resources to learn more about mental health issues and how to seek help?",
"Q12":"Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?",
"Q13":"How easy is it for you to take medical leave for a mental health condition?",
"Q14":"Do you think that discussing a mental health issue with your employer would have negative consequences?",
"Q15":"Do you think that discussing a physical health issue with your employer would have negative consequences?",
"Q16":"Would you be willing to discuss a mental health issue with your coworkers?",
"Q17":"Would you be willing to discuss a mental health issue with your direct supervisor(s)?",
"Q18":"Would you bring up a mental health issue with a potential employer in an interview?",
"Q19":"Would you bring up a physical health issue with a potential employer in an interview?",
"Q20":"Do you feel that your employer takes mental health as seriously as physical health?",
"Q21":"Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?"}  
        
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
                                    value = list(qdict.keys())[0],
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
                            style = {'border-width': '500', 'width': '100%', 'height': '500px'}
                        )
                        ], style={"width": "90%","height": "100%"}),
                        ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                    ]),
                ])
            ])

    return layout
    
    
fnameDict = {
    "Q11":["Yes","No","Dont' know"],
    "Q12":["Yes","No","Dont' know"],
    "Q13":["Very difficult","Somewhat difficult","Somewhat easy","Very easy","Dont' know"],
    "Q14":["Yes","No","Maybe"],
    "Q15":["Yes","No","Maybe"],
    "Q16":["Yes","No","Some of them"],
    "Q17":["Yes","No","Some of them"],
    "Q18":["Yes","No","Maybe"],
    "Q19":["Yes","No","Maybe"],
    "Q20":["Yes","No","Dont' know"],
    "Q21":["Yes","No"]
}  

names = list(fnameDict.keys())


def tab3():
    """Layout structure for Interactive View"""
    layout = html.Div([
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Toast([
                        html.H1(children="Mental Health in Tech Dashboard"), 
                        html.Br(),
                            html.P([
                                html.Br(),
                                html.H4("Survey questions"),
                                dcc.Dropdown(
                                    id = 'map_q-widget',
                                    value = list(qdict.keys())[0],
                                    options = [{'label': q, 'value': p} for p, q in qdict.items()],
                                    optionHeight = 100),
                                html.Br(),
                                html.H4("Response"),
                                dcc.Dropdown(
                                    id = 'answer-widget',
                                    #value = list(fnameDict.values())[0],
                                    ),
                            ]),
                        ]),
                ], width=5,style={'margin-right': '0px', 'margin-left': '20px'}),
                dbc.Col([
                    dbc.Toast([
                        html.Iframe(
                            id = 'interactive_map',
                            style = {'border-width': '500', 'width': '100%', 'height': '500px'}
                        )
                        ], style={"width": "90%","height": "100%"}),
                        ],className="chart-box",style={'margin-right': '0px', 'margin-left': '0px'}),
                    ]),
                ])
            ])
    
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
    Output("interactive", component_property='srcDoc'),
    inputs = dict(question = Input('q-widget', "value"),
                  chart_type = Input('chart-widget', "value"),
                  gender = Input('gender-widget', "value"),
                  age = Input('age-widget', "value"),
                  size = Input('size-widget', "value"))
)

def interactive(question, chart_type, gender, size, age):
    qdict = {"Q11":"Does your employer provide resources to learn more about mental health issues and how to seek help?",
    "Q12":"Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources?",
    "Q13":"How easy is it for you to take medical leave for a mental health condition?",
    "Q14":"Do you think that discussing a mental health issue with your employer would have negative consequences?",
    "Q15":"Do you think that discussing a physical health issue with your employer would have negative consequences?",
    "Q16":"Would you be willing to discuss a mental health issue with your coworkers?",
    "Q17":"Would you be willing to discuss a mental health issue with your direct supervisor(s)?",
    "Q18":"Would you bring up a mental health issue with a potential employer in an interview?",
    "Q19":"Would you bring up a physical health issue with a potential employer in an interview?",
    "Q20":"Do you feel that your employer takes mental health as seriously as physical health?",
    "Q21":"Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace?"}   

    df_p = data[data.Gender.isin(gender) &
          data.Q5.isin(size) &
          data.Age.isin(age)]
   
    title = qdict[question]
    titlesplit = title.split(" ")
    title_n = len(titlesplit)//3
    title = ' '.join(titlesplit[:title_n]) + " <br> " + ' '.join(titlesplit[title_n:-title_n]) + " <br> " + ' '.join(titlesplit[-title_n:])
    
   
    if chart_type == "Bar":
        order = ["Yes", "No", "Maybe"]
        fig = bar_chart(df_p, question, orientation="v", title=title, order=order)
        return fig.to_html()
    
    if chart_type == "Pie":       
        fig = pie_chart(df_p, question, colors=['skyblue','navy','lightgray'], title=title)        
        return fig.to_html()

  
@app.callback(
    Output('answer-widget', 'options'),
    [Input('map_q-widget', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]]

@app.callback(
    Output("interactive_map", component_property='srcDoc'),
    inputs = dict(map_question = Input('map_q-widget', "value"),
                  answer = Input('answer-widget', "value"))
)


def interactive_map(map_question, answer):
    us_states = pd.DataFrame({'name':['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','NewJersey','NewMexico','NewYork','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','RhodeIsland','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],
    'state':['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']}).set_index("state")

    country = 'United States'
    data_us = data[data.Country == country]

    if type(answer) == str:
        answer=[answer]

    if answer is None:
        answer = ["Yes","Very difficult"]
        answer = [data_us[data_us[map_question].isin(answer)][map_question][0]]

    response = pd.DataFrame(data_us[data_us[map_question].isin(answer)].groupby('state')[map_question].agg("count"))
    response = response.rename(columns={map_question: "response"})
    
    base = pd.DataFrame(data_us.groupby('state')[map_question].agg("count"))
    base = base.rename(columns={map_question: "base"})

    data_map = pd.merge(
        response,
        base,
        how="right",
        left_index=True,
        right_index=True,).fillna(0)

    data_map["Percent"] = data_map['response'] / data_map['base'] * 100.0
    data_map = pd.merge(
        data_map,
        us_states,
        how="left",
        left_index=True,
        right_index=True)
    
    data_map = data_map.replace(0.0, np.NaN)
    
    title = qdict[map_question]
    titlesplit = title.split(" ")
    title_n = len(titlesplit)//2
    title = ' '.join(titlesplit[:title_n]) + " <br> " + ' '.join(titlesplit[-title_n:])
    title = '<b>' + title + '</b> <br> (' + ', '.join(answer) + ')'
    
    fig = go.Figure(data=go.Choropleth(locations=data_map.index,z = data_map['Percent'],locationmode = 'USA-states',colorscale = 'Reds',colorbar_title = "Percent",))
    fig.update_layout(title=f'{title}', title_x=0.5)
    fig.update_layout(margin=dict(l=20, r=20, t=100, b=50),#, width = 800, height = 800,
                      geo_scope='usa')
    return fig.to_html()
    

if __name__ == '__main__':
    app.run_server(debug=True)