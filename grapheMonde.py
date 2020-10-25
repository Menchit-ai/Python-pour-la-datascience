from createDatapack import *
#On importe ici notre fichier qui contient toutes les fonctions nécessaires

if __name__ == "__main__":

    init()

    filesName,datag,dataCol = parseCSV(r".\data_world")
    index = filesName.index("share-of-electricity-production-from-renewable-sources.csv")
    #Pour ce fichier on a un souci avec un Code qui n'est pas reconnu par la fonction Continent
    elec = datag[index]
    
    elec[elec['Code']=='OWID_KOS'] = 'KOS'
    
    try:
        data = mergeData(filesName,datag,"happiness-cantril-ladder.csv","life-expectancy.csv",["Code","Year","Entity"])
        
    except NameError as e:
        print(e)
        quit()

    data = continent(data)
    nTab = len(data.columns)
    diffyears = uniqueYear(data, 'Year')
    diffyears.sort()
    dico = createDataDic(data, 'Year', diffyears)
    #On crée les premiers éléments du Dashboard (qui vont ensuite être modifiés par les Dropdowns et Sliders)

    #print(diffyears[0])

    #print(dico[2008])
    x = "Life satisfaction in Cantril Ladder (World Happiness Report 2019)"
    y = "Life expectancy"

    #map(data,2012,y)


    fig = createFig(dico, 2008, x, y, 'Continent', 'Entity')
    #On crée le premier graphe qui va être affiché

    # webbrowser.open("http://127.0.0.1:8050/",new=1)
    app = dash.Dash(__name__)
    dashBoard(dico, data, diffyears, fig, filesName, datag, dataCol, 'Continent', 'Entity', appl=app)
    app.run_server(debug=True)
