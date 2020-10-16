from createDatapack import *

if __name__ == "__main__":
    init()
    filesName,data,dataCol = parseCSV(r".\data_world")

    try:
        data = mergeData(filesName,data,"happiness-cantril-ladder.csv","life-expectancy.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()

    data = continent(data)
    nTab = len(data.columns)
    diffyears = uniqueYear(data, 'Year')
    diffyears.sort()
    dico = createDataDic(data, 'Year', diffyears)

    #print(diffyears)
    #print(dico[2008])
    x = "Life satisfaction in Cantril Ladder (World Happiness Report 2019)"
    y = str(data.columns[-2])

    fig = createFig(dico, 2008, x, y, 'Continent', 'Entity')


    app = dash.Dash(__name__)
<<<<<<< HEAD
    dashBoard(dico,data, diffyears, fig,  x, y, 'Continent', 'Entity', appl=app)
=======
    dashBoard(dico, data, diffyears, fig,  str(data.columns[nTab-2]), str(data.columns[nTab-1]), 'Entity', 'Entity', appl=app)
>>>>>>> 2ec8875ee33f28360b13903b63c197a861e75c7f
    app.run_server(debug=True)
