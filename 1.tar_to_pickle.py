# Step 1
# Extract the tar.gz file into temporary folder and get some useful information from it.
# Save useful information into a pandas DataFrame pickle file.

import glob, re, os
import json
import xmltodict
import pandas as pd
import tarfile
import shutil
from tools.names import compare_two_names


def abbr(name):
    n = name.split(' ')
    return f"{n[0][0]}. {n[-1]}"

def step1():
    if not os.path.exists("data/arxiv_4422"):
        tar = tarfile.open("data/arxiv_4422.tar.gz", "r:gz")
        # extract
        tar.extractall("data")
        tar.close()

    df = pd.DataFrame(columns=['arxiv_id', 'title', 'year_arxiv', 'year_s2', 's2', 'g'])

    filenames = glob.glob("data/arxiv_4422/0.arxiv/*.xml")
    for filename in filenames:
        with open(filename, "r") as f:
            record_xml = f.read()
        record_dict = xmltodict.parse(record_xml, process_namespaces=False)['record']['metadata']['arXiv']
        arxiv_id = record_dict['id']
        title = record_dict['title']
        title = re.sub(r'\s+', ' ', title)
        year_arxiv = int(record_dict['created'][:4])

        s2_filename = f"data/arxiv_4422/1.s2/{arxiv_id}.json"
        with open(s2_filename, "r") as f:
            s2_info = json.load(f)
        s2_citations = len(s2_info['citations'])
        year_s2 = int(s2_info['year'])

        # extract first author, last author, and other authors
        # with tricks try to correct the names.
        other_authors = []
        if isinstance(record_dict['authors']['author'], list):
            first_k, last_k = 0, 0
            if 'forenames' in record_dict['authors']['author'][0]:
                first_author = f"{record_dict['authors']['author'][0]['forenames']} {record_dict['authors']['author'][0]['keyname']}"
            elif record_dict['authors']['author'][0]['keyname']=="OpenAI":
                first_author = record_dict['authors']['author'][0]['keyname']
            else:
                first_k = 1
                first_author = f"{record_dict['authors']['author'][0]['keyname']} {record_dict['authors']['author'][1]['keyname']}"
            if 'forenames' in record_dict['authors']['author'][-1]:
                last_author = f"{record_dict['authors']['author'][-1]['forenames']} {record_dict['authors']['author'][-1]['keyname']}"
            else:
                last_k = 1
                last_author = f"{record_dict['authors']['author'][-2]['keyname']} {record_dict['authors']['author'][-1]['keyname']}"
            if len(record_dict['authors']['author'])>2+first_k+last_k:
                for i in range(1+first_k, len(record_dict['authors']['author'])-last_k-1):
                    if 'forenames' in record_dict['authors']['author'][i]:
                        author = f"{record_dict['authors']['author'][i]['forenames']} {record_dict['authors']['author'][i]['keyname']}"
                    else:
                        author = f"{record_dict['authors']['author'][i]['keyname']}"
                    other_authors.append(f"{author}")
                
        else:
            first_author = last_author = f"{record_dict['authors']['author']['forenames']} {record_dict['authors']['author']['keyname']}"

        s2_filename = f"data/arxiv_4422/1.s2/{arxiv_id}.json"
        with open(s2_filename, "r") as f:
            s2_info = json.load(f)
        s2_citations = len(s2_info['citations'])
        year_s2 = int(s2_info['year'])

        g_filename = f"data/arxiv_4422/2.gscholar/{arxiv_id}.txt"
        with open(g_filename, "r") as f:
            g_info = f.read()
        g_citations = int(g_info)
        
        # If names from arxiv and semantic scholar are different, show a warning.
        if not compare_two_names(first_author, s2_info['authors'][0]['name']):
            print(f"Warning: Name difference, {first_author} v.s. {s2_info['authors'][0]['name']}, refer to https://arxiv.org/abs/{arxiv_id}")

        record = {
            "arxiv_id": arxiv_id,
            "title": title,
            "year_arxiv": year_arxiv,
            "year_s2": year_s2,
            "s2": s2_citations,
            "g": g_citations,
            "first_author": first_author,
            "last_author": last_author,
            "other_authors": ":|:".join(other_authors),
        }
        df = df.append(record, ignore_index=True)

    # save pickle
    df.to_pickle("data/arxiv_4422.pickle")

    # clean 
    shutil.rmtree("data/arxiv_4422/")

if __name__=="__main__":
    step1()