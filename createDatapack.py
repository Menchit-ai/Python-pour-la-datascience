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
    for fil in pathFiles:
        data.append(pd.read_csv(fil,delimiter=","))
    #data est la liste des dataframes correpondant aux csv présent dans le répertoire
    liDataCol = []
    for d in data:
        liDataCol.append(str(d.columns[-1]))
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
    legend_name=dataName
    ).add_to(m)

    style_function = "font-size: 15px; font-weight: bold"
    cho.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], style=style_function, labels=False))

    folium.LayerControl().add_to(m)


    m.save('map.html')

###############################################################################################################    

def uniqueYear(dataf, yearname):
    return dataf[yearname].unique()

def createDataDic(dataf, yearname, years):
    return {year:dataf.query(yearname + " == @year") for year in years}

def createFig(data_dic, yearnumber, x, y, coloured=None, hover=None):

    fig = px.scatter(data_dic[yearnumber], x=data_dic[yearnumber][x], y=data_dic[yearnumber][y], #data[input_value]
                        color=data_dic[yearnumber][coloured], #size="pop",
                        hover_name=data_dic[yearnumber][hover])

    return fig

def dashBoard(dataf, dataO, years, fig, x, y, coloured=None, hover=None, appl=None):
    
    appl.layout = html.Div([
        dcc.Tabs([
            dcc.Tab(label='Graphe', children=[
                html.H1(children=f'Titre',   #{year}
                                style={'textAlign': 'center', 'color': '#7FDBFF'}), # (5)

                dcc.Graph(
                    id='graph',
                    figure=fig
                ), # (6)

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-graph",
                    min = years[0],
                    max = years[len(years)-1],
                    step = None,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )
            ]),

            dcc.Tab(label='Histogramme', children=[
                dcc.Graph(
                    id='histo',
                    figure=px.histogram(dataO, x = dataO[y])
                ),
                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-histo",
                    min = years[0],
                    max = years[len(years)-1],
                    step = None,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )

                #dcc.RadioItems(
                #    id="variables",
                #    options=[{'label' : str(y), 'value' : str(y)} for y in variables],
                #    value='BB-P100-TOT'
                #)
            ]),

            dcc.Tab(label='Carte', children=[
                html.Iframe(id = 'map', srcDoc = open('map.html','r').read(), width = '100%', height = '600'),
                # dcc.Graph(
                #     #id = 'map',
                #     figure = map(pd.read_csv('./data_world/happiness-cantril-ladder.csv'),2012,x)
                # ),

                html.Label('Year'),
                dcc.Slider(
                    id="year-slider-map",
                    min = years[0],
                    max = years[len(years)-1],
                    step = None,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )
            ]),
        ])
    ])
    
    @appl.callback(
    [Output(component_id='graph', component_property='figure'),
     Output(component_id='histo', component_property='figure'),
     Output(component_id='map', component_property='srcDoc')], # (1)
    [Input(component_id='year-slider-graph', component_property='value'),
     Input(component_id='year-slider-histo', component_property='value'),
     Input(component_id='year-slider-map', component_property='value')] # (2)
    )

    def update(input_graph,input_histo,input_map): # (3)
        map(dataO,input_map,y)
        return (
                px.scatter(dataf[input_graph], x=dataf[input_graph][x], y=dataf[input_graph][y], #data[input_graph]
                        color=dataf[input_graph][coloured], #size="pop",
                        hover_name=dataf[input_graph][hover])
                ,
                px.histogram(dataO[dataO['Year']==input_histo], x = dataO[y])
                ,
                open('map.html','r').read()
        )


###############################################################################################################


if __name__ == "__main__":
    
    filesName,data,dataCol = parseCSV(r".\data_world")

    try:
        data = mergeData(filesName,data,"happiness-cantril-ladder.csv","human-development-index.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()


    data.to_csv(r".\data_world\AAAfichier-test.csv",sep=",")

    print("colonnes de base :"+ str(data.columns))
    print()
    data = data.rename(columns = {'Code':'ccc','Entity':'eee','Year':'yyy'})
    print("colonnes renommées :"+ str(data.columns))
    print()
    l = standardizeData([data])
    data = l[0]
    print("colonnes standardes :"+ str(data.columns))

