# Step 6
# produce contents for the Word Cloud

import re
import numpy as np
import pandas as pd
from collections import Counter


def step6():
    # This file is copied from the server's folder ${proj}/tmp/seed_94_step_0181*
    filename = "best/seed_94_step_0181"

    indices = np.load(f"{filename}_indicies.npy")
    df = pd.read_pickle("data/arxiv_4422.pickle")
    df = df.iloc[indices]
    df = df.reset_index(drop=True)


    # common english stop words from https://github.com/Alir3z4/stop-words/blob/master/english.txt
    with open("tools/stop_words.txt", "r") as f:
        stop_words = f.read()
    stop_words = stop_words.split('\n')

    title = ""
    for index, row in df.iterrows():
        title += row['title']
    # Cleaning text and lower casing all words
    for char in ':.,\n':
        title=title.replace(char,' ')
    title = title.lower()
    # split returns a list of words delimited by sequences of whitespace (including tabs, newlines, etc, like re's \s) 
    word_list = title.split()
    word_list = Counter(word_list).most_common()
    words = {}
    for word, count in word_list:
        if word not in stop_words and count>30:
            words[word.capitalize()] = count
    print(words)

    with open("public_html/word_cloud.html", "w") as f:
        for word, count in words.items():
            print(f"{word}:::{count}", file=f)

if __name__=="__main__":
    step6()