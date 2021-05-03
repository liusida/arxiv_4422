import glob, re
import json
import xmltodict
import pandas as pd

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

    s2_filename = f"data/citation_compare/1.s2/{arxiv_id}.json"
    with open(s2_filename, "r") as f:
        s2_info = json.load(f)
    s2_citations = len(s2_info['citations'])
    year_s2 = int(s2_info['year'])

    g_filename = f"data/citation_compare/2.gscholar/{arxiv_id}.txt"
    with open(g_filename, "r") as f:
        g_info = f.read()
    g_citations = int(g_info)

    record = {
        "arxiv_id": arxiv_id,
        "title": title,
        "year_arxiv": year_arxiv,
        "year_s2": year_s2,
        "s2": s2_citations,
        "g": g_citations
    }
    df = df.append(record, ignore_index=True)

df.to_pickle("data/arxiv_4422.pickle")
