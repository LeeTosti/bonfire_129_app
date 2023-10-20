#Import for the image return page
import streamlit as st
import requests
import os
import sys
from PIL import Image
from pathlib import Path
from io import BytesIO
import pandas as pd
import ast

folder_dir = os.path.join(Path(__file__).parents[1], 'data')

df = pd.read_csv(f'{folder_dir}/oracle_cards.csv', low_memory=False)

# When I go to click on the page:
st.title('Image Return Page')

# Then we take an input from the user:
answer= st.text_input("Enter a Card Name:", value='Sol Ring')


s = df[df['name'] == answer]['image_uris']
print(s.index[0])
img_dic = ast.literal_eval(s.loc[s.index[0]])
img_str = img_dic['normal']
response = requests.get(img_str)

# Transform that into a query
#card = list(c.cards.find({'name': answer}))[0]['image_uris']['normal']
#making this a list helps work with this easier and the indexing calls our response, then then we call to 
#our key value

img = Image.open(BytesIO(response.content))
st.image(img)