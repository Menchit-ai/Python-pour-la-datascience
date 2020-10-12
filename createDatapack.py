import os

import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly.express as px

# dataAbo = pd.read_csv("abo.csv",delimiter=",")

# # passer TIME en date en supprimant les semestres
# # drop Pays, Variable, Temps, Unit, Flag Codes, Flags, PowerCode

# # on drop les colonnes servant à l'homme et les colonnes ne contenant que des NaN
# dataAbo = dataAbo.drop(["Pays","Variable","Temps","Unit","Flag Codes","Flags","PowerCode","Reference Period Code","Reference Period"], axis=1)

# ##########################################################################################

# dataPIB = pd.read_csv("PIB\dataPIB.csv",delimiter=",",header = 2)
# # print(dataPIB.head())
# # print(dataPIB.info())
# # print(dataPIB["Indicator Name"].unique()) # --> supprimer la colonne
# dataPIB = dataPIB.drop("Indicator Name",axis=1)
# # print(dataPIB["Indicator Code"].unique()) # --> supprimer la colonne
# dataPIB = dataPIB.drop("Indicator Code",axis=1)

# # print(dataPIB.describe())
# # print(dataPIB.isna().sum())
# dataPIB = dataPIB.drop(["Unnamed: 65","2020"],axis=1)
# # print(dataPIB.info())


# ##########################################################################################

# dataSan = pd.read_csv("depense_sante.csv",delimiter=",")
# # print(dataSan)
# # print(dataSan.isna().sum())
# # print("##################")
# # for i in dataSan.columns:
# #     print(i," ",dataSan[i].unique())
# dataSan = dataSan.drop(["INDICATOR","FREQUENCY"],axis=1)
# # faire le pivot longer

def parseCSV(path):
    if not path.endswith("\\"):
        path = path +"\\"
    filesName = os.listdir(path)
    pathFiles = [path + sub for sub in filesName] 
    for fil in filesName:
        if not fil.endswith(".csv"):
            filesName.remove(i)
            pathFiles.remove(i)
    #donne la liste des tous les fichiers csv présent dans le répertoire indiqué par path

    data = []
    for fil in pathFiles:
        data.append(pd.read_csv(fil,delimiter=","))
    #data est la liste des dataframes correpondant aux csv présent dans le répertoire
    return (filesName,data)

def mergeData(names,liData,dataName1,dataName2,join):
    
    if not (dataName1 in names or dataName2 in names):
        raise NameError("These dataNames are not available in this list of dataframe")

    data1 = liData[names.index(dataName1)]
    data2 = liData[names.index(dataName2)]

    if not (set(join).issubset(data1.columns) or set(join).issubset(data2.columns)):
        raise NameError("Cannot join the dataframe, join name is absent from at least one of them")

    joinedData = data1.merge(data2, on=join, how='inner')

    return joinedData

def createGraph(data,x,y,title="Insérez un titre",mode='markers',text="Entity"):
    year=2008
    data = data.query('Year == '+str(year))
    trace = px.scatter(
    x=data[x],
    y=data[y],
    color = data['Year']
    )
    
    # data = [trace]

    # layout = px.layout(title=title,
    #                         xaxis=dict(
    #                         title=x,
    #                         ticklen=5,
    #                         zeroline=False,
    #                         gridwidth=2,
    #                     ),
    #                     yaxis=dict(
    #                         title=y,
    #                         ticklen=5,
    #                         zeroline=False,
    #                         gridwidth=2,
    #                     ),)
    trace.show()
    return trace


if __name__ == "__main__":
    
    filesName,data = parseCSV(r".\data_world")

    try:
        data = mergeData(filesName,data,"happiness-cantril-ladder.csv","human-development-index.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()

    print(data.head())
    data.to_csv(r".\data_world\AAAfichier-test.csv",sep=",")

    graph = createGraph(data,"Life satisfaction in Cantril Ladder (World Happiness Report 2019)","Human Development Index (UNDP)",title="Happiness vs HDI")
    # graph.show()
    # plotly.offline.plot(graph, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
# https://plotly.com/python/text-and-annotations/