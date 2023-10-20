import streamlit as st
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.join(Path(__file__).parents[1]))
from model import Model
m = Model()

# Here is the actual contents of the page:
st.title('Recommendation Page')
card_name = st.text_input(
    "Please enter the full name of the card you wish to see recommendations for:"
)

if st.button('Submit Card'):
    try:
        st.image(m.img_return(card_name))
        img_list = m.recommended_cards(card_name)
        st.write(
            f'''Here are the {len(img_list)} cards 
            that would be recommended for a deck with the card {card_name} in it:'''
        )
        col1, col2, col3 = st.columns(3)
        col1.image(img_list[0:4])
        col2.image(img_list[4:8])
        col3.image(img_list[8:11])
    except BaseException:
        st.error('''
                {card_name.title()} is not a valid card name.
                 Please try again with a valid card name. If the 
                 card name you entered is VALID, please try typing it the EXACT way
                 it appears on the face of the card.
                ''')