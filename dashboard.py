# filename = 'dash-01.py'

#
# Imports
#

import plotly_express as px

import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#
# Data
#

year = "2016-Q2"

gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

dataf = pd.read_csv("abo.csv",delimiter=',')
data_abo = dataf[(dataf["VAR"] == "BB-P100-TOT") | (dataf["VAR"] == "BB-P100-DSL")]
#data_abo2 = dataf[dataf["VAR"] == "BB-DATA-GB"]

#print(gapminder.head())
#print(data)

xvalue = data_abo[data_abo["VAR"] == "BB-P100-TOT"]
yvalue = data_abo[data_abo["VAR"] == "BB-P100-DSL"]

#print(xvalue.head())
#print(yvalue.head())

yearsA = xvalue["TIME"].unique()
yearsB = yvalue["TIME"].unique()

data_abo = { year:data_abo.query("TIME == @year") for year in yearsA}
xvalue = { year:xvalue.query("TIME == @year") for year in yearsA}
yvalue = { year:yvalue.query("TIME == @year") for year in yearsB}

#print(xvalue[year])
#print(yvalue[year])

#
# Main
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    @app.callback(
    Output(component_id='graph1', component_property='figure'), # (1)
    [Input(component_id='year-dropdown', component_property='value')] # (2)
    )

    def update_figure(input_value): # (3)
        return px.scatter(xvalue[input_value], x=xvalue[input_value]["Value"], y=yvalue[input_value]["Value"], #data[input_value]
                        color=xvalue[input_value]["Pays"], #size="pop",
                        hover_name=xvalue[input_value]["Pays"]) # (4)

    fig = px.scatter(xvalue[year], x=xvalue[year]["Value"], y=yvalue[year]["Value"], #data[input_value]
                        color=xvalue[year]["Pays"], #size="pop",
                        hover_name=xvalue[year]["Pays"])

    app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Graphe des pays', children=[
                html.H1(children=f'Total Abo entre 2016 et 2019',   #{year}
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                dcc.Graph(
                    id='graph1',
                    figure=fig
                ), # (6)

                html.Label('Year'),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{'label' : str(y), 'value' : str(y)} for y in yearsA],
                    value="2016",
                ),

                html.Div(children=f'''
                    The graph above shows relationship between life expectancy and
                    GDP per capita for year {year}. Each continent data has its own
                    colour and symbol size is proportionnal to country population.
                    Mouse over for details.
                '''), # (7)
            ]),
            dcc.Tab(label='Tab two', children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [1, 4, 1],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [1, 2, 3],
                            'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
            ]),
            dcc.Tab(label='Tab three', children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                            'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
            ]),
        ])
    ])

    #
    # RUN APP
    #

    app.run_server(debug=True) # (8)