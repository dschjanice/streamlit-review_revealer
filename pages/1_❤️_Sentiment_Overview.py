## run the app by tiping in the terminal
# streamlit run notebooks/streamlit_app.py  --theme.base="light"  --theme.primaryColor="#1b786e"  --theme.backgroundColor="#eeeeee" --theme.secondaryBackgroundColor="#f7f7f7" --theme.textColor="#424242" --theme.font="sans serif"

import streamlit as st
from streamlit_dynamic_filters import DynamicFilters
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import pickle
import time
from matplotlib import pyplot as plt
from  matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import datetime as dt
from datetime import datetime
import seaborn as sns

st.set_page_config(layout="wide")
## add a title
st.title('ReviewRevealer')

# Load df
df_raw = pd.read_csv("data/chatgpt-combined_short_topics.csv")
df_raw['appVersion'] = df_raw['appVersion'].replace(np.nan, "not available")
df_raw["Operating System"] = np.where(df_raw.Source == 'Apple', "iOS", "Android")
df_raw['at_dt'] = pd.to_datetime(df_raw['at'])
df_raw['Stars'] = '⭐'
df_raw['Stars'] = df_raw['Stars'] * df_raw['score'] 

with st.sidebar:
    st.write("Filter the shown data")
    df_source = df_raw
    df_app = df_raw
    if st.toggle('Select iOS or Android Reviews'):
        source = st.selectbox("Filter here on the operating system", df_raw['Operating System'].sort_values().unique())
        df_source = df_raw[df_raw['Operating System'].isin([source])]
        df_app = df_source
        if source == 'Android':
            appversion = st.multiselect(
                "Filter here on the Android AppVersion", 
                df_source['appVersion'].sort_values().unique(),
                default=list(df_app['appVersion'].sort_values().unique()))
            df_app = df_source[df_source['appVersion'].isin(appversion)]

    category = st.multiselect(
        "Filter here on the Sentiment of the Review", 
        df_app['category'].sort_values().unique(), 
        default=list(df_app['category'].sort_values().unique()))

    review_date = st.date_input(
        "Review Date Range", 
        (df_app['at_dt'].min(), 
        df_app['at_dt'].max()),
        key='#date_range',)

df_cat = df_app[df_app['category'].isin(category)]
df = df_cat.loc[(pd.to_datetime(df_cat['at']) >= pd.to_datetime(review_date[0])) & (pd.to_datetime(df_cat['at']) <= pd.to_datetime(review_date[1]))]

## Plots
#c1 = '#c0791b'
c1 = '#86e5be'
# c2 = '#1b786e'
c2 = '#ff95c0'
#c3 = '#424242'
c3 = '#ffd495'
c4 = '#5f5f5f'
c5 = '#202112'
f = 16

## absolute numbers
col1_1, col1_2= st.columns(2)
with col1_1:
    for var in ['category']:
        df_chart = df.groupby([var]).size().reset_index(name='Reviews')
        df_chart['Reviews (%)'] = df_chart['Reviews'].transform(lambda x: x / x.sum())
        df_chart = df_chart.sort_values(var, ascending = False)
        df_chart['helper'] = df_chart['Reviews (%)'].round(2)
        df_chart['helper'] = pd.Series(["{0:.1f}%".format(val * 100) for val in df_chart['helper']], index = df_chart.index)
        df_chart['helper'] = df_chart['Reviews'].astype(str) + '<br />(' + df_chart['helper'] + ')'
        list=[]
        for i in range(1,6,1):
            x = df_chart[var].unique()[i-1] if df_chart[var].nunique() >= i else ''
            list.append(x)
        fig = px.bar(df_chart, 
            x=var,
            y='Reviews',
            title="Proportion of Reviews by Sentiment " + var.capitalize(),
            text='helper',
            template='ggplot2',
            color=var,
            color_discrete_map={
                list[0]: c1, 
                list[1]: c3, 
                list[2]: c2, 
                list[3]: c4,     
                list[4]: c5
                }, 
            #histnorm = "percent"
            )
        fig.update_layout(
            height=300,
            legend_title_text=var.capitalize(),
            font=dict(size=f),
            xaxis_title="Sentiment",
            xaxis_title_font_size=f,
            xaxis_tickfont_size=f,
            yaxis=dict(visible=False), 
            showlegend = False)
        st.plotly_chart(fig, use_container_width=True,height=800)
        
with col1_2:    
    #apparently you dont need to write st.write and just “” as magic commands
    if st.checkbox(f'Push this button to show sample dataframe.'): # {appversion}'):
        st.write(df[['Source', 'Original content', 'category', 'Label']].sample(10))
    

col5_1, col5_2 = st.columns(2)
with col5_1:
    st.write(f':+1: **Top 5 Highlights**')
    st.write(f'Here you can see some trending topics that are getting the highest positive attention among users.')
    st.dataframe(df[df['category'] == "positive"].groupby('Label')['thumbsUpCount'].sum().reset_index().sort_values('thumbsUpCount', ascending=False)[['Label', 'thumbsUpCount']].head(5),
            use_container_width=True,
            column_config={
            "Label": st.column_config.Column(
            "Most Popular Positive"), "thumbsUpCount": st.column_config.Column("Likes")},
            hide_index=True)
    st.write(f'**Trending positive reviews**')
    st.dataframe(df[df['category'] == "positive"].sort_values('thumbsUpCount', ascending=False)[['Original content']].head(5), 
                 use_container_width=True,
                 column_config={"Original content": st.column_config.Column(
                 "Review")},
                 hide_index=True)
        
with col5_2:
    st.write(f':-1: **Top 5 Painpoints**')
    st.write(f'Here you can see some trending topics that are getting the highest negative attention among users.')
    st.dataframe(df[df['category'] == "negative"].groupby('Label')['thumbsUpCount'].sum().reset_index().sort_values('thumbsUpCount', ascending=False)[['Label', 'thumbsUpCount']].head(5),
        use_container_width=True,
        column_config={
        "Label": st.column_config.Column(
        "Most Popular Negative"), "thumbsUpCount": st.column_config.Column("Likes")},
        hide_index=True)
    st.write(f'**Trending negative reviews**')
    st.dataframe(df[df['category'] == "negative"].sort_values('thumbsUpCount', ascending=False)[['Original content']].head(5), 
                 use_container_width=True,
                 column_config={"Original content": st.column_config.Column(
                 "Review")},
                 hide_index=True)
