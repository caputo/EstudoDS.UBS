#Converte o arquivo XML para CSV
import xml.etree.ElementTree as ET 
import csv

tree = ET.parse("UnidadesDeSaude.xml")
elements = tree.getroot()

#No XML a cada 6 linhas representa uma UBS
#<registros>48</registros>  - ignora a primeira linha
#<codigo>200</codigo> 1 #
#<descricao>UBS Buquirinha</descricao> 2 
#<x>-45.91618149999999</x> 3 
#<y>-23.1126931</y> 4 
#<cor>800000</cor> 5 
#<mais>S</mais> 6

#Cria um vetor para guardar as linhas
rows = [] 
print(str(len(elements)) + ' elementos')

for i in range(1, len(elements)-1,6):
    print(i)
    rows.append([elements[i].text,elements[i+1].text,elements[i+2].text,elements[i+3].text,elements[i+4].text,elements[i+5].text])

with open("unidades.csv",'w',newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)


