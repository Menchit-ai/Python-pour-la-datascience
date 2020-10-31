from createDatapack import *

if __name__ == "__main__":

    init()
    x = "Life satisfaction in Cantril Ladder (World Happiness Report 2019)"
    y = "Life expectancy"

    filesName,datag,dataCol = parseCSV(r".\data_world")
    
    try:
        data = mergeData(filesName,datag,"happiness-cantril-ladder.csv","life-expectancy.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()

    data = continent(data)
    nTab = len(data.columns)
    diffyears = uniqueYear(data, 'Year')
    diffyears.sort()
    dico = createDataDic(data, diffyears, 'Year')

    fig = createFig(dico, 2008, x, y, 'Continent', 'Entity')

    webbrowser.open("http://127.0.0.1:8050/",new=1)
    app = dash.Dash(__name__)
    dashBoard(dico, data, diffyears, fig, filesName, datag, dataCol, 'Continent', 'Entity', appl=app)
    app.run_server(debug=False)
