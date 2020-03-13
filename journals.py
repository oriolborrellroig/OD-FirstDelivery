import pandas as pd
import csv

from random import seed
from random import randint

seed(1)

journals = pd.read_csv("./dblp2/output_article.csv",error_bad_lines=False, sep=';', na_values = 'N', 
                      converters={i: str for i in range(0, 100)})
columns = ['id','author', 'journal', 'title', 'volume', 'year', 'mdate', 'key', 'url']

journals = journals[columns]
journals = journals[journals['url'].str.contains('db/journal', regex=False, case=False)]

#authors = authors[authors.volume != ""]
journals['title'] = journals['title'].apply(lambda x: x.replace('"', ''))
#journal-volume
journals["journal-volume"] = journals["journal"] + '-' + journals["volume"]
journals['author'] = journals['author'].apply(lambda x: x.split('|')[0])
journals = journals.iloc[:1000]

auth = pd.DataFrame(columns=columns)
auth.to_csv("articles.csv", mode='w', index=False, sep=';', header=True)
journals.to_csv("articles.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)




#Generate Citations
maxNumberOfArticles = len(journals)-1
citations = []
for i in range(maxNumberOfArticles):
    numberOfCitations = randint(0, 20)
    for j in range(numberOfCitations):
        randomLine = randint(0, maxNumberOfArticles)
        if(journals.iloc[i]['id'] != journals.iloc[randomLine]['id']) and journals.iloc[i]['year'] >= journals.iloc[randomLine]['year']:
            newCitation = [journals.iloc[i]['id'], journals.iloc[randomLine]['id'], journals.iloc[i]['year']]
            citations.append(newCitation)

cit = pd.DataFrame(columns=['paperID', 'citedID', 'year'])
cit.to_csv("articles_citations.csv", mode='w', index=False, sep=';', header=True)
citations = pd.DataFrame(citations)
citations.to_csv("articles_citations.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

