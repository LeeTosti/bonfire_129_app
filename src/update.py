import pandas as pd
from pathlib import Path
from base import Base
from to_mongo import ToMongo
import re
import spacy
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pickle

# Set our folder directory
folder_dir = f"{Path(__file__).parents[0]}/data"


Base().df.to_csv(f'{folder_dir}/oracle_cards.csv', index=False)
print('Saved New Cards Data to CSV File')

ToMongo().drop_collection()
print('Successfully Dropped all Items in Collection')
ToMongo().upload_one_by_one()
print('Successfully Updated Collection with New Data')

# Read in the dataframe from the csv:
df = pd.read_csv(f'{folder_dir}/oracle_cards.csv', low_memory=False)
print('Created the DataFrame object')

# Drop all null values and any empty strings as well
df.dropna(subset=['oracle_text'], axis=0, inplace=True)
df.drop(df.index[df['oracle_text'] == ''], inplace=True)
print('Dropped all values that were either null or empty')

#Use regex, remove all non alpha-numerical values from the column:
df['oracle_text'] = [re.sub('[^0-9a-zA-Z]+', ' ', i)for i in df.oracle_text]
print('Regex was successful! Thank God')

nlp = spacy.load('en_core_web_md')
lemmas = []
for doc in df['oracle_text']:
    lemmas.append([token.lemma_.lower().strip() for token in nlp(str(doc)) if (token.is_stop != True) and (token.is_punct != True) and (token.is_space !=True) and (len(token) > 2)])

df['lemmas'] = lemmas
print('Successfully Created a Lemma Column in a DataFrame Object!')

# Save back over the csv file with the new lemma column:
df.to_csv(f'{folder_dir}/oracle_cards.csv', index=False)

#Create the dummy function
#def dummy_fun(doc):
    #return doc

# Create the pipeline object:
pipe = make_pipeline(
    TfidfVectorizer(),
    NearestNeighbors(n_neighbors=12)
)

pipe.fit(df['lemmas'].astype(str))
pickle.dump(pipe, open(f'{folder_dir}/pipe.pk', 'wb'))
print('Create the pipeline and save it to a file')