from createDatapack import *

if __name__ == "__main__":
    init()
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

    nTab = len(data.columns)
    #print(data.head())
    # graph.show()
    # plotly.offline.plot(graph, filename='fig.html', auto_open=True, include_plotlyjs='cdn')
# https://plotly.com/python/text-and-annotations/

    diffyears = uniqueYear(data, 'Year')
    diffyears.sort()
    dico = createDataDic(data, 'Year', diffyears)

    print(diffyears)
    #print(dico[2008])
    fig = createFig(dico, 2008, str(data.columns[nTab-1]), str(data.columns[nTab-2]), 'Entity', 'Entity')


    app = dash.Dash(__name__)
    dashBoard(dico, diffyears, fig, str(data.columns[nTab-1]), str(data.columns[nTab-2]), 'Entity', 'Entity', app)
    app.run_server(debug=True)