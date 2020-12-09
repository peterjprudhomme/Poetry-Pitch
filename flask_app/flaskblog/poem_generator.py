# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 17:26:07 2020

@author: peter
"""


import numpy as np
import pandas as pd
import pickle
from random import randint
import re
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
import string


np.random.seed(42)
'''
Need to make rand_poem depend on imported dataframe
'''
poem_raw = pd.read_csv("PoetryFoundationData.csv")
del poem_raw['Unnamed: 0']

#remove empty duplicate poems and reset index
poem_raw = poem_raw.drop_duplicates('Poem', False).reset_index(drop = True)

#remove tageless poems and reset index
poem_raw = poem_raw.drop_duplicates('Tags', False).reset_index(drop = True)

#make grouped tag strings a list of tags
tags_to_list = lambda tags: tags.replace('Seas, Rivers, & Streams', 'Seas & Rivers & Streams').split(',')
poem_raw.Tags = poem_raw.Tags.apply(tags_to_list)

# add word_count column
poem_raw['Word_count'] = poem_raw.Poem.map(lambda poem: len([term for term in poem.split(' ') if term != '']))
scl = MinMaxScaler()
poem_raw['Word_count_scaled'] = scl.fit_transform(poem_raw.Word_count.values.reshape(-1, 1))

# add scaled line_count column
line_count_func = lambda poem: len([line for line in poem.split('\r\r\n')])
poem_raw['Line_count'] = poem_raw.Poem.apply(line_count_func)
scl = MinMaxScaler()
poem_raw['Line_count_scaled'] = scl.fit_transform(poem_raw.Line_count.values.reshape(-1, 1))

# add scaled average word length column
def get_average_word_length(poem):
    poem = poem.replace('\r', ' ').replace('\n', ' ')
    poem = re.sub('[%s]' % re.escape(string.punctuation), ' ', poem.lower())
    word_lengths = [len(word) for word in poem.split(' ') if word != '']
    if not word_lengths: # fix this later, there is at least one empty poem in the dataset
        word_lengths.append(1)
    return sum(word_lengths)/len(word_lengths)
    

poem_raw['Ave_word_length'] = poem_raw.Poem.apply(get_average_word_length)
scl = MinMaxScaler()
poem_raw['Ave_word_length_scaled'] = scl.fit_transform(poem_raw.Ave_word_length.values.reshape(-1, 1))

#meaningful columns for content based recsys
poem_df = poem_raw[['Poet', 'Tags', 'Word_count_scaled', 'Line_count_scaled', 'Ave_word_length_scaled']]

# binarize tags and poets, NEED TO FIX TAGS
mlb = MultiLabelBinarizer()
tags_series = poem_df.Tags
tags_dummies = pd.DataFrame(mlb.fit_transform(tags_series),columns=mlb.classes_, index=poem_df.index)
poet_dummies = pd.get_dummies(poem_df.Poet, prefix = None)
poem_dummies = pd.concat([poem_df.Word_count_scaled, poet_dummies, tags_dummies], axis = 1)

pca = PCA()
df_poem_pca = pca.fit_transform(poem_dummies)

#get around 80% of varience from 75 principal components
df_poem_pca = df_poem_pca[:, :75]
dists = pairwise_distances(df_poem_pca, metric='cosine')

def rand_poem():
    random_poem_idx = randint(0, poem_raw.Poem.shape[0] - 1)
    return poem_raw.loc[random_poem_idx]

recommend_df = pd.DataFrame(data=dists, index=poem_raw.index, columns=poem_raw.index)

def recommend_poems(liked_poems):
    poems_summed = recommend_df[liked_poems].sum(axis=1)
    poems_summed = poems_summed.sort_values(ascending=True)
    mask = ~poems_summed.index.isin(liked_poems)
    ranked_poems = poems_summed.index[mask]
    ranked_poems = ranked_poems.tolist()
    return ranked_poems

def poem_info_from_id(poem_id):
    return poem_raw.loc[poem_id]





