#!/usr/bin/env python
# coding: utf-8

# # <b/>Projet 2 : Analysez des données de systèmes éducatifs</b>

# **Pascaline Grondein**
# 
# **Date début projet : 07/02/2022**
# 
# 
# En tant que Data Scientist dans une start-up de la EdTech, nommée academy, qui propose des contenus de formation en ligne pour un public de niveau lycée et université, j'ai reçu une première mission d’analyse exploratoire concernant une expansion à l'international. 
# 
# Par cette étude je dois déterminer : 
# 
#  - Quels sont les pays avec un fort potentiel de clients pour nos services ?
#  - Pour chacun de ces pays, quelle sera l’évolution de ce potentiel de clients ?
#  - Dans quels pays l'entreprise doit-elle opérer en priorité ?
# 

# ### Table of Contents
# 
# * [I. Jeu de données pays](#chapter1)
#     * [1 Nettoyage et sélection des variables](#section_1_1)
#     * [2 Variable Income Group](#section_1_2)
# * [II. Jeu de données indicateurs](#chapter2)
#     * [1 Nettoyage et sélection des variables](#section_2_1)
#     * [2 Pré-sélection des indicateurs](#section_2_2)
#          * [a. Indicateurs démographique : population entre 15 et 24 ans](#section_2_2_1)
#          * [b. Indicateurs démographique : croissance démographique](#section_2_2_2)
#          * [c. Indicateur d'éducation dans le secondaire](#section_2_2_3)
#          * [d. Indicateur d'éducation dans le tertiaire](#section_2_2_4)
#          * [e. Indicateur pour internet](#section_2_2_5)
#          * [f. Indicateur pour internet](#section_2_2_5)
# * [III. Jeu de données final](#chapter3)            
#     * [1. Nettoyage et sélection des variables](#section_3_1)
#     * [2. Sélection de la variable Population Totale](#section_3_2)
#     * [3. Sélection finale des indicateurs](#section_3_3)
# * [IV. Calcul et attribution des points par indicateur](#chapter4)
#     * [1.  Indicateurs démographiques : population entre 15 et 24 ans](#section_4_1)
#     * [2.  Indicateurs démographiques : croissance démographique](#section_4_2)
#     * [3.  Indicateur pour l'accès à internet](#section_4_3)
#     * [4. Indicateur pour l'éducation dans le secondaire](#section_4_4)
#     * [5. Indicateur pour l'éducation dans le tertiaire](#section_4_5)
# * [V. Calcul et attribution des points par indicateur](#chapter5)

# In[72]:


#importation librairies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pct_seuil = 50 #seuil du pourcentage de remplissage pour les indicateurs


High_income = 2 #points attribué aux pays de cette classe de revenu
Middle_income = 1 #points attribué aux pays de cette classe de revenu
Low_income = 0 #points attribué aux pays de cette classe de revenu

boxprops = dict(linestyle='-', linewidth=1, color='k')
medianprops = dict(linestyle='-', linewidth=1, color='k')
meanprops = dict(marker='D', markeredgecolor='black',markerfacecolor='firebrick')


# #   <a class="anchor" id="chapter1">I. Sélection du jeu de données pays</a>

# ##  <a class="anchor" id="section_1_1">1. Nettoyage et sélection des variables</a>

# Le fichier EdStatsCountry.csv est un annuaire des pays. 

# In[2]:


countries = pd.read_csv('EdStatsCountry.csv')
print('Le fichier comporte',countries.shape[0],'lignes et',countries.shape[1],'colonnes.')


# Ce fichier comporte de nombreuses variables, qui ne nous seront pas utiles pour la suite. Une sélection des variables pertinentes est alors nécessaire.

# In[3]:


countries.dtypes


# Dans le cadre de notre étude, il nous faut déterminer quels sont les pays avec un fort potentiel de clients pour nos services. La start-up Academy proposant des contenus de formation en ligne pour un public de niveau lycée et université, les variables pouvant nous intéresser sont : 
# 
# Pour l'indentification : 
#   - Country Code : code du pays
#   - Short Name : nom du pays raccourci
#   
# Pour la localisation et la classification :
#   - Region : Zone géographique du pays
#   - Income group : classement du pays en fonction du niveau de revenu
#   
# Toutes ces variables sont au bon format (object), donc inutile de les convertir.
#   
# On peut réduire le fichier à ces colonnes:

# In[4]:


countries = countries[['Country Code','Short Name','Region','Income Group']]


# Regardons les valeurs manquantes pour ce fichier :

# In[5]:


#On collecte le nombre de valeurs manquanets par variable
nb_na = countries.isnull().sum() 
print ('Ce fichier comporte',nb_na.sum(),'valeurs manquantes.' )

#On calcule le pourcentage de valeurs manquantes par variabels
index = countries.index
pct_manquant = pd.DataFrame(((nb_na/len(index))*100).astype(int), columns=['Pourcentage de données manquantes (%)']) 


#On trace les pourcentages de valeurs manquantes, en retirant les variables avec un pourcentages nul ou supérieur au seuil
sns.set_style("whitegrid")
pct_manquant.plot.bar(x=None, y=None, ylim = [0,100], sort_columns = pct_manquant['Pourcentage de données manquantes (%)'],legend=False,figsize=(8, 5))
plt.title("Pourcentage de donnée manquantes (%)",fontsize=20)
plt.xticks(rotation=30, horizontalalignment="center",fontsize=15)
plt.yticks(fontsize=15)
plt.show()


# Les variables sélectionnées ont peu de valeurs manquantes, il est alors possible d'ignorer les lignes concernées.
# 
# Retirons les pays n'ayant aucune région ou groupe de revenu indiqué.

# In[6]:


countries = countries.dropna(axis = 0)
print('Il reste',countries.shape[0],'pays.')


# Vérifions s'il existe des doublons.

# In[7]:


countries.loc[countries['Country Code'].duplicated(keep=False),:]


# Aucun doublon n'est détecté.

# ##  <a class="anchor" id="section_1_2">2. Variable Income Group</a>

# Intéressons nous à la variable 'Income Group'.

# In[8]:


countries['Income Group'].unique()


# La catégorie "Income group" compte 5 groupes : 
# 
#   - High income (OECD) 
#   - High income (nonOECD)
#   - Upper middle income
#   - Lower middle income
#   - Low Income
#   
# OECD : Organisation for Economic Co-operation and Development, ou Organisation de Coopération et de Développement     Économiques, une organisation économique intergouvernementale avec 38 pays membres.
#  
# On peut regarder la répartition des pays dans les différents groupes :

# In[9]:


sns.set_style("whitegrid")
countries["Income Group"].value_counts(normalize=True).plot(kind='bar',figsize=(8, 5))
plt.title("Répartition des pays en fonction de leur économie",fontsize = 20)
plt.xticks(rotation=40, horizontalalignment="center",fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Il pourrait sembler intéressant de sélectionner les pays appartenant aux groupes "High Income" (OECD et non-OECD) et "Upper middle income". Cependant, le seul niveau économique ne peut rendre compte d'autres facteurs primordiaux comme l'accès à internet ou le niveau d'éducation. Se priver d'un marché possiblement importante d'une population ayant le niveau éducatif suffisant et accès à internet sous seul prétexte du niveau économique insuffisant de leur pays de résidence serait une mauvaise option d'un point de vue économique. De même, aucune pré-sélection ne sera faite en fonction de la région géographique.
# 
# Cependant, le niveau Income d'un pays peut aider au classement final des pays. Pour cela, attribuons des points en fonctions du niveau : 
# 
#   - High income (OECD & nonOECD) : +2
#   - Middle income : +1
#   - Low Income : +0

# In[10]:


countries.loc[countries['Income Group'].isin(['High income: OECD','High income: nonOECD']),'Income Point'] = High_income
countries.loc[countries['Income Group'].isin(['Upper middle income','Lower middle income']),'Income Point'] = Middle_income
countries.loc[countries['Income Group'] == 'Low income','Income Point'] = Low_income


# In[11]:


countries.head(3)


# In[12]:


print('Le fichier comporte désormais',countries.shape[0],'lignes et',countries.shape[1],'colonnes.')


# # <a class="anchor" id="chapter2">II. Jeu de données indicateurs  </a>

# ## <a class="anchor" id="section_2_1">1. Nettoyage et sélection des variables</a>

# Le fichier EdStatsSeries.csv est un annuaire des indicateurs utilisés dans l'étude. 

# In[13]:


series = pd.read_csv('EdStatsSeries.csv')
print('Le fichier comporte',series.shape[0],'lignes et',series.shape[1],'colonnes.')


# In[14]:


series.dtypes


# Comme pour le fichier annuaire des pays, le nombre de variable est important, il est donc nécessaire de sélectionner les pertinentes.
# 
# Dans le cadre de notre étude, il nous faut estimer si un pays peut être intéressant pour le développement d'un système éducatif en ligne. La start-up Academy proposant des contenus de formation en ligne pour un public de niveau lycée et université, les variables pouvant nous intéresser sont : 
# 
# Pour l'indentification : 
#   - Series Code : code de l'indicateur
#   - Indicator Name : nom de l'indicateur
#   - Long definition : définition de l'indicateur
#   
# Pour la classification
#   - Topic : nom du pays raccourci
#    
# Toutes ces variables sont au bon format (object), donc inutile de les convertir.
#   
# On peut réduire le fichier à ces colonnes:

# In[15]:


series = series[['Series Code','Indicator Name','Long definition','Topic']]


# Regardons les valeurs manquantes pour ce fichier :

# In[16]:


#On collecte le nombre de valeurs manquanets par variable
nb_na = series.isnull().sum() 
print ('Ce fichier comporte',nb_na.sum(),'valeurs manquantes.' )


# Vérifions s'il existe des doublons.

# In[17]:


series.loc[series['Series Code'].duplicated(keep=False),:]


# Aucun doublon n'est détecté.
# 
# Intéressons nous maintenant à la variable Topic.

# In[18]:


series['Topic'].unique()


# Pour l'étude, il serait intéressant de choisir 5 ou 6 indicateurs, pour illustrer les problématiques suivantes
# 
#   - Démographie : population susceptible d'être intéressés par des cours en ligne niveau lycée/fac, évolution démographique
#   - Education dans secondaire : taux d'enfants ou adolescents scolarisés, le taux d'alphabétisation, niveau d'éducation
#   - Etudes supérieures : le taux de jeunes impliqués dans des études supérieures, ou au contraire sans diplômes
#   - L'accès à internet
#   - Marché de l'emploi : taux de chômage chez les jeunes,
#   
# Parmi les indicateurs, on peut retenir ceux ayant les sujets suivant : 
# 
# Pour la démographie et son évolution:
#    - Attainment (733)
#    - Population (213 indicateurs)
#    - Health: Population: Dynamics (1 indicateur)
#    - Health: Population: Structure (13 indicateurs)
#    
# Pour l'éducation dans le secondaire :
#    - Education Equality (426 indicateurs)
#    - Secondary (256 indicateurs)
#    
# Pour les études supérieurs (secteur tertiaire) :
#    - Tertiary (158 indicateurs)
#    - Post-Secondary/Non-Tertiary (19 indicateurs)
#    
# Pour l'accès à internet :
#    - Infrastructure: Communications (2 indicateurs)
#    
# Pour le marché de l'emploi
#    - Social Protection & Labor: Labor force structure (11 indicateurs)
#    - Laber (3 indicateurs)
#    
# On peut déjà réduire le jeu données aux indicateurs de ces sujets.  

# In[19]:


series = series[series['Topic'].isin(['Attainment','Education Equality','Infrastructure: Communications',
                                     'Education Management Information Systems (SABER)','Tertiary Education (SABER)',
                                     'Literacy','Secondary','Tertiary','Social Protection & Labor: Labor force structure',
                                     'Laber','Health: Population: Structure','Population','Health: Population: Dynamics',
                                     'Post-Secondary/Non-Tertiary'])]

print('Il reste',len(series),'indicateurs possibles')


# ## <a class="anchor" id="section_2_2">2. Sélection des indicateurs</a> 

# ###  <a class="anchor" id="section_2_2_1">a. Indicateurs démographique : population entre 15 et 24 ans</a>

# Sélectionnons en premier les indicateurs pour la démographie. La population visée étant celle pour des cours niveau lycée et fac, on peut estimée une fouchette d'âge de 15-24 ans. On s'intéresse à la population totale, indépendamment du genre, et sans contexte ou condition. On peut alors enlever les indicateurs specifique "female" et "male", "schooling", "primary","secondary","tertiary" en retirant ceux ayant un code contenant 'FE', 'MA', 'MF', 'SCHL', 'PRM','SEC'.

# In[20]:


ind_demo = series[series['Topic'].isin(['Attainment','Population','Health: Population: Structure'])]
ind_demo = ind_demo[ind_demo['Series Code'].str.contains('1524|1519|2024')]
ind_demo = ind_demo[~ind_demo['Series Code'].str.contains('FE|MA|MF|SCHL|PRM|SEC')]
#ind_demo['Series Code'].unique()
print('Il reste',len(ind_demo),'indicateurs possibles.')
ind_demo


# In[21]:


#ind_demo['Long definition'].unique()


# On pré-sélectionne trois indicateurs.

# In[22]:


ind_demo = ind_demo.loc[ind_demo['Series Code'].isin(['BAR.POP.1519','BAR.POP.2024','SP.POP.1524.TO.UN'])]
ind_demo


# In[23]:


ind_demo['Long definition'].unique()


# Les trois indicateurs sont gardés, la sélections finale se faisant avec le taux de remplissage dans le jeu de données principal.

# ### <a class="anchor" id="section_2_2_2">b. Indicateurs démographique : croissance démographique</a>

# Un indicateur pour l'évolution démographique est utile pour notre étude, une population croissante étant un marché intéressant pour les formations en ligne pour une population jeune.

# In[24]:


ind_demo_evo = series[series['Topic'] == 'Health: Population: Dynamics']
ind_demo_evo


# In[25]:


ind_demo_evo['Long definition'].unique()


# ### <a class="anchor" id="section_2_2_3">c. Indicateur d'éducation dans le secondaire</a>

# Plusieurs types d'indicateurs pour mesurer le taux de développement de l'éducation dans le secondaire existent. Pour cette étude, j'ai décidé de me concentrer sur le taux de fréquentation des établissement secondaire, privés et publics.

# In[26]:


ind_sec = series[series['Topic'].isin(['Education Equality','Secondary'])]


# On peut s'intéresser au taux de fréquentation l'éducation dans le secondaire, indépendamment du genre.

# In[27]:


ind_sec = ind_sec[ind_sec['Indicator Name'].str.contains('Secondary|secondary','Enrolment|enrolment')]
ind_sec = ind_sec[~ind_sec['Indicator Name'].str.contains('Primary|primary|Survival|female|male|expectancy|Repetition|repeaters|Drop-out|duration|Duration|Grade|grade')]
ind_sec = ind_sec[ind_sec['Series Code'].str.contains('ENRL','ENRR')]

print('Il reste',len(ind_sec),'indicateurs possibles.')
ind_sec


# On garde le premier, plus général, indépendant du genre.

# In[28]:


ind_edu_secondary = ind_sec.loc[ind_sec['Series Code']== 'SE.SEC.ENRL']
ind_edu_secondary


# ### <a class="anchor" id="section_2_2_4">d. Indicateur d'éducation dans le tertiaire</a>

# Pour les indicateurs pour les éducations dans le tertiaire, on peut s'intéresser au taux de taux de fréquentation du tertiaire, indépendamment du genre, du type d'établissement (public, private). On veut un taux global, non genré.

# In[29]:


ind_ter = series[series['Topic'] == 'Tertiary']
ind_ter = ind_ter[~ind_ter['Series Code'].str.contains('F|M')]
ind_ter = ind_ter[~ind_ter['Long definition'].str.contains('public|private|female|age|graduates')]
print('Il reste',len(ind_ter),'indicateurs possibles.')
ind_ter


# Après recherche on choisit un indicateur donnant le nombre d'étudiants pour 100 000 habitants impliqués dans des études suprérieures. 

# In[30]:


ind_edu_tertiary = ind_ter.loc[ind_ter['Series Code']== 'UIS.TE_100000.56']
ind_edu_tertiary


# In[31]:


ind_edu_tertiary['Long definition'].unique()


# ### <a class="anchor" id="section_2_2_5">e. Indicateur pour internet</a> 

# In[32]:


ind_internet = series[series['Topic'] == 'Infrastructure: Communications']
ind_internet


# Deux indicateurs sont possibles pour rendre compte de l'accès à internet. Gardons les pour le moment.

# ### <a class="anchor" id="section_2_2_5">f. Indicateur pour le marché de l'emploi</a> 

# In[33]:


ind_work = series[series['Topic'].isin(['Social Protection & Labor: Labor force structure','Laber'])]
ind_work = ind_work[~ind_work['Indicator Name'].str.contains('female|male')]
ind_work = ind_work.loc[ind_work['Series Code'].isin(['SL.TLF.TOTL.IN','SL.UEM.NEET.ZS'])]
ind_work


# In[34]:


#ind_work['Long definition'].unique()


# On garde deux indicateurs, l'un pour la force de travail à partir de 15 ans, l'autre pour la proportion de jeunes sans emplois, non impliqués dans des études supérieures ou dans une formation.

# In[35]:


indicators = pd.concat([ind_demo,ind_demo_evo,ind_edu_secondary,ind_edu_tertiary,ind_internet,ind_work],axis = 0,ignore_index = True)
indicators


# On garde finalement 10 indicateurs en tout pour la présélection.

# # <a class="anchor" id="chapter3">III. Jeu de données principal  </a>

# ## <a class="anchor" id="section_3_1">1. Nettoyage et sélection des variables</a>

# Ce fichier est le fichier principal du jeu de données. 

# In[36]:


data = pd.read_csv('EdStatsData.csv')
print('Le fichier comporte',data.shape[0],'lignes et',data.shape[1],'colonnes.')


# In[37]:


data.dtypes


# Le fichier présente les valeurs associées à un indicateur et un pays précis pour chaque année entre 1970 et 2017, puis tous les cinq ans entre 2020 et 2100. Pour l'étude menée, il n'est pas nécessaire d'étudier les données trop anciennes, les années entre 1970 et 2002 sont donc retirées. De plus, les projections ne sont pour l'instant inutiles, les années après 2017 sont également enlevées.

# In[38]:


data_subset = pd.concat([data[['Country Code','Indicator Code']],data.loc[:,"2002":"2017"]],axis = 1,ignore_index = False)
#data_subset.dtypes


# Les variables gardées sont au bon format.
# 
# Jetons un oeil aux valeurs manquantes.

# In[39]:


#On collecte le nombre de valeurs manquanets par variable
nb_na = data_subset.isnull().sum() 
print ('Ce fichier comporte',nb_na.sum(),'valeurs manquantes.' )

#On calcule le pourcentage de valeurs manquantes par variabels
index = data_subset.index
pct_manquant = pd.DataFrame(((nb_na/len(index))*100).astype(int), columns=['Pourcentage de données manquantes (%)']) 

#On trace les pourcentages de valeurs manquantes, en retirant les variables avec un pourcentages nul ou supérieur au seuil
sns.set_style("whitegrid")
pct_manquant = pct_manquant.loc[pct_manquant['Pourcentage de données manquantes (%)'] > 0]
pct_manquant.plot.bar(x=None, y=None, ylim = [0,100], sort_columns = pct_manquant['Pourcentage de données manquantes (%)'],legend=False,figsize=(10, 6))
plt.title("Pourcentage de donnée manquantes (%)",fontsize = 20)
plt.xticks(rotation=30, horizontalalignment="center",fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[40]:


column = pct_manquant["Pourcentage de données manquantes (%)"]
min_value = column.idxmin()

print('L année avec le moins de données manquantes semble être', min_value, '. Nous utiliserons cette années pour comparer les pays entre eux.') 


# In[41]:


data_subset = data_subset[['Country Code','Indicator Code','2010']]
data_subset.shape


# On peut également retirer les pays ayant une valeur nulle pour l'année de référence.

# In[42]:


data_subset = data_subset.loc[~data_subset['2010'].isnull()]
data_subset.shape


# Enfin, on retire les pays non listés dans le jeu de données des pays.

# In[43]:


list_countries = countries['Country Code'].unique()
data_subset = data_subset[data_subset['Country Code'].isin(list_countries)]
print('Le fichier comporte désormais',data_subset.shape[0],'lignes et',data_subset.shape[1],'colonnes.')


# ## <a class="anchor" id="section_3_2">2. Sélection de la variable Population Totale</a>

# Pour la suite de notre étude, la population globale sera utile. Nous allons donc la sélectionner et la conserver pour plus tard.

# In[44]:


pop_tot = series.loc[series['Series Code'] == 'SP.POP.TOTL']
pop_tot


# On sélectionne les données dans le fichier de data globale et on vérifie qu'il n'y a pas de valeurs manquantes.

# In[45]:


pop_totale = data_subset.loc[data['Indicator Code'] == 'SP.POP.TOTL']
pop_totale.isnull().sum()
#pop_totale


# ## <a class="anchor" id="section_3_3">3. Sélection finale des indicateurs</a>

# On peut désormais finir la sélection finale des indicateurs en regardant le taux de remplissage de ceux pré-sélectionnés.

# In[46]:


data_subset = data_subset.loc[data_subset['Indicator Code'].isin(indicators['Series Code'].unique())]


# On ne garde que les indicateurs dont le taux de taux de remplissage est supérieur au seuil fixé en début de code. 

# In[47]:


ind_select = data_subset['Indicator Code'].value_counts()

#On calcule le pourcentage de valeurs manquantes par variabels
index = ind_select.index
pct_remplissage = (ind_select/len(countries))*100.0
pct_remplissage

#On trace les pourcentages de valeurs manquantes, en retirant les variables avec un pourcentages nul ou supérieur au seuil
sns.set_style("whitegrid")
pct_remplissage.plot.bar(x=None, y=None, ylim = [0,100], sort_columns = pct_manquant['Pourcentage de données manquantes (%)'],legend=False,figsize = (10,6))
plt.title("Pourcentage de remplissage (%)",fontsize = 20)
plt.xticks(rotation=30, horizontalalignment="center",fontsize = 15)
plt.yticks(fontsize = 15)
line_seuil = plt.axhline(y=pct_seuil, color='r', linestyle='-')
plt.legend([line_seuil],['Seuil de remplissage'])


# In[48]:


pct_remplissage.loc[pct_remplissage>pct_seuil]
ind_final = pct_remplissage.loc[pct_remplissage>pct_seuil]
indicators_final = indicators.loc[indicators['Series Code'].isin(ind_final.index)]
print('Les indicateurs sélectionnés sont :')
indicators_final = indicators_final.reset_index(drop = True)
indicators_final


# Cependant, 8 indicateurs représente trop de données. Parmi ces indicateurs finaux nous choisiront :
#  
#   - SP.POP.1524.TO.UN : Population, ages 15-24, total
#   - SP.POP.GROW : Population growth (annual %)
#   - IT.NET.USER.P2 : Internet users (per 100 people)
#   - SE.SEC.ENRL : Enrolment in secondary education, both sexes
#   - UIS.TE_100000.56 : Enrolment in tertiary education per 100,000 in

# In[49]:


indicators_final = indicators_final.loc[indicators_final['Series Code'].isin(['SP.POP.1524.TO.UN','SP.POP.GROW','IT.NET.USER.P2','SE.SEC.ENRL','UIS.TE_100000.56'])]
indicators_final = indicators_final.reset_index(drop = True)
indicators_final


# In[50]:


indicators_final['Long definition'].unique()


# On peut alors retirer du jeu de données principal les indicateurs non retenus.

# In[51]:


data_subset = data_subset.loc[data_subset['Indicator Code'].isin(indicators_final['Series Code'].unique())]
print('Le fichier comporte désormais',data_subset.shape[0],'lignes et',data_subset.shape[1],'colonnes.')


# In[52]:


data_subset.isnull().sum()


# Il n'y a aucune valeurs manquantes.

# In[53]:


data_subset.loc[data_subset[['Country Code','Indicator Code']].duplicated(keep=False),:]


# Aucun doublon détecté.

# # <a class="anchor" id="chapter4">IV. Calcul et attribution des points par indicateur  </a>

# In[54]:


indicators_final


# ## <a class="anchor" id="section_4_1">1.  Indicateurs démographiques : population entre 15 et 24 ans</a>

# On crée le sous-ensemble avec les valeurs liées au seul indicateur de population 15/24 ans.

# In[55]:


data_subset_1524 = data_subset.loc[data_subset['Indicator Code'] == 'SP.POP.1524.TO.UN']
data_subset_1524 = data_subset_1524.rename(columns={'2010':'Pop 15-24 (2010)'})
data_subset_1524


# In[56]:


print(data_subset_1524.shape[0],'pays sont considérés.')


# In[57]:


data_subset_1524.describe()


# In[60]:


stats = data_subset_1524.describe()
name_ind = 'Pop 15-24 (2010)'
print('La moyenne pour l\'indicateur',name_ind,'est de',stats.loc['mean','Pop 15-24 (2010)'])
print('La médiane pour l\'indicateur',name_ind,'est de',stats.loc['50%','Pop 15-24 (2010)'])
print('L\'écart-type pour l\'indicateur',name_ind,'est de',stats.loc['std','Pop 15-24 (2010)'])


# In[74]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
boxprops = dict(linestyle='-', linewidth=1, color='k')
medianprops = dict(linestyle='-', linewidth=4, color='k')
meanprops = dict(marker='D', markeredgecolor='black',markerfacecolor='firebrick')

data_subset_1524.boxplot(column=['Pop 15-24 (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=True,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population entre 15 et 24 ans",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[75]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_1524.boxplot(column=['Pop 15-24 (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=False,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population entre 15 et 24 ans",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Regardons la répartition de cet indicateur en fonction des zones géographiques

# In[76]:


data_subset_1524 = data_subset_1524.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_1524.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Pop 15-24 (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), boxprops = boxprops,showfliers=True, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population entre 15 et 24 ans",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Deux valeurs semblent trop importantes comparées aux autres. Il serait sage de les considérer comme des outliers.

# In[77]:


outliers = data_subset_1524.loc[data_subset_1524['Pop 15-24 (2010)'] > 2.0e8]
outliers


# L'Inde et la Chine semblent avoir une importante population entre 15 et 24 ans. 

# In[78]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(),boxprops = boxprops, showfliers=False, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population entre 15 et 24 ans",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# L'Asie du sud et l'Amérique du Nord semblent avoir la plus importante population entre 15 et 24 ans, avec les plus hautes valeurs médianes, les plus hautes moyennes et les écart-types les plus grands.
# 
# Cependant, il pourrait être intéressant de rapporter ces valeurs de population brutes à un pourcentage de jeunes entre 15 et 24 ans par rapport à la population globale.
# 
# Pour cela, on utilise la variable pop_totale crée précédemment.

# In[79]:


for country in data_subset_1524['Country Code'].unique():
    population = pop_totale.loc[pop_totale['Country Code'] == country,'2010'].values
    jeunes = data_subset_1524.loc[data_subset_1524['Country Code'] == country,'Pop 15-24 (2010)'].values
    pct = (jeunes/population)*100
    data_subset_1524.loc[data_subset_1524['Country Code'] == country,'Pourcentage pop 15-24 (2010)'] = pct

data_subset_1524.sort_values('Pourcentage pop 15-24 (2010)',ascending=False).head(10)


# In[80]:


data_subset_1524.describe()


# In[81]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_1524.boxplot(column=['Pourcentage pop 15-24 (2010)'], boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=True,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Pourcentage de la population entre 15 et 24 ans (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[82]:


data_subset_1524 = data_subset_1524.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_1524.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Pourcentage pop 15-24 (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), boxprops = boxprops,showfliers=True, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Pourcentage de la population entre 15 et 24 ans (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Cette fois-ci, ce sont l'Asie du sud et l'Afrique Sub-Saharienne qui ont la médiane la plus haute.
# 
# Avec ce pourcentage, on peut classer les pays en fonction de la proportion de jeunes dans leur population totale, et leur accorder des points pour le classement final.
# 
# Pour calculer les points attribués à chaque pays, il a été décidé de prendre la formule suivante:
# (1 + Indicateur/max(Indicateur))
# Le score final sera calculé en multipliant les points attribués à chaque indicateur.

# In[83]:


data_subset_1524['Points pop 15-24 (2010)'] = (1+(data_subset_1524['Pourcentage pop 15-24 (2010)']/max(data_subset_1524['Pourcentage pop 15-24 (2010)'])))
data_subset_1524 = data_subset_1524.drop('Indicator Code',axis = 1)
data_subset_1524.sort_values('Points pop 15-24 (2010)',ascending=False).head(10)


# On vérifie qu'il n'y a aucune valeur manquante et aucun doublon.

# In[84]:


data_subset_1524.isnull().sum()


# In[85]:


data_subset_1524.loc[data_subset_1524[['Country Code']].duplicated(keep=False),:]


# ## <a class="anchor" id="section_4_2">2.  Indicateurs démographiques : croissance démographique</a>

# On crée le sous-ensemble avec les valeurs liées à l'indicateur pour l'évolution démographique.

# In[86]:


data_subset_growth = data_subset.loc[data_subset['Indicator Code'] == 'SP.POP.GROW']
data_subset_growth = data_subset_growth.rename(columns={'2010':'Croissance démo en % (2010)'})
data_subset_growth.describe()


# In[87]:


stats = data_subset_growth.describe()
name_ind = 'Croissance démo en % (2010)'
print('La moyenne pour l\'indicateur',name_ind,'est de',stats.loc['mean','Croissance démo en % (2010)'])
print('La médiane pour l\'indicateur',name_ind,'est de',stats.loc['50%','Croissance démo en % (2010)'])
print('L\'écart-type pour l\'indicateur',name_ind,'est de',stats.loc['std','Croissance démo en % (2010)'])


# In[88]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_growth.boxplot(column=['Croissance démo en % (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=True,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Coissance démographique en 2010(%)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[89]:


print(data_subset_growth.shape[0],'pays sont considérés.')


# Observons sa répartition géographique.

# In[90]:


data_subset_growth = data_subset_growth.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_growth.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Croissance démo en % (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), boxprops = boxprops,showfliers=True, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Coissance démographique en 2010(%)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Le Moyen Orient & l'Afrique semblent afficher la plus importante croissance démographique avec les plus hautes médianes et moyennes.

# In[91]:


data_subset_growth.sort_values('Croissance démo en % (2010)', ascending = False).head(10)


# Attribuons maintenant les points liés à cet indicateur, en employant la même méthode que précédemment. 

# In[92]:


data_subset_growth['Points croissance démo (2010)'] = (1+(data_subset_growth['Croissance démo en % (2010)']/max(data_subset_growth['Croissance démo en % (2010)'])))
data_subset_growth.loc[data_subset_growth['Points croissance démo (2010)'] < 1] == 1
#data_subset_growth = data_subset_growth.drop('Indicator Code',axis = 1)
data_subset_growth.sort_values('Points croissance démo (2010)',ascending=False).head(10)


# In[93]:


data_subset_growth.isnull().sum()


# In[94]:


data_subset_growth.loc[data_subset_growth[['Country Code']].duplicated(keep=False),:]


# ## <a class="anchor" id="section_4_3">3.  Indicateur pour l'accès à internet</a>

# On crée le sous-ensemble pour l'indicateur d'accès à internet.

# In[95]:


data_subset_internet = data_subset.loc[data_subset['Indicator Code'].isin(['IT.NET.USER.P2'])]
data_subset_internet = data_subset_internet.rename(columns={'2010':'Utilisateurs internet en % (2010)'})
data_subset_internet.describe()


# In[96]:


stats = data_subset_internet.describe()
name_ind = 'Utilisateurs internet en % (2010)'
print('La moyenne pour l\'indicateur',name_ind,'est de',stats.loc['mean','Utilisateurs internet en % (2010)'])
print('La médiane pour l\'indicateur',name_ind,'est de',stats.loc['50%','Utilisateurs internet en % (2010)'])
print('L\'écart-type pour l\'indicateur',name_ind,'est de',stats.loc['std','Utilisateurs internet en % (2010)'])


# In[97]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_internet.boxplot(column=['Utilisateurs internet en % (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=True,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Utilisateurs d'internet (%)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[98]:


print(data_subset_internet.shape[0],'pays sont considérés.')


# In[99]:


data_subset_internet = data_subset_internet.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_internet.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Utilisateurs internet en % (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), showfliers=True,boxprops = boxprops, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Utilisateurs d'internet (%)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# L'Europe, l'Asie centrale et l'Amérique du Nord semblent être majoritairement avantagées avec les plus hautes médianes.

# In[100]:


data_subset_internet.sort_values('Utilisateurs internet en % (2010)', ascending = False).head(10)


# Attribuons maintenant les points liés à cet indicateur, en employant la même méthode que précédemment. 

# In[101]:


data_subset_internet['Points internet (2010)'] = (1+(data_subset_internet['Utilisateurs internet en % (2010)']/max(data_subset_internet['Utilisateurs internet en % (2010)'])))
data_subset_internet = data_subset_internet.drop('Indicator Code',axis = 1)
data_subset_internet.sort_values('Points internet (2010)',ascending=False).head(10)


# In[102]:


data_subset_internet.isnull().sum()


# In[103]:


data_subset_internet.loc[data_subset_internet[['Country Code']].duplicated(keep=False),:]


# ## <a class="anchor" id="section_4_4">4. Indicateur pour l'éducation dans le secondaire</a>

# On crée le sous-ensemble pour l'indicateur pour l'éducation dans le secondaire.

# In[104]:


data_subset_edu_sec = data_subset.loc[data_subset['Indicator Code'].isin(['SE.SEC.ENRL'])]
data_subset_edu_sec = data_subset_edu_sec.rename(columns={'2010':'Population 15-24 inscrite dans secondaire (2010)'})
data_subset_edu_sec.describe()


# In[105]:


stats = data_subset_edu_sec.describe()
name_ind = 'Population 15-24 inscrite dans secondaire (2010)'
print('La moyenne pour l\'indicateur',name_ind,'est de',stats.loc['mean','Population 15-24 inscrite dans secondaire (2010)'])
print('La médiane pour l\'indicateur',name_ind,'est de',stats.loc['50%','Population 15-24 inscrite dans secondaire (2010)'])
print('L\'écart-type pour l\'indicateur',name_ind,'est de',stats.loc['std','Population 15-24 inscrite dans secondaire (2010)'])


# In[106]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_edu_sec.boxplot(column=['Population 15-24 inscrite dans secondaire (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=True,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population 15-24 inscrite dans secondaire (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[107]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_edu_sec.boxplot(column=['Population 15-24 inscrite dans secondaire (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, showfliers=False,patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population 15-24 inscrite dans secondaire (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[108]:


print(data_subset_edu_sec.shape[0],'pays sont considérés.')


# In[109]:


data_subset_edu_sec = data_subset_edu_sec.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_edu_sec.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Population 15-24 inscrite dans secondaire (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), showfliers=True, boxprops = boxprops,medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population 15-24 inscrite dans secondaire (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# Deux valeurs semblent trop importantes comparées aux autres. Il serait sage de les considérer comme des outliers.

# In[110]:


outliers = data_subset_edu_sec.loc[data_subset_edu_sec['Population 15-24 inscrite dans secondaire (2010)'] > 0.8e8]
outliers


# Encore une fois, l'Inde et la Chine.

# In[111]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), showfliers=False, boxprops = boxprops,medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Population 15-24 inscrite dans secondaire (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# L'Amérique du nord et l'Asie du sud devant les autres régions, avec les plus ahutes valeurs, médianes et moyennes. 
# 
# Comme pour la population 15/24 il pourrait être intéressant de calculer le pourcentage de jeunes entre 15 et 24 ans inscrits dans le secondaire. Cependant, les variables Population 15-24 (2010) et Population 15-24 inscrite dans secondaire (2010) semblent avoir une longue liste de pays non en commun. 

# In[112]:


no_value_countries = []
for country in data_subset_edu_sec['Country Code'].unique():
    if country not in data_subset_1524['Country Code'].unique():
        no_value_countries.append(country)
len(no_value_countries)
no_value_countries


# 12 pays devront être écartésn ce qui constitue presque 10% des pays considérés pour cet indicateur. On garde donc la population pour attribuer les points. 

# In[113]:


data_subset_edu_sec['Points secondaire (2010)'] = (1+(data_subset_edu_sec['Population 15-24 inscrite dans secondaire (2010)']/max(data_subset_edu_sec['Population 15-24 inscrite dans secondaire (2010)'])))
data_subset_edu_sec = data_subset_edu_sec.drop('Indicator Code',axis = 1)
data_subset_edu_sec.sort_values('Points secondaire (2010)',ascending=False).head(10)


# In[114]:


data_subset_edu_sec.isnull().sum()


# In[115]:


data_subset_edu_sec.loc[data_subset_edu_sec[['Country Code']].duplicated(keep=False),:]


# ## <a class="anchor" id="section_4_5">5. Indicateur pour l'éducation dans le tertiaire</a>

# On crée le sous-ensemble pour l'indicateur pour l'éducation dans le tertiaire.

# In[116]:


data_subset_edu_ter = data_subset.loc[data_subset['Indicator Code'].isin(['UIS.TE_100000.56'])]
data_subset_edu_ter = data_subset_edu_ter.rename(columns={'2010':'Pop inscrite dans tertiaire pour 100,000 (2010)'})
data_subset_edu_ter.describe()


# In[117]:


stats = data_subset_edu_ter.describe()
name_ind = 'Pop inscrite dans tertiaire pour 100,000 (2010)'
print('La moyenne pour l\'indicateur',name_ind,'est de',stats.loc['mean','Pop inscrite dans tertiaire pour 100,000 (2010)'])
print('La médiane pour l\'indicateur',name_ind,'est de',stats.loc['50%','Pop inscrite dans tertiaire pour 100,000 (2010)'])
print('L\'écart-type pour l\'indicateur',name_ind,'est de',stats.loc['std','Pop inscrite dans tertiaire pour 100,000 (2010)'])


# In[118]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
data_subset_edu_ter.boxplot(column=['Pop inscrite dans tertiaire pour 100,000 (2010)'],boxprops = boxprops,medianprops=medianprops,vert=True, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Pop inscrite dans tertiaire pour 100,000 (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[119]:


print(data_subset_edu_ter.shape[0],'pays sont considérés.')


# In[120]:


data_subset_edu_ter = data_subset_edu_ter.merge(countries[['Country Code','Region']],how='left')
grouped = data_subset_edu_ter.groupby(['Region'])
df2 = pd.DataFrame({col:vals['Pop inscrite dans tertiaire pour 100,000 (2010)'] for col,vals in grouped})
meds = df2.median()
meds.sort_values(ascending=False, inplace=True)
df2 = df2[meds.index]

sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
df2.boxplot(labels=countries['Region'].unique(), showfliers=True,boxprops = boxprops, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Taux de fréquentation pour l'éducation tertiaire (pour 100,000 pers)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# L'Amérique du nord, L'asie de l'est et Pacifique sont en tête des régions.

# In[121]:


data_subset_edu_ter.sort_values('Pop inscrite dans tertiaire pour 100,000 (2010)', ascending = False).head(10)


# On attribue les points aux pays pour cet indicateur.

# In[122]:


data_subset_edu_ter['Points tertiaire (2010)'] = (1+(data_subset_edu_ter['Pop inscrite dans tertiaire pour 100,000 (2010)']/max(data_subset_edu_ter['Pop inscrite dans tertiaire pour 100,000 (2010)'])))
data_subset_edu_ter = data_subset_edu_ter.drop('Indicator Code',axis = 1)
data_subset_edu_ter.sort_values('Points tertiaire (2010)',ascending=False).head(10)


# In[123]:


data_subset_edu_ter.isnull().sum()


# In[124]:


data_subset_edu_ter.loc[data_subset_edu_ter[['Country Code']].duplicated(keep=False),:]


# # <a class="anchor" id="chapter5">V. Classement final des pays et conclusion de l'analyse  </a>

# Calculons le score final pour les pays.
# 
# Associons les données dans un seul jeu de données. 

# In[125]:


final_class = countries.merge(data_subset_1524[['Country Code','Points pop 15-24 (2010)']], how = 'left')
final_class = final_class.merge(data_subset_growth[['Country Code','Points croissance démo (2010)']], how = 'left')
final_class = final_class.merge(data_subset_internet[['Country Code','Points internet (2010)']], how = 'left')
final_class = final_class.merge(data_subset_edu_sec[['Country Code','Points secondaire (2010)']], how = 'left')
final_class = final_class.merge(data_subset_edu_ter[['Country Code','Points tertiaire (2010)']], how = 'left')
final_class.head(3)


# In[126]:


#final_class['Country Code'].value_counts()


# In[127]:


final_class['Score Total (2010)'] = final_class['Income Point'] * final_class['Points pop 15-24 (2010)'] * final_class['Points croissance démo (2010)'] * final_class['Points internet (2010)'] * final_class['Points secondaire (2010)'] * final_class['Points tertiaire (2010)']
final_class.sort_values('Score Total (2010)', ascending = False).head(10)


# Regardons en détail les 10 premiers pays.

# In[128]:


final_class = final_class.sort_values('Score Total (2010)', ascending = False)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(17,10))
sns.barplot(x = 'Score Total (2010)',y = 'Short Name',data=final_class.iloc[:20],palette="Blues_d")
plt.title("Score final des 20 pays en tête",fontsize = 25)
plt.xticks(fontsize = 15)
plt.xlabel('Score final',fontsize = 15)
plt.yticks(fontsize = 15)
plt.ylabel('',fontsize = 20)
plt.show()


# In[129]:


sns.set_style("white")
final_class_rep = final_class[['Short Name','Region','Income Point','Points pop 15-24 (2010)','Points croissance démo (2010)','Points internet (2010)','Points secondaire (2010)','Points tertiaire (2010)']].iloc[:10]
final_class_rep.set_index("Short Name",drop=True,inplace=True)
final_class_rep.plot.bar(stacked=True, rot = 50,figsize=(10, 7),ylim = [0,13])
plt.title("Répartition des points (2010)",fontsize = 20)
plt.xticks(fontsize = 15)
plt.xlabel('',fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[130]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,8))
boxprops = dict(linestyle='-', linewidth=1, color='k')
final_class_ind = final_class[['Short Name','Region','Income Point','Points pop 15-24 (2010)','Points croissance démo (2010)','Points internet (2010)','Points secondaire (2010)','Points tertiaire (2010)']]
final_class_ind.boxplot(boxprops = boxprops,showfliers=True, medianprops=medianprops,vert=False, patch_artist=True, showmeans=True, meanprops=meanprops)
plt.title("Indicateurs normalisés",fontsize = 20)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.show()


# In[131]:


final_class_10 = final_class[:10]
final_class_10['Region'].value_counts()


# Les régions à favoriser semblent être: 
# 
#  - **L'Asie de l'Est et le Pacifique**, regroupant la Corée, la Nouvelle-Zélande, l'Australie et Macao
#  - **L'Europe**, regroupant l'Islande, la Norvège, la Finlande et la Suède.
#  
#  Mais il semblerait également que les **Etats-Unis** et **Israël** soient de potentiels candidats. 

# In[ ]:




