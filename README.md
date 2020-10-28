**Projet Dashboard Python : Analyse des données de satisfaction de vie par rapport aux pays, aux années, et à d'autres données complémentaires**



**Introduction :**


Ce projet a pour but d'intégrer dans un dashboard trois éléments graphiques permettant de comparer les différents pays du monde :

-Un graphe comparant une donnée choisie par l'utilisateur à la satisfaction de vie dans les pays

-Un histogramme comptant une donnée pour tous les pays pour une année choisie

-Une carte choroplète qui montre les différents niveaux de données dans chaque pays pour une année choisie


Lien du dataset :


**User's Guide :**


Pour démarrer l'application, il faut avoir dans le même dossier :

-Les deux fichiers Python createDatapack.py et main.py

-Le fichier install.py si les packages ne sont pas installés

-Le fichier world.json pour la carte

-Le dossier data_world contenant tous les fichiers csv nécessaires pour la comparaison de données

Pour avoir le dashboard décrit ci-dessus, il faut exécuter le fichier Python main.py, et peut être exécuté à partir de l'invite de commandes

Différents packages sont utilisés pour les deux fichiers Python : os, requests, pandas, plotly et plotly.express, numpy, datetime folium, 
geopandas, json, pycountry, dash, dash corecomponents, dash htmlcomponents, webbrowser.

Normalement, l'installation de ces packages se fait automatiquement grâce au fichier install.py. Pour cette fonction il faut installer
subprocess (pip install subprocess). Si l'installation ne marche pas, on peut installer tous les packages avec la commande *pip install*. S'il y a encore des
problèmes d'installation (notamment pour geopandas qui peut causer quelques soucis), on peut utiliser la commande *conda install* dans l'Anaconda Prompt.
Cependant, avoir Anaconda est nécessaire pour ce type de commande.







