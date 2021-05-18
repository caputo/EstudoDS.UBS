import pandas as pd
import numpy as np
from simpledbf import Dbf5
import matplotlib.pyplot as plt

#CONSIDERADO DEZ ANOS A MENOS POIS O DADO É DE DEZ ANOS ATRÁS 

field = 'V061'
alias= 'Pop_45A49'

dbf = Dbf5('shp/setores_ubs_result.dbf')
df = dbf.to_dataframe()


#Visualizar qual possue mais residentes com a idade
groupedByUbs = df[df['Field2'] != 0].groupby('Field2').agg(Habitantes= pd.NamedAgg(column=field, aggfunc=sum))


#Seleciona apenas os 10 primeiros 
#groupedByUbs = groupedByUbs.sort_values('Habitantes', ascending  = False).head(10)
#groupedByUbs.unstack(fill_value=0).plot.bar()
#plt.title("População 55 a 59 anos por UBS")
#plt.xlabel("UBS")
#plt.ylabel("Habitantes")
#print(groupedByUbs)
#plt.show()
#print(len(groupedByUbs))
#exit()

#Visualizar o boxplot do dado agrupado por UBS
groupedByUbs.boxplot()
#plt.show()
print(groupedByUbs.describe())
q1 = groupedByUbs['Habitantes'].quantile(0.25)
print('Primeiro quantil: ' + str(q1))
q3 = groupedByUbs['Habitantes'].quantile(0.75)
print('Tereceiro quantil: ' + str(q3))
q4 =  groupedByUbs['Habitantes'].quantile(0.99)
q0 = groupedByUbs['Habitantes'].quantile(0.11)
mediana = q3 - q1

outlier_top_lim = q3 + 1.5 * (q3 - q1)
outlier_bottom_lim = q1 - 1.5 * (q3 - q1)


abaixoQ1 = groupedByUbs[( (groupedByUbs['Habitantes']  < q1) & (groupedByUbs['Habitantes']  > outlier_bottom_lim) )]
acimaQ3 = groupedByUbs[( (groupedByUbs['Habitantes']  > q3) & (groupedByUbs['Habitantes']  < outlier_top_lim) )]



outlinersTop = groupedByUbs[(groupedByUbs['Habitantes']  > outlier_top_lim)]
outlinersBottom = groupedByUbs[(groupedByUbs['Habitantes']  < outlier_bottom_lim)]


print("Outliers top: > " + str(outlier_top_lim))
print(outlinersTop)
print("Outliers bottom: <" + str(outlier_bottom_lim))
print(outlinersBottom)

print("Abaixo do primeiro quantil")
print(abaixoQ1)
print("Acima do terceiro quantil")
print(acimaQ3)


print("Dentro")
print(groupedByUbs[( (groupedByUbs['Habitantes']  < q3) & (groupedByUbs['Habitantes']  > q1))])

#quantiles = df.quantile([0.01, 0.25, 0.5, 0.75, 0.99])
#filter = (groupedByUbs['Habitantes'] >= q1 - 1.5 * iqr) & (groupedByUbs['Habitantes'] <=q3 + 1.5 *iqr)

#print(groupedByUbs[filter])
plt.plot([1]*len(groupedByUbs),groupedByUbs[0],'x')
plt.show()

#print(df.groupby('Field1').agg(V154= pd.NamedAgg(column='V154', aggfunc=sum)))

#df.plot(x="Field1",y="V154")


#V066 - 70 A 74 
#V065 - 65 A 69
#V064 - 60 A 64 
#V063 - 55 A 59