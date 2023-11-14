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
## add text in markdown
st.write('We are showing ChatGPT Reviews for iOS and Android')

# Load df
df_raw = pd.read_csv("/Users/janice/Documents/Bootcamp/Git/Capstone/capstone_chat-gpt/data/chatgpt-combined_short_topics.csv")
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


if st.toggle('Show the topic overview'):
    # Read file and keep in variable
    with open("/Users/janice/Documents/Bootcamp/Git/Capstone/capstone_chat-gpt/charts/visualize_docs.html" ,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    components.html(html_data, height=800)

## Plots
c1 = '#c0791b'
c2 = '#1b786e'
c3 = '#424242'
c4 = '#5f5f5f'
c5 = '#202112'
f = 16

## absolute numbers
col1_1, col1_2= st.columns(2)
with col1_1:
    for var in ['category']:
        list=[]
        for i in range(1,6,1):
            x = df[var].unique()[i-1] if df[var].nunique() >= i else ''
            list.append(x)
        fig = px.histogram(df.sort_values(var), 
            x=var,
            title="Number of Reviews by " + var.capitalize(),
            labels={'count': 'Reviews'},
            text_auto=True,
            template='ggplot2',
            hover_data={"at_ym": "|%B %d, %Y"},
            color=var,
            color_discrete_map={
                list[0]: c1, 
                list[1]: c2, 
                list[2]: c3, 
                list[3]: c4,     
                list[4]: c5
                })
        fig.update_traces(textposition='auto')
        fig.update_layout(
            height=300,
            legend_title_text=var.capitalize(),
            font=dict(size=f),
            xaxis_title="Category",
            xaxis_title_font_size=f,
            xaxis_tickfont_size=f,
            yaxis_title="Reviews",
            yaxis_title_font_size=f,
            yaxis_tickfont_size=f, 
            legend_font_size=f,
            legend_title = dict(font = dict(size = f)))
        fig.update_xaxes(
            dtick="M2",
            tickformat="%B\n%Y")
        st.plotly_chart(fig, use_container_width=True,height=800)
        
with col1_2:    
    #apparently you dont need to write st.write and just “” as magic commands
    if st.checkbox(f'Push this button to show sample dataframe.'): # {appversion}'):
        st.write(df[['Source', 'content', 'category', 'Label']].sample(10))
    