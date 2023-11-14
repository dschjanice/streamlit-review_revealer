import streamlit as st

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
# )

st.set_page_config(layout="wide")
## add a title
st.title('ReviewRevealer')
## add text in markdown
st.write('We are showing ChatGPT Reviews for iOS and Android')

st.markdown(
    """
    This dashboard shows the final result of our capstone project for the SPICED Academy Data Science Bootcamp.
    
    
    **👈 Select a section from the sidebar** to have a look into our work.
    
    
    
    ### Want to learn more?
    - Feel free to contact us on LinkedIn.
    
    
    
    
    #### We wish you much fun while scrolling through the results.
    #### Andrii, Martje and Janice.

"""
)