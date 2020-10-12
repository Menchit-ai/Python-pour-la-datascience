import plotly_express as px

import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def uniqueYear(dataf, yearname):
	return dataf[yearname].unique()

def createDataDic(dataf, yearname, years):
	return {year:dataf.query(yearname + " == @year") for year in years}

def createFig(data_dic, yearnumber, value1, value2, value3, value4):

	fig = px.scatter(data_dic[yearnumber], x=data_dic[yearnumber][value1], y=data_dic[yearnumber][value2], #data[input_value]
                        color=data_dic[yearnumber][value3], #size="pop",
                        hover_name=data_dic[yearnumber][value4])

	return fig

def dashBoard(dataf, years, fig, value1, value2, value3, value4):

	app = dash.Dash(__name__)

	app.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Graphe', children=[
                html.H1(children=f'Titre',   #{year}
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                dcc.Graph(
                    id='graph1',
                    figure=fig
                ), # (6)

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider",
                    min = years[0],
                    max = years[len(years)-1],
                    marks=[{years[i] : str(years[i])} for i in range(len(years))],
                    value=years[0],
                )
            ]),
        ])
    ])

    @app.callback(
    Output(component_id='graph1', component_property='figure'), # (1)
    [Input(component_id='year-slider', component_property='value')] # (2)
    )

    def update_figure(input_value): # (3)
        return px.scatter(dataf[input_value], x=dataf[input_value][value1], y=dataf[input_value][value2], #data[input_value]
                        color=dataf[input_value][value3], #size="pop",
                        hover_name=dataf[input_value][value4]) # (4)

    app.run_server(debug=True)




if __name__ == "__main__":

	yearsU = uniqueYear(df, "")
	dataDic = createDataDic(df, "", yearsU)
    
    fig = createFig(dataDic, )#Completer ici pour les params

    dashBoard(dataDic, yearsU, fig, )#Completer ici pour les params

