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
    import os

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

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def downloader(urls):
    # attend une liste d'urls
    for url in urls:
        r = requests.get(url, allow_redirects=True)
        filename = getFilename_fromCd(r.headers.get('content-disposition'))
        open(r'.\data_world\\'+str(filename), 'wb').write(r.content)
    return True

def parseCSV(path):
    if not path.endswith("\\"):
        path = path +"\\"
    filesName = os.listdir(path)
    pathFiles = [path + sub for sub in filesName]
    for fil in filesName:
        if not fil.endswith(".csv"):
            filesName.remove(fil)
            pathFiles.remove(fil)
    #donne la liste des tous les fichiers csv présent dans le répertoire indiqué par path

    data = []
    liDataCol = []
    for i in range(len(pathFiles)):
        data.append(pd.read_csv(pathFiles[i],delimiter=","))
        liDataCol.append(str(data[i].columns[-1]))
    #data est la liste des dataframes correpondant aux csv présent dans le répertoire
    #liDataCol = []
    #for d in data:
        #liDataCol.append(str(d.columns[-1]))
    #liDataCol est la liste contenant les noms des colonnes de chaque dataframe avec la donnée intéressante
    return (filesName,data,liDataCol)

def getDataCol(liData):
    liDataCol = []
    for data in liData:
        liDataCol.append(str(data.columns[-1]))
    return liDataCol

def mergeData(names,liData,dataName1,dataName2,join):
    
    if not (dataName1 in names or dataName2 in names):
        raise NameError("These dataNames are not available in this list of dataframe")

    data1 = liData[names.index(dataName1)]
    data2 = liData[names.index(dataName2)]

    if not (set(join).issubset(data1.columns) or set(join).issubset(data2.columns)):
        raise NameError("Cannot join the dataframe, join name is absent from at least one of them")

    joinedData = data1.merge(data2, on=join, how='inner')

    return joinedData

def correlation(data,value1,value2):
    data['Cor'] = data[value1]/data[value2]
    return data

def standardizeData(liData,model="basic"):
    # basic scheme : Entity,Code,Year,data

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

def continent(data):
    alpha2 = data['Code'].apply(lambda x : pc.country_alpha3_to_country_alpha2(x))
    data['Continent'] = alpha2.apply(lambda x : pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(x)))
    return data

def map(data,year,dataName):

    bins = list(data[dataName].quantile([0, 0.2, 0.4, 0.6, 0.8,1]))

    data = data[data['Year'] == year]
    world_json = json.load(open('./world.json'))

    

    # Initialize the map:
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
        folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False))

    folium.LayerControl().add_to(m)


    m.save('map.html')

###############################################################################################################    

def uniqueYear(dataf, yearname='Year'):
    return dataf[yearname].unique()

def createDataDic(dataf, yearname, years):
    return {year:dataf.query(yearname + " == @year") for year in years}

def createFig(data_dic, yearnumber, x, y, coloured=None, hover=None):

    fig = px.scatter(data_dic[yearnumber], x=data_dic[yearnumber][x], y=data_dic[yearnumber][y], #data[input_value]
                        color=data_dic[yearnumber][coloured], #size="pop",
                        hover_name=data_dic[yearnumber][hover])

    return fig

def dashBoard(dataf, dataO, years, fig, filesName, datag, dataCol, coloured=None, hover=None, appl=None):

    genI = 0
    datagen = datag[genI]
    # datagen = mergeData(filesName, datag, filesName[0],"life-expectancy.csv",["Code","Year","Entity"])
    #datagen = continent(datagen)
    diffyearsgen = uniqueYear(datagen, 'Year')
    diffyearsgen.sort()
    #print(diffyearsgen)
    #print(datagen[datagen['Year']==diffyearsgen[0]])

    fileLabelGraph = [{'label' : y, 'value' : y} for y in filesName if not (y=="happiness-cantril-ladder.csv")]
    
    appl.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Graphe', children=[
                html.H1(children=f'Titre',   #{year}
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                dcc.Graph(
                    id='graph',
                    figure=fig
                ), # (6)

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
     Output(component_id='histo', component_property='figure'),
     Output(component_id='map', component_property='srcDoc'),
     Output(component_id='year-slider-graph', component_property='marks'),
     Output(component_id='year-slider-histo', component_property='marks'),
     Output(component_id='year-slider-map', component_property='marks'),
     Output(component_id='year-slider-graph', component_property='min'),
     Output(component_id='year-slider-histo', component_property='min'),
     Output(component_id='year-slider-map', component_property='min'),
     Output(component_id='year-slider-graph', component_property='max'),
     Output(component_id='year-slider-histo', component_property='max'),
     Output(component_id='year-slider-map', component_property='max')],
      # (1)
    [Input(component_id='year-slider-graph', component_property='value'),
     Input(component_id='year-slider-histo', component_property='value'),
     Input(component_id='year-slider-map', component_property='value'),
     Input(component_id='variables_graph', component_property='value'),
     Input(component_id='variables_histo', component_property='value'),
     Input(component_id='variables_map', component_property='value')] # (2)
    )

    def update(input_graph,input_histo,input_map, fichcsv_graph, fichcsv_histo, fichcsv_map): # (3)
        
        genI_h = filesName.index(fichcsv_histo)
        genI_m = filesName.index(fichcsv_map)
        genI_g = filesName.index(fichcsv_graph)

        data_graph = datag[genI_g]
        data_histo = datag[genI_h]
        data_map   = datag[genI_m]

        map(data_map,input_map,dataCol[genI_m])
        
        datagen = mergeData(filesName, datag, "happiness-cantril-ladder.csv",filesName[genI_g],["Code","Year","Entity"])


        try:
            datagen = continent(datagen)
        except:
            pass

        diffyearsgen_g = uniqueYear(datagen, 'Year')
        diffyearsgen_g.sort()
        dico = createDataDic(datagen, 'Year', diffyearsgen_g)

        diffyearsgen = uniqueYear(data_histo, 'Year')
        diffyearsgen.sort()

        years_graph = uniqueYear(datagen)
        years_histo = uniqueYear(data_histo)
        years_map = uniqueYear(data_map)

        mm_graph = (years_graph[0],years_graph[-1])
        mm_histo = (years_histo[0],years_histo[-1])
        mm_map = (years_map[0],years_map[-1])

        dico_graph = {int(i) : str(i) for i in years_graph}
        dico_histo = {int(i) : str(i) for i in years_histo}
        dico_map = {int(i) : str(i) for i in years_map}

        min_g = min(years_graph)
        min_h = min(years_histo)
        min_m = min(years_map)

        if min_g < 1980:
            min_g = 1980
        if min_h < 1980:
            min_h = 1980
        if min_m < 1980:
            min_m = 1980

        max_g = max(years_graph)
        max_h = max(years_histo)
        max_m = max(years_map)

        return (
                px.scatter(dico[input_graph], x=dico[input_graph][dataCol[filesName.index("happiness-cantril-ladder.csv")]], y=dico[input_graph][dataCol[genI_g]], #data[input_graph]
                        color=dico[input_graph]['Continent'], #size="pop",
                        hover_name=dico[input_graph][hover])
                ,
                px.histogram(data_histo[data_histo['Year']==input_histo], x = dataCol[genI_h])
                ,
                open('map.html','r').read()
                ,
                dico_graph
                ,
                dico_histo
                ,
                dico_map
                ,
                min_g
                ,
                min_h
                ,
                min_m
                ,
                max_g
                ,
                max_h
                ,
                max_m
        )


###############################################################################################################
