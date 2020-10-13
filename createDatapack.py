import os

import requests

import pandas as pd
import plotly.graph_objs as go
import plotly
import plotly.express as px

import pycountry
import numpy as np
import datetime

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

def downloader(urls):
    # attend une liste d'urls
    for url in urls:
        r = requests.get(url, allow_redirects=True)
        filename = getFilename_fromCd(r.headers.get('content-disposition'))
        open(r'.\data_world\\'+str(filename), 'wb').write(r.content)

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


if __name__ == "__main__":
    
    filesName,data = parseCSV(r".\data_world")

    try:
        data = mergeData(filesName,data,"happiness-cantril-ladder.csv","human-development-index.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()


    data.to_csv(r".\data_world\AAAfichier-test.csv",sep=",")

    print("colonnes de base :"+ str(data.columns))
    data = data.rename(columns = {'Code':'ccc','Entity':'eee','Year':'yyy'})
    print("colonnes renommées :"+ str(data.columns))
    l = standardizeData([data])
    data = l[0]
    print("colonnes standardes :"+ str(data.columns))
    # graph.show()
    # plotly.offline.plot(graph, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
# https://plotly.com/python/text-and-annotations/
