import os
import subprocess
import sys

import requests

import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly.express as px
import folium
import geopandas
import json

import pycountry
import pycountry_convert as pc
import numpy as np
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import webbrowser

def init():
    """import all the packages needed in this script."""

    import os
    import subprocess
    import requests

    import pandas as pd
    import plotly.graph_objs as go
    import plotly
    import plotly.express as px
    import folium
    import geopandas
    import json

    import pycountry
    import pycountry_convert as pc
    import numpy as np
    import datetime

    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output

    import webbrowser

def downloader(urls):
    """Download all files from the urls in the folder data_world.

    Keyword arguments:
    urls -- list that contains all the urls that you have to download"""

    for url in urls:
        try:
            r = requests.get(url, allow_redirects=True)
            filename = getFilename_fromCd(r.headers.get('content-disposition'))
            open(r'.\data_world\\'+str(filename), 'wb').write(r.content)
        except expression as identifier:
            return False

    return True

def parseCSV(path=r".\data_world"):
    """Used to build 3 lists:
    -filesname : contains all the files' name
    -data : contains all the dataframes of the files in the folder
    -liDataCol : contains the interesting data columns' name of our dataframe

    Keyword arguments:
    path -- path to the folder that contains all the files to be transforme in dataframe (default : r"./data_world")"""
    
    if not path.endswith("\\"):
        path = path +"\\"
    filesName = os.listdir(path)
    pathFiles = [path + sub for sub in filesName]
    for fil in filesName:
        if not fil.endswith(".csv"):
            filesName.remove(fil)
            pathFiles.remove(fil)

    data = []
    liDataCol = []
    for i in range(len(pathFiles)):
        data.append(pd.read_csv(pathFiles[i],delimiter=","))
        liDataCol.append(str(data[i].columns[-1]))

    return (filesName,data,liDataCol)

def mergeData(names,liData,dataName1,dataName2,join):
    """Merged 2 dataframes on the given name, used an inner join :

    Keyword arguments:
    names -- list containing all files' name
    liData -- list containing all dataframes that are used
    dataName1 -- name of the firt dataframe to be merged
    dataName2 -- name of the second dataframe to be merged
    join -- name of the column to be used as join"""

    if not (dataName1 in names or dataName2 in names):
        raise NameError("These dataNames are not available in this list of dataframe")

    data1 = liData[names.index(dataName1)]
    data2 = liData[names.index(dataName2)]

    if not (set(join).issubset(data1.columns) or set(join).issubset(data2.columns)):
        raise NameError("Cannot join the dataframe, join name is absent from at least one of them")

    joinedData = data1.merge(data2, on=join, how='inner')

    return joinedData

def standardizeData(liData,model="basic"):
    """Transform dataframes and change it columns' name by using a scheme :

    Keyword arguments:
    liData -- list containing all the dataframes
    model -- contains the name of the columns to be used (default : "basic")"""


    stdData = []

    if model == "basic":
        scheme = ["Entity","Code","Year"]

        for data in liData:
            col = data.columns

            renamer = {}
            if not set(col).issubset(scheme):

                if not "Code" in col:
                    for c in range(len(col)):
                        if (isinstance(data[col[c]][0], str))  and  (len(data[col[c]][0]) == 3):
                            code = data[col[c]].apply(lambda x: pycountry.countries.get(alpha_3=x))
                            if code.isnull().sum().item() == 0:
                                renamer[col[c]] = "Code"
                                break

                if not "Entity" in col:
                    for c in range(len(col)):
                        if isinstance(data[col[c]][0], str):
                            code = data[col[c]].apply(lambda x: pycountry.countries.get(name=x))
                            if code.isnull().sum().item() < len(data[col[c]]) * 0.25: # estime que si 75% des entrées sont des pays, toutes le sont
                                renamer[col[c]] = "Entity"
                                break

                if not "Year" in col:
                    for c in range(len(col)):
                        if(isinstance(data[col[c]][0],datetime.datetime)):
                            renamer[col[c]] = "Year"
                            break
                        elif isinstance(data[col[c]][0], np.int64):
                            code = data[col[c]].apply(lambda x: 1900<x and x<datetime.datetime.now().year)
                            if code.sum() == len(code):
                                renamer[col[c]] = "Year"
                                break

            stdData.append(data.rename(columns = renamer))

    return stdData

def createFig(data_dic, yearnumber, x, y, coloured=None, hover=None):

    fig = px.scatter(data_dic[yearnumber], x=data_dic[yearnumber][x], y=data_dic[yearnumber][y], #data[input_value]
                        color=data_dic[yearnumber][coloured], #size="pop",
                        hover_name=data_dic[yearnumber][hover])

    return fig

def continent(data):
    """Create a new column in the dataframe that contains the continent corresponding to the country in the dataframe :

    Keyword arguments:
    data -- dataframe to be used"""

    alpha2 = data['Code'].apply(lambda x : pc.country_alpha3_to_country_alpha2(x))
    data['Continent'] = alpha2.apply(lambda x : pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(x)))
    return data

def map(data,year,dataName):
    """Generate a map in a "map.html" file, these map is worldwide and contains the values in the current dataframe :

    Keyword arguments:
    data -- dataframe to be used
    year -- year used to filter the data and use only this year
    dataName -- name of the column containing the values"""

    bins = list(data[dataName].quantile([0, 0.2, 0.4, 0.6, 0.8,1]))

    data = data[data['Year'] == year]
    world_json = json.load(open('./world.json'))

    m = folium.Map(location=[39, 2.333333], zoom_start=1.8)

    cho = folium.Choropleth(
    geo_data=world_json,
    name='choropleth',
    data=data,
    columns=['Code', dataName],
    key_on='feature.id',
    fill_color='GnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=dataName,
    bins=bins
    ).add_to(m)

    style_function = "font-size: 15px; font-weight: bold"
    cho.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False),
        folium.features.GeoJsonTooltip(['value'], style=style_function, labels=False))

    folium.LayerControl().add_to(m)

    m.save('map.html')
    return True

def uniqueYear(data, yearname='Year'):
    """Return a list containing all the unique years in the given dataframe :

    Keyword arguments:
    data -- dataframe to be used
    yearname -- name of the column containing the years (default : "Year")"""

    return data[yearname].unique()

def createDataDic(data, years, yearname="Year"):
    """Return a dictionnary containing all the years in the given dataframe associated with the data for each year:

    Keyword arguments:
    data -- dataframe to be used
    years -- list containing all the years to build the dictionnary with
    yearname -- name of the column containing the years (default : "Year")"""

    return {year:data.query(yearname + " == @year") for year in years}

def dashBoard(dataf, dataO, years, fig, filesName, datag, dataCol, coloured=None, hover=None, appl=None):
  #dashBoard(dico, data, diffyears, fig, filesName, datag, dataCol, 'Continent', 'Entity', appl=app)
    """Used to build the dashboard and run it

    Keyword arguments:
    dataf -- dictionnary containing year sorted data for the initializing dataframe
    dataO -- dataframe used to initialize the dashboard with it
    years -- list of all unique years in the initializing dataframe
    fig -- graph to plot with the initializing data
    filesName -- list containing all files' name
    datag -- list containing all dataframes
    dataCol -- list containing all data's column's name
    coloured -- what parameters used to colour graphics (default : None)
    hover -- what value to print when you look at specific point in the graphic (default : None)
    appl -- object containing the HTML part (default : None)
    """
    genI = 0
    datagen = datag[genI]
    diffyearsgen = uniqueYear(datagen, 'Year')
    diffyearsgen.sort()

    fileLabelGraph = [{'label' : y, 'value' : y} for y in filesName if not (y=="happiness-cantril-ladder.csv")]
    
    appl.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Graphe', children=[
                html.H1(id="TitreGraphe",
                        children=f'Life Satisfactiuon vs {dataCol[0]}',   #{year}
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                dcc.Graph(
                    id='graph',
                    figure=fig
                ),

                dcc.Dropdown(
                    id="variables_graph",
                    options=fileLabelGraph,
                    value= filesName[0]
                ),

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-graph",
                    min = 2000,
                    max = 2020,
                    step = 1,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )

            ]),

            dcc.Tab(label='Histogramme', children=[
                dcc.Graph(
                    id='histo',
                    figure=px.histogram(datagen[datagen['Year']==diffyearsgen[0]], x = dataCol[genI])
                ),

                dcc.Dropdown(
                    id="variables_histo",
                    options=[{'label' : y, 'value' : y} for y in filesName],
                    value= filesName[0]
                ),

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-histo",
                    min = 2000,
                    max = 2020,
                    step = 1,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )

                
            ]),

            dcc.Tab(label='Carte', children=[
                html.Iframe(id = 'map', srcDoc = open('map.html','r').read(), width = '100%', height = '600'),


                dcc.Dropdown(
                    id="variables_map",
                    options=[{'label' : y, 'value' : y} for y in filesName],
                    value= filesName[0]
                ),

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-map",
                    min = 2000,
                    max = 2020,
                    step = 1,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )

            ]),
        ])
    ])

    @appl.callback(
    [Output(component_id='graph', component_property='figure'),
     Output(component_id='year-slider-graph', component_property='marks'),
     Output(component_id='year-slider-graph', component_property='min'),
     Output(component_id='year-slider-graph', component_property='max'),
     Output(component_id='TitreGraphe', component_property='children')],
    [Input(component_id='year-slider-graph', component_property='value'),
     Input(component_id='variables_graph', component_property='value')]
    )

    def updateG(input_graph, fichcsv_graph):

        genI_g = filesName.index(fichcsv_graph)
        data_graph = datag[genI_g]
        datagen = mergeData(filesName, datag, "happiness-cantril-ladder.csv",filesName[genI_g],["Code","Year","Entity"])

        try:
            datagen = continent(datagen)
        except:
            pass

        diffyearsgen_g = uniqueYear(datagen, 'Year')
        diffyearsgen_g.sort()
        dico = createDataDic(datagen, diffyearsgen_g, 'Year')
        years_graph = uniqueYear(datagen)
        dico_graph = {int(i) : str(i) for i in years_graph}

        min_g = min(years_graph)
        if min_g < 1980:
            min_g = 1980
        max_g = max(years_graph)

        return (
                px.scatter(dico[input_graph], x=dico[input_graph][dataCol[filesName.index("happiness-cantril-ladder.csv")]], y=dico[input_graph][dataCol[genI_g]], #data[input_graph]
                        color=dico[input_graph][coloured],
                        hover_name=dico[input_graph][hover])
                ,
                dico_graph
                ,
                min_g
                ,
                max_g
                ,
                f'Life Satisfaction vs {dataCol[genI_g]}' #Pour rafraîchir le titre du graphe
        )

    @appl.callback(
    [Output(component_id='histo', component_property='figure'),
     Output(component_id='year-slider-histo', component_property='marks'),
     Output(component_id='year-slider-histo', component_property='min'),
     Output(component_id='year-slider-histo', component_property='max')],
    [Input(component_id='year-slider-histo', component_property='value'),
     Input(component_id='variables_histo', component_property='value')]
    )

    def updateH(input_histo, fichcsv_histo):

        genI_h = filesName.index(fichcsv_histo)
        data_histo = datag[genI_h]

        years_histo = uniqueYear(data_histo)
        dico_histo = {int(i) : str(i) for i in years_histo}

        min_h = min(years_histo)
        if min_h < 1980:
            min_h = 1980
        max_h = max(years_histo)

        return (
                px.histogram(data_histo[data_histo['Year']==input_histo], x = dataCol[genI_h])
                ,
                dico_histo
                ,
                min_h
                ,
                max_h
        )

    @appl.callback(
    [Output(component_id='map', component_property='srcDoc'),
     Output(component_id='year-slider-map', component_property='marks'),
     Output(component_id='year-slider-map', component_property='min'),
     Output(component_id='year-slider-map', component_property='max')],
    [Input(component_id='year-slider-map', component_property='value'),
     Input(component_id='variables_map', component_property='value')]
    )

    def updateM(input_map, fichcsv_map):

        genI_m = filesName.index(fichcsv_map)
        data_map = datag[genI_m]

        map(data_map,input_map,dataCol[genI_m])

        years_map = uniqueYear(data_map)
        dico_map = {int(i) : str(i) for i in years_map}

        min_m = min(years_map)
        if min_m < 1980:
            min_m = 1980
        max_m = max(years_map)

        return (
                open('map.html','r').read()
                ,
                dico_map
                ,
                min_m
                ,
                max_m
        )






