import streamlit as st

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

st.set_page_config(layout="wide")
## add a title
st.title('ReviewRevealer')

st.markdown(
    """
    ### Welcome to the ReviewRevealer Dashboard! 
    Interested in gaining quantitative insights from app reviews? 
    This dashboard as a combination of a sentiment analysis based on zero-shot-classification with the results of BERTopic topic modeling provides a great overview over the most important and most frequently discussed positive and negative issues of the ChatGPT app for iOS and Android users between May and November 2023. 
    On the first page you can find some general sentiment statistics and an overview over the topic landscape. On the second page you can deep-dive into single topics and take a look at how discussions on a specific topic evolve over time. 
    
    **👈 Select a section from the sidebar** to have a look into our work.

    ### Background Info
    This dashboard is part of the data science project “ReviewRevealer: App review analysis through sentiment analysis and topic modeling on the example of ChatGPT” by Janice Schönfeld, Andrii Ivanytskyi, and Martje Buss (last updated: 22.11.2023) from the SPICED Academy Data Science Bootcamp, cohort: Rice Regression.

    **GitHub Repositories**
    - Data Analysis: https://github.com/dschjanice/App-Review-Analysis
    - Dashboard: https://github.com/dschjanice/streamlit-review_revealer

    **Want to learn more?**
    Feel free to contact us on LinkedIn! 
    
    #### Now it's on you to unravel the mystery of what's behind the 30k+ app reviews we analyzed! Feel free to click through our dashboard and have fun! 🕵️😊

"""
)