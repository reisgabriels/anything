##Imports
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash import html, dcc
from plotly import graph_objects as go
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template

load_figure_template('minty')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
##Dados

df = pd.read_csv('Projeto 1 - Supermarket Sales/supermarket_sales.csv',parse_dates=['Date'])
#pd.read_csv('supermarket_sales.csv',parse_dates=['Date'])
##app = dash.Dash()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


##app.layout = []

app.layout = html.Div([
#1ª Coluna
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H3('ASIMOV'),
                        html.Hr(),
                        html.H6('Cidades:'),
                        dcc.Checklist(id = 'cities', options=list(set(df['City'])),value=list(set(df['City'])), inputStyle={'margin-right':'5px','margin-left':'20px'}),
                        html.H5('Variável de Análise:',style={'margin-top':'50px'}),
                        dcc.RadioItems(['gross income','Rating'],'gross income',id = 'visao', inputStyle={'margin-right':'5px','margin-left':'20px'})
                    ], style={'height':'90vh','margin':'10px','padding':'20px'})
                ], md = 2),
                
                dbc.Col([ 
                    dbc.Row([
                        dbc.Col(html.Div([dcc.Graph(id = 'graph1')]), md = 4),
                        dbc.Col(html.Div([dcc.Graph(id = 'graph2')]), md = 4),
                        dbc.Col(html.Div([dcc.Graph(id = 'graph3')]), md = 4)
                    ]),
                    dbc.Row(dbc.Col(html.Div([dcc.Graph(id = 'graph5')]), md = 12)),
                    dbc.Row(dbc.Col(html.Div([dcc.Graph(id = 'graph4')]), md = 12))
                ], md = 10),
            ])            
        ])
])

##Callbacks
@app.callback([
        Output('graph1','figure'),
        Output('graph2','figure'),
        Output('graph3','figure'),
        Output('graph4','figure'),
        Output('graph5','figure')
    ],
    [
        Input('cities', 'value'),
        Input('visao', 'value'),
    ])
def render_graphs(cities,visao):
    operation = np.sum if visao == 'gross income' else np.mean
    df_filtered = df[df['City'].isin(cities)]
    df_city = df_filtered.groupby('City')[visao].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[visao].apply(operation).to_frame().reset_index()
    df_pline = df_filtered.groupby(['Product line','City'])[visao].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(['Gender','City'])[visao].apply(operation).to_frame().reset_index()
    df_date = df_filtered.groupby('Date')[visao].apply(operation).to_frame().reset_index().sort_values('Date')
    
    graph1 = px.bar(df_city,x='City',y=visao)
    graph2 = px.bar(df_gender,x='Gender',y=visao,color='City',barmode='group')
    graph3 = px.bar(df_payment,y='Payment',x=visao)
    graph4 = px.bar(df_pline,y='Product line',x=visao, color='City')
    graph5 = px.bar(df_date,x='Date',y=visao)
    
    for graph in [graph1,graph2,graph3,graph5]:
        graph.update_layout(margin = dict(l = 0, r = 0, t = 20, b = 30), height = 200, template = 'minty')
    graph4.update_layout(margin = dict(l = 0, r = 0, t = 20, b = 30), height = 200)
    
    
    return graph1,graph2,graph3,graph4,graph5


#app.run_server()

if __name__ == '__main__':
    app.run_server(debug='False',port=8080)