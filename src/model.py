from pathlib import Path
from PIL import Image
from io import BytesIO
import pandas as pd
import pickle
import ast
import os
import re
import requests

# First step: Establish a folder directory
folder_dir = os.path.join(Path(__file__).parents[0], 'data')

class Model:

    def __init__(self):
        # Instantiate the DataFrame object:
        self.df = pd.read_csv(f'{folder_dir}/oracle_cards.csv', low_memory=False)
        #Load in our pretrained model:
        self.nnm = pickle.load(open(f'{folder_dir}/pipe.pk', 'rb'))
        # Creating a list of our own stop words:
        self.stop_words = ['on', 'the', 'of', 'and', 'to']
        self.cap_stop_words = [w.title() for w in self.stop_words]

    def card_name_fix(self, card_name:str):
        # Create the string object, parse it, fix it, then return it:
        self.string = re.sub(
            r"[A-Za-z]+('[A-Za-z]+)?",
            lambda x: x.group(0)[0].upper() + 
            x.group(0)[1:].lower() if x.group(0) not in self.stop_words or self.cap_stop_words and card_name.startswith(x.group(0)) else x.group(0).lower(),
            card_name
        )
        
        # Split the string:
        self.split_str = self.string.split()
        c = 0
        for name in self.split_str:
            if '-' in name:
                name = name.title()
                c +=1
            elif name[1] == "'":
                name = name[0:3].upper() + name[3:]
                self.split_str[c] = name
                c +=1
            else:
                c += 1
        return " ".join(self.split_str)
    
    def nn(self, card_name:str):
        self.card_name = self.card_name_fix(card_name)
        self.i = self.nnm.named_steps['nearestneighbors'].kneighbors(
            self.nnm.named_steps['tfidfvectorizer'].transform(
                self.df['lemmas'][self.df['name'] == self.card_name]
            ),
            return_distance=False
        )
        return [self.df['name'][index] for index in self.i[0] if index != self.df[self.df['name'] ==self.card_name].index]
    
    def img_return(self, card_name:str):
        img_uri = self.df[self.df['name'] == self.card_name_fix(card_name)]['image_uris']
        for k in img_uri:
            img_dic = ast.literal_eval(k)
        img_str = img_dic['normal']
        respone = requests.get(img_str)
        return Image.open(BytesIO(respone.content))
    
    def recommended_cards(self, card_name:str):
        names = self.nn(card_name)
        return [self.img_return(name) for name in names]

if __name__ == '__main__':
    c = Model()
    print(c.card_name_fix('sol ring'))
    print(c.nn('Sol Ring'))


