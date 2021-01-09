import streamlit as st

import altair as alt


import pandas as pd
import numpy as np

# Streamlit
# Page: https://www.streamlit.io/
# Repo: https://github.com/streamlit/streamlit
# Author: Adrian Treuille (https://www.streamlit.io/about)
#   * Prof @ Carnegie Mellon University 
#   * Google X
#   * ZOOX (Self Driving Cars)
#   * Streamlit

df = pd.read_csv('df.csv')

st.title('world happiness')
st.markdown(
"""
In this demo, we are going to analyze world happiness report data. You can filter the dataset in the sidebar.  
Selected Cars:
"""
)

# Sidebar Controls
st.sidebar.header('Filter Data:')
year = st.sidebar.slider('Year', 2015, 2019, (2015,2019))
origin = st.sidebar.multiselect('Continent', ['Europe', 'North America', 'Oceania','Asia','South America','Africa'], ['Europe', 'North America', 'Oceania','Asia','South America','Africa'])

# Filter data by sidebar inputs:
df = df[(df['Year'].dt.year.between(year[0],year[1])) & (df['Origin'].isin(origin))]
df

# Summary of selected data
chart = alt.Chart(cars).mark_bar().encode(
    x='count()',
    y='Origin',
    color='Origin'
).properties(
    width=300,
    height=200
) | alt.Chart(cars).mark_bar().encode(
    alt.X("year(Year):N"),
    y='count()',
    color='Origin'
).properties(
    width=300,
    height=200
)
chart

st.markdown('## Projection of cars')

projcars = df.dropna().reset_index(drop=True)

features = st.multiselect('Features to project:', ["Freedom", "Generosity",'Happiness Rank','Happiness Score','Socia Support','Life Expectancy','Year'], ["Freedom", "Generosity",'Happiness Rank','Happiness Score','Socia Support','Life Expectancy','Year'])
method_name = st.selectbox('Projection method:', ('PCA', 'MDS', 'TSNE'))

projData = projcars.drop(projcars.columns.difference(features), axis=1)

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
projcars = pd.concat([projcars, pos.reset_index(drop=True)], axis='columns')

placeholder.empty()
color = st.selectbox('Color by:', ("Freedom", "Generosity",'Happiness Rank','Happiness Score','Socia Support','Life Expectancy','Year'))
# We use a point as mark
chart = alt.Chart(projcars).mark_point().encode(
    x='x',
    y='y',
    color=color
).properties(
    width=600,
    height=600
)
chart

projcars
