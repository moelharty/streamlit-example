import streamlit as st

import altair as alt
from vega_datasets import data

import pandas as pd
import numpy as np


df = pd.read_csv('df.csv')
print(df)
st.title('world happiness')
st.markdown(
"""
In this demo, we are going to analyze world happiness report data. You can filter the dataset in the sidebar.  
"""
)

# Sidebar Controls
st.sidebar.header('Filter Data:')
year = st.sidebar.slider('Year', 2015, 2019, (2015,2019))
Continent = st.sidebar.multiselect('Continent', ['Europe', 'North America', 'Oceania','Asia','South America','Africa'], ['Europe', 'North America', 'Oceania','Asia','South America','Africa'])
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
#Filter data by sidebar inputs:
#data = df[(df['Year'].isin(year)) & (df['Continent'].isin(Continent))]

data = df[(df['Year'].dt.year.between(year[0],year[1])) & (df['Continent'].isin(Continent))]
print(data)



# Summary of selected data
chart = alt.Chart(data).mark_bar().encode(
    Y='Happiness Score',
    x='Year',
    color='Continent'
).properties(
    width=300,
    height=200
) | alt.Chart(data).mark_bar().encode(
    y='Continent',
    x='Freedom',
    color='Continent'
).properties(
    width=300,
    height=200
)

chart


st.markdown('## Projection of world happiness')

projdf = data.dropna().reset_index(drop=True)

features = st.multiselect('Features to project:', ["Freedom", "Generosity",'Happiness Rank','Happiness Score','Social Support','Life Expectancy'], ["Freedom", "Generosity",'Happiness Rank','Happiness Score','Social Support','Life Expectancy'])
method_name = st.selectbox('Projection method:', ('PCA', 'MDS', 'TSNE'))

projData = projdf.drop(projdf.columns.difference(features), axis=1)

projData

from sklearn import manifold
from sklearn import decomposition


if method_name == 'PCA':
  method = decomposition.PCA(n_components=2)

if method_name == 'MDS':
  method = manifold.MDS(n_components=2)

if method_name == 'TSNE':
  perplexity = st.slider('Perplexity', 10, 100, 30)
  method = manifold.TSNE(n_components=2, perplexity=perplexity)

  

placeholder = st.empty()
placeholder.text('calculating...')
  

pos = pd.DataFrame(method.fit_transform(projData), columns=['x','y'])
projdf = pd.concat([projdf, pos.reset_index(drop=True)], axis='columns')

placeholder.empty()
color = st.selectbox('Color by:', ('Continent','Country', "Freedom", "Generosity",'Happiness Rank','Social Support','Life Expectancy'))
# We use a point as mark
chart = alt.Chart(projdf).mark_point().encode(
    x='x',
    y='y',
    color=color
).properties(
    width=600,
    height=600
)
chart

projdf
