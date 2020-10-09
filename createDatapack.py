import pandas as pd

dataAbo = pd.read_csv("abo.csv",delimiter=",")

# passer TIME en date en supprimant les semestres
# drop Pays, Variable, Temps, Unit, Flag Codes, Flags, PowerCode

# on drop les colonnes servant à l'homme et les colonnes ne contenant que des NaN
dataAbo = dataAbo.drop(["Pays","Variable","Temps","Unit","Flag Codes","Flags","PowerCode","Reference Period Code","Reference Period"], axis=1)

##########################################################################################

dataPIB = pd.read_csv("PIB\dataPIB.csv",delimiter=",",header = 2)
# print(dataPIB.head())
# print(dataPIB.info())
# print(dataPIB["Indicator Name"].unique()) # --> supprimer la colonne
dataPIB = dataPIB.drop("Indicator Name",axis=1)
# print(dataPIB["Indicator Code"].unique()) # --> supprimer la colonne
dataPIB = dataPIB.drop("Indicator Code",axis=1)

# print(dataPIB.describe())
# print(dataPIB.isna().sum())
dataPIB = dataPIB.drop(["Unnamed: 65","2020"],axis=1)
# print(dataPIB.info())


##########################################################################################

dataSan = pd.read_csv("depense_sante.csv",delimiter=",")
# print(dataSan)
# print(dataSan.isna().sum())
# print("##################")
# for i in dataSan.columns:
#     print(i," ",dataSan[i].unique())
dataSan = dataSan.drop(["INDICATOR","FREQUENCY"],axis=1)