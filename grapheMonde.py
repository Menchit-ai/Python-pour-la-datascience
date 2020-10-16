from createDatapack import *

if __name__ == "__main__":
    init()
    filesName,data,dataCol = parseCSV(r".\data_world")

    try:
        data = mergeData(filesName,data,"happiness-cantril-ladder.csv","life-expectancy.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()

    nTab = len(data.columns)
    diffyears = uniqueYear(data, 'Year')
    diffyears.sort()
    dico = createDataDic(data, 'Year', diffyears)

    #print(diffyears)
    #print(dico[2008])
    fig = createFig(dico, 2008, str(data.columns[nTab-2]), str(data.columns[nTab-1]), 'Entity', 'Entity')


    app = dash.Dash(__name__)
    dashBoard(dico, diffyears, fig,  str(data.columns[nTab-2]), str(data.columns[nTab-1]), 'Entity', 'Entity', appl=app)
    app.run_server(debug=True)
