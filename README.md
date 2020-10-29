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
Le dashboard peut continuer d'ouvrir de lui-même, ce bug n'a pas été résolu mais n'impacte pas le fonctionnement du dashboard. Si ce bug est trop  impactant, il suffit de commenter
la ligne 26 du main.py et d'ouvrir le dashboard manuellement en utilisant l'url ci-dessus.


**Developper's Guide :**


Le programme fonctionne en utilisant les fichiers csv se trouvant dans le dossier donné en "path" dans la fonction parseCSV, les colonnes des dataframes doivent ensuite être
de la forme [noms de pays, code ascii2 du pays, année de la donnée, valeur de la donnée], il suffit ensuite de passer la liste des dataframes à la fonction standardizeData qui
va renommer les colonnes et les mettre dans le bon ordre pour rendre les dataframes exploitables pour la suite. Tous les dataframes sont ensuite pris en compte et utilisables
dans le dashboard. Toutes les fonctions utilisées sont présentes de le fichier createDatapack.py . Actuellement la mise en forme des dataframes est faite directement dans le fichier
main.py .



**Analyse des résultats :**

Avec les fichiers que nous avons choisis d'utiliser, nous pouvons montrer des corrélations entre différents critères. En exploitant les graphiques du premier onglet de notre
dashboard, on peut tenter de définir une courbe des tendances entre la variable étudiée et la variable principale que nous utilisons : la satisfaction de vie (le bonheur dans un pays).
Nous pouvons ainsi montrer que la bonheur dans un pays est impacté par plusieurs critères. Il est fortement impacté négativement par le nombre d'heures de travail et est faiblement impacté
positivement par la liberté économique du pays. Il est fortement impacté par l'espérance de vie moyenne dans un pays. On voit ensuite que l'indice de développement humain est fortement corrélé
au niveau de bonheur. On en déduit donc que le PIB par habitant, l'espérance de vie à la naissance et le niveau d'éducation des enfants de 17 ans et plus impactent tous fortement le niveau
de satisfaction d'un pays. On voit aussi que le régime politique n'impact pas le niveau de satisfaction d'un pays. Enfin la consommation d'énergie d'un Etat impact peu la satisfaction
(même si visiblement plus la consommation est élevée plus le pays est considéré comme heureux).


