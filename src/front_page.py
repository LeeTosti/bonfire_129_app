import streamlit as st

st.title('Bonfire-129 MTG Tracer Application')
st.text('My first application that utlizes Pandas, Streamlit, SpaCy, MongoDB, and Python to create a MTG Recommendation System')

st.header('Here are the different pages of my application:')
st.subheader('Image Return:')
st.text('Image Return: Returns an image of the requested card')

st.subheader('Summary:')
st.text('Summary Page, explaining all the inner workings of my application and the "why" behind decisions we made')

st.subheader('Query')
st.text('Query: Allows a user to ender a card name and queries the database in mongo for all info matching that card name. Card names MUST be exact')

st.subheader('Recommender')
st.text('A recommendation system that we will build to allow users to see recommended cards')

st.subheader('Vis')
st.text('Vis: Ability to create a couple of visualizations in Plotly')