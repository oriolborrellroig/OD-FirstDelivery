import pandas as pd
import csv

from random import seed
from random import randint

seed(1)

proceeding = pd.read_csv("./dblp2/output_inproceedings.csv", error_bad_lines=False, sep=';', 
                      converters={i: str for i in range(0, 100)})

columns = ['id','author', 'crossref', 'title', 'year', 'mdate', 'key', 'url']
proceeding = proceeding[columns]
proceeding = proceeding[proceeding['url'].str.contains('db/conf/', regex=False, case=False)]
proceeding['conference'] = proceeding['url'].apply(lambda x: x.split('/')[2])
proceeding['edition'] = proceeding['url'].apply(lambda x: x.split('/')[3])
proceeding['edition'] = proceeding['edition'].apply(lambda x: x.split('.')[0])

proceeding['title'] = proceeding['title'].apply(lambda x: x.replace('"', ''))
proceeding['author'] = proceeding['author'].apply(lambda x: x.split('|')[0])

workshops = proceeding[proceeding['title'].str.contains('workshop', regex=False, case=False)]
#workshops = workshops.iloc[:1000]
workshops = workshops.head(1000)

conferences = proceeding[~proceeding['title'].str.contains('workshop', regex=False, na=False, case=False)]
#conferences = conferences.iloc[:1000]
conferences = conferences.head(1000)

columns.append('conference')
columns.append('edition')
auth = pd.DataFrame(columns=columns)
auth.to_csv("proceedings.csv", mode='w', index=False, sep=';', header=True)
proceeding.to_csv("proceedings.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

auth.to_csv("workshops.csv", mode='w', index=False, sep=';', header=True)
workshops.to_csv("workshops.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

auth.to_csv("conferences.csv", mode='w', index=False, sep=';', header=True)
conferences.to_csv("conferences.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

#Generate Workshop Citations
maxNumberOfArticles = len(workshops)-1
citations = []
for i in range(maxNumberOfArticles):
    numberOfCitations = randint(0, 10)
    for j in range(numberOfCitations):
        randomLine = randint(0, maxNumberOfArticles)
        if(workshops.iloc[i]['id'] != workshops.iloc[randomLine]['id'] and workshops.iloc[i]['year'] >= workshops.iloc[randomLine]['year']):
            newCitation = [workshops.iloc[i]['id'], workshops.iloc[randomLine]['id'], workshops.iloc[i]['year']]
            citations.append(newCitation)

cit = pd.DataFrame(columns=['paperID', 'citedID', 'year'])
cit.to_csv("workshops_citations.csv", mode='w', index=False, sep=';', header=True)
citations = pd.DataFrame(citations)
citations.to_csv("workshops_citations.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

#Generate Conferences Citations
maxNumberOfArticles = len(conferences)-1
citations = []
for i in range(maxNumberOfArticles):
    numberOfCitations = randint(0, 10)
    for j in range(numberOfCitations):
        randomLine = randint(0, maxNumberOfArticles)
        if(conferences.iloc[i]['id'] != conferences.iloc[randomLine]['id'] and conferences.iloc[i]['year'] >= conferences.iloc[randomLine]['year']):
            newCitation = [conferences.iloc[i]['id'], conferences.iloc[randomLine]['id'], conferences.iloc[i]['year']]
            citations.append(newCitation)

cit = pd.DataFrame(columns=['paperID', 'citedID', 'year'])
cit.to_csv("conferences_citations.csv", mode='w', index=False, sep=';', header=True)
citations = pd.DataFrame(citations)
citations.to_csv("conferences_citations.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)