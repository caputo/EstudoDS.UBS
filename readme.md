*Estudo de estimativa de capacidade de atendimento em postos UBS de acordo com a densidade populacional por faixa etária*


OBJETIVO: Através de uma preparação de dados geográficos, criar uma amostra com uma estimativa de área de atendimento por unidade de saúde e 
realizar uma comparação indicando quais se encontram dentro dos quartis medianos e quais podem sofrer super lotação.
Essa análise permite que a prefeitura crie ações necessárias para dias de vacinação criando postos de vacinação para as áreas indicadas como fora do padrão. 

Dados de entrada: 
    - POI de UBS
    - Setores Censitarios
    - Limite municipal 




Geração de pontos de interesse de UBS

Para fazer essa análise, primeiramente foi necessário obter a localização dos postos de saúde, a fim de determinar qual área seria atendida por cada posto. 
Foi realizado uma pesquisa sobre os dados da prefeitura de São José dos Campos, porém não foi encontrado de forma intuítiva como um dado aberto disponibilizado pela prefeitura. 
Então para fazer a extração desse dado, foi localizado um serviço de mapa disponibilizado pela prefeitura onde indica os postos de saúde. Então através do depurador do navegador foi possivel identificar o serviço que disponibilizava o XML para tal informação, assim consegui extrair o XML com a informação que precisava. 

Passos:
 - Acessei o site https://servicos2.sjc.sp.gov.br/mapa-google.aspx?p=12
 - Através o depurador verifiquei o codigo fonte e identifiquei a parte do código que fazia a chamada para o serviço, assim foi possivel identificar o endereço da chamada.
 - Com o endereço acessei diretamente o serviço e salvei o XML : https://servicos2.sjc.sp.gov.br//pmsjc_paginas/GuiaDeUnidadesV2MGoogle_Busca.aspx?categ=12

Com o XML em mão, o formato do XML não atenderia às futuras necessidades, então achei necessário criar um script para converter esse arquivo para XML: 
#Script Conversão


Agora, com o arquivo CSV já é possivel importar diretamento no ArcMAP e gerar um SHAPEFILE com os pontos de interesse. 
Essa ação foi feita manualmente e gerado o arquivo xxx. (TODO: Pode ser feito via script usando ArcPY)


--------

Dados Censitário 

Primeiramente é necessário ter o limite dos setores censitários do município. Então foi realizado o download do shapefile dos limites dos setores censitários através do site do IBGE. Essa dado porém, não contém o resultado da pesquisa do Censo, então foi necessário pesquisar dentre os dados disponibilizados pelo IBGE o arquivo que contém o resultado da pesquisa Censo2010. Foi localizado um arquivo XLS com o resultado da pesquisa com o código de cada Setor (https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Sinopse/Agregados_por_Setores_Censitarios/).
O arquivo XLS contém os dados de todos municipios do estado de SP, então foi extraído apenas os dados do municipio de SJC, e salvo para CSV. Com o CSV foi realiazado através do ArcMAP(também possivel via script) a conversão para o formato DBF, pois foi identificado a necessidade de conversão de tipo de campos para que fosse possivel realizar o Join com os setores, então durante essa conversão foi alterado o tipo do campo COD_SETOR, e substituido nos campos das variaveis de pesquisa os valor X por 0. 
Então foi realizado o join entra os limites dos setores censitarios com o resultado da pesquisa (dbf), após o Join foi exportado esse dado para Shapefile. 

------

Definição de área de atendimento 

Para a definição da área de atendimento, foi executado através do métodos Thissen (Diagráma de Voronoi). 
Esse é uma método matematico, que dado um espaço métrico e uma familia de subconjuntos (pontos) são gerado áreas atravé da decomposição da equidistancia entre os pontos.
Resumidamente, as fronteiras do poligono do ponto, se dará através da métade da distancia entre seus pontos mais próximos. 

-- Todo: criar uma imagem explciativa 

Assim, com o dado do limite (extent) dos setores censitarios e com os pontos de interesse, foi executado a ferramenta Thiesse Polygon, e assim foram gerado as áreas de interesse de cada posto UBS. 

-- Todo: colocar imagem 


Com o dado da área de atendimento, foir realizado um cruzamento espacial (Spatial Join), a fim de associar em cada setor, qual posto de atendimento ele é atendido. 
Para aquele que se encontram na fronteira de dois postos, é associado o qual ele esta em maior área contida. 

---------- 

Pronto, agora temos o dado necessário, o número de pessoas por posto de atendimento, e classificado por faixa etária. 
Agora vamos analisar esse dado. 

Primeiramente vamos analisar de uma forma mais simples, vamos agrupar o setores e ver a UBS com mais habitantes. 

: codigo 

UBS Jardim das Indústrias                         1140
AME - Ambulatório Médico de Especialidades        1102
UBS Vila Industrial-Tatetuba                       770
UBS Bosque dos Eucaliptos                          619
UBS Jardim da Granja                               570
UBS Jardim Morumbi                                 523
UPA de Saúde Mental                                515
UBS Jardim Paulista                                482
UBS Vila Tesouro                                   460
UBS Centro II                                      417

Podemos ver aqui as UBS que ja merecem um pouco de atenção, mas será que são todas? 
Vamos analisar então através de um gráfico bloxpot, pra ver quem são as outliners, e tambem quais estão abaixo do 1 quantil, que hipoteticamente poderia estar recebendo mais pacientes. E as que estão acima do 3º quantil, que hipoteticamente podem sofrer lotações. 

Primeiramente vamos ver o gráfico para termos uma ideia: 


Numero de UBS: 



Limite outlier top: > 756.5
UBS                                           Habitantes
AME - Ambulatório Médico de Especialidades        1102
UBS Jardim das Indústrias                         1140
UBS Vila Industrial-Tatetuba                       770

Então essas são as UBS que estão totalmente fora do padrão da amostra, hipoteticamente seriam as UBS que mais sofreriam lotação em um dia de vacinação. 


Mas não só são essas que merecem atenção, vamos visualizar quais estão acima do terceiro quantil: 

UBS                           Habitantes
UBS Bosque dos Eucaliptos         619
UBS Centro II                     417
UBS Jardim Morumbi                523
UBS Jardim Oriente                410
UBS Jardim Paulista               482
UBS Jardim da Granja              570
UBS Vila Tesouro                  460
UBS Vista Verde                   386
UPA de Saúde Mental               515


Então podemos dizer que essas tambem está um pouco fora do padrão da amostra, onde o quadrante fia entre 124 e 377 habitantes. 

Mas também é importante identificar quais são aquelas que terão baixo atendimento, seja por baixo população na área, ou por caracteristica etária da população. Assim podemos deslocar habitantes de uma área lotada para essas UBS. 

UBS Alto da Ponte                 41
UBS Bonsucesso                    15
UBS Chácaras Reunidas             89
UBS Dom Pedro                     46
UBS Jardim Santa Inês II          79
UBS Jardim São José II            79
UBS Limoeiro                     107
UBS Putim                         20
UBS São Francisco Xavier          53
UBS São Judas Tadeu               78
UPA Sem Nome                     121
UPA São Francisco Xavier          26


Ubs dentro 

                           Habitantes
Field2
Hospital de Clínicas Sul          374
UBS Altos de Santana              178
UBS Buquirinha                    244
UBS Campo dos Alemães             221
UBS Campos São José               219
UBS Centro I                      270
UBS Colonial                      348
UBS Eugênio de Melo               217
UBS Jardim Nova Detroit           272
UBS Jardim Satélite               315
UBS Jardim Telespark              179
UBS Paraíso do Sol                265
UBS Parque Industrial             362
UBS Parque Interlagos             126
UBS Parque Novo Horizonte         255
UBS Residencial União             136
UBS Santana                       316
UBS Vila Maria                    262
UBS Vila Nair                     125
UBS Vila Paiva                    236
UPA Alto da Ponte                 127
UPA Campo dos Alemães             294
UPA Eugênio de Melo               139
UPA Novo Horizonte                301

# grafico 





Geração dos dados censisarios
Download do shapefile dos limites dos Setores
Download do xls com os dados censitarios de SP : https://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Sinopse/Agregados_por_Setores_Censitarios/
Extraido para csv apenas os dados de sjc
Convertido o csv para dbf alterando o tipo do campo de cod_setor e substituindo valores X por 0 
Join entre os limites censitarios e os dados - Exportado o dado com limite de setores e valores do censo 


Criado o Thiessen Polygon tendo como entrada os pontos da Ubs e setado no enviroment da ferramenta o extent dos setores 
(Foi feito manualmente mas pode ser via script)



