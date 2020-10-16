import os

import requests

import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly.express as px

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

    # joinedData["Continent"]=

    return joinedData

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
                        if isinstance(data[col[c]][0], np.int64):
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

<<<<<<< HEAD
def dashBoard(dataf,dataO, years, fig, x, y, coloured=None, hover=None, appl=None):
=======
def dashBoard(dataf, dataO, years, fig, x, y, coloured=None, hover=None, appl=None):
>>>>>>> 2ec8875ee33f28360b13903b63c197a861e75c7f
    
    appl.layout = html.Div([
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
                    step = None,
                    marks={int(i) : str(i) for i in years},
                    value=years[0]
                )
            ]),

            dcc.Tab(label='Tab two', children=[
                dcc.Graph(
                    figure = px.histogram(dataO, x = dataO[y])
                )

                #dcc.RadioItems(
                #    id="variables",
                #    options=[{'label' : str(y), 'value' : str(y)} for y in variables],
                #    value='BB-P100-TOT'
                #)
            ]),

            dcc.Tab(label='Tab three', children=[
                html.Iframe(id = 'map', srcDoc = open('map.html','r').read(), width = '100%', height = '600')
            ]),
        ])
    ])
    webbrowser.open("http://127.0.0.1:8050/",new=1)
    @appl.callback(
    Output(component_id='graph1', component_property='figure'), # (1)
    [Input(component_id='year-slider', component_property='value')] # (2)
    )

    def update_figure(input_value): # (3)
        return px.scatter(dataf[input_value], x=dataf[input_value][x], y=dataf[input_value][y], #data[input_value]
                        color=dataf[input_value][coloured], #size="pop",
                        hover_name=dataf[input_value][hover]) # (4)


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

