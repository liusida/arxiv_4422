# Step 5
# Based on the best solution we found, produce the content and background image for the web page.

import numpy as np
import pandas as pd
import cv2

def step5():
    # This file is copied from the server's folder ${proj}/tmp/seed_94_step_0181*
    filename = "best/seed_94_step_0181"

    indices = np.load(f"{filename}_indicies.npy")
    matrix = np.load("data/matrix.npy")
    df = pd.read_pickle("data/arxiv_4422.pickle")
    df = df.iloc[indices]
    df = df.reset_index(drop=True)

    with open("public_html/the_page.html", "w") as f:
        for index, row in df.iterrows():
            all_authors = authors = row['first_author']
            if row['other_authors']!="":
                authors += ", ..."
                all_authors += ", " + ", ".join(row['other_authors'].split(":|:"))[1:-1]
            if row['first_author']!=row['last_author']:
                authors += ", "+row['last_author']
                all_authors += ", "+row['last_author']

            year = int(row['year_s2'])
            if int(row['year_arxiv'])>year:
                year = f"{year} or {int(row['year_arxiv'])}"
            elif int(row['year_arxiv'])<year:
                year = f"{int(row['year_arxiv'])} or {year}"

            tooltip = f"""<p>{row['title']}</p>
            <p><i>{all_authors}</i></p>
            <p>Year {year}</p>
            <p>Cited by {row['s2']} or {row['g']}</p>
            """
            tooltip = tooltip.replace('\'', '`')
            print(f"<div class='paper' index='{index}' arxiv_id='{row['arxiv_id']}' tooltip='{tooltip}'>{row['title']} ({authors}, {int(row['year_arxiv'])})</div>", file=f)

    # reorder the matrix
    matrix = matrix[indices,:]
    matrix = matrix[:,indices]

    if True:
        png_filename = f"public_html/bg.png"
        im = np.array(matrix / matrix.max() * 255, dtype = np.uint8)
        im = 255-im
        # No border needed
        if False:
            border_width = 0
            a = np.zeros(shape=[im.shape[0], border_width], dtype=np.uint8)
            im = np.concatenate([a,im,a], axis=1)
            b = np.zeros(shape=[border_width, border_width+im.shape[0]+border_width ], dtype=np.uint8)
            im = np.concatenate([b,im,b], axis=0)
        cv2.imwrite(png_filename, im)
        
if __name__=="__main__":
    step5()