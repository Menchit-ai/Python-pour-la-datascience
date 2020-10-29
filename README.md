**Projet Dashboard Python : Analyse des données de satisfaction de vie par rapport aux pays, aux années, et à d'autres données complémentaires**



**Introduction :**


Ce projet a pour but d'intégrer dans un dashboard trois éléments graphiques permettant de comparer les différents pays du monde :

-Un graphe comparant une donnée choisie par l'utilisateur à la satisfaction de vie dans les pays

-Un histogramme comptant une donnée pour tous les pays pour une année choisie

-Une carte choroplète qui montre les différents niveaux de données dans chaque pays pour une année choisie


Lien du dataset : https://ourworldindata.org/


**User's Guide :**


Pour démarrer l'application, il faut avoir dans le même dossier :

-Les deux fichiers Python createDatapack.py et main.py

-Le fichier install.py si les packages ne sont pas installés

-Le fichier world.json pour la carte

-Le dossier data_world contenant tous les fichiers csv nécessaires pour la comparaison de données

Pour avoir le dashboard décrit ci-dessus, il faut exécuter le fichier Python main.py, et peut être exécuté à partir de l'invite de commandes

Différents packages sont utilisés pour les deux fichiers Python : os, requests, pandas, plotly et plotly.express, numpy, datetime folium, 
geopandas, json, pycountry, dash, dash corecomponents, dash htmlcomponents, webbrowser.

L'installation de ces packages se fait automatiquement en exécutant le fichier install.py via la commande "python install.py". Si l'installation ne fonctionne pas, 
on peut installer tous les packages avec la commande *pip install XXX* où XXX est le nom du package en question. S'il y a encore des
problèmes d'installation (notamment pour geopandas qui peut causer quelques soucis), on peut utiliser la commande *conda install XXX* dans l'Anaconda Prompt.
Si des problèmes subisistent, les diverses commandes d'installation via Anaconda peuvent être trouvées sur le site Anaconda.org .

Le dashboard devrait s'ouvrir automatiquement au lancement du main.py, normalement il s'ouvrira deux fois, si le dashboard ne s'ouvre pas automatique, utiliser l'url suivante : "http://127.0.0.1:8050/"



**Developper's Guide :**


Le programme fonctionne en utilisant les fichiers csv se trouvant dans le dossier donné en "path" dans la fonction parseCSV, les colonnes des dataframes doivent ensuite être
de la forme [noms de pays, code ascii2 du pays, année de la donnée, valeur de la donnée], il suffit ensuite de passer la liste des dataframes à la fonction standardizeData qui
va renommer les colonnes et les mettre dans le bon ordre pour rendre les dataframes exploitables pour la suite. Tous les dataframes sont ensuite pris en compte et utilisables
dans le dashboard. Toutes les fonctions utilisées sont présentes de le fichier createDatapack.py . Actuellement la mise en forme des dataframes est faite directement dans le fichier
main.py .








