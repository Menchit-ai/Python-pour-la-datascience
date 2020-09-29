from googletrans import Translator
import pandas as pd

def translate(dataframe, colname):
    translator = Translator()
    liOrig = dataframe[colname].unique()
    liEng = []
    print(liOrig)
    sentences = ['Bienvenu', 'Comment allez-vous', 'je vais bien']
    result = translator.translate(sentences, src='fr', dest='sw')
    for trans in result:
        print(f'{trans.origin} -> {trans.text}')
    # trans = {}
    # for country in range(len(liOrig)):
    #     trans[liOrig[i]] = liEng[i]
    # dataframe[colname].map(trans)
    

data = pd.read_csv("abo.csv",delimiter=',')
country = data["Pays"].unique()
translate(data,"Pays")

# print(data.head(40))