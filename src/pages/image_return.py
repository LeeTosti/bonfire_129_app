#Import for the image return page
import streamlit as st
import requests
import os
import sys
from PIL import Image
from pathlib import Path
from io import BytesIO

# Create file path to system where the main folder for the applicaiton lives
sys.path.insert(0, os.path.join(Path(__file__).parents[1]))

#Import the created class from our file
from to_mongo import ToMongo

# When I go to click on the page:
st.title('Image Return Page')

# Create and instance of our Mongo Class:
c = ToMongo()

# Then we take an input from the user:
answer= st.text_input("Enter a Card Name:", value='Sol Ring')


print(list(c.cards.find({'name': answer})))
# Transform that into a query
card = list(c.cards.find({'name': answer}))[0]['image_uris']['normal']
#making this a list helps work with this easier and the indexing calls our response, then then we call to 
#our key value
st.image(Image.open(BytesIO(requests.get(card).content)))