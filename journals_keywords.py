import pandas as pd
import csv

journals = pd.read_csv("./dblp2/output_article.csv",error_bad_lines=False, sep=';', na_values = 'N', 
                      converters={i: str for i in range(0, 100)}, nrows=110000)
columns = ['id','author', 'journal', 'title', 'volume', 'year', 'mdate', 'key', 'url']

journals = journals[columns]
journals = journals[journals['url'].str.contains('db/journal', regex=False, case=False)]

#authors = authors[authors.volume != ""]
journals['title'] = journals['title'].apply(lambda x: x.replace('"', ''))
#journal-volume
journals["journalVolume"] = journals["journal"] + '-' + journals["volume"]
journals['author'] = journals['author'].apply(lambda x: x.split('|')[0])
journals = journals.iloc[:100000]

# columns.append('journalVolume')
# auth = pd.DataFrame(columns=columns)
# auth.to_csv("articles.csv", mode='w', index=False, sep=';', header=True)
# journals.to_csv("articles.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)

columns2 = ['id', 'author', 'title', 'keywords']
keywords = pd.DataFrame(columns=columns2)
keywords.to_csv("keywords.csv", mode='w', index=False, sep=';', header=True)
for index, row in journals.iterrows():
    if (index%100 == 0):
        keywords.to_csv("keywords.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)
        keywords = pd.DataFrame(columns=columns2)
        print(index)
    #title = row[['id', 'author', 'title']]
    #print(len(row['title'].split(' ')))
    for keyword in row['title'].split(' '):
        keyword = ''.join(filter(lambda c: c.isalpha(), keyword))
        if (len(keyword) > 3):
            keyword = keyword.lower()
            k = [[row['id'], row['author'], row['title'], keyword]]
            df = pd.DataFrame(k, columns=columns2)
            keywords = keywords.append(df)
        #print(len(keywords))

keywords.to_csv("keywords.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)
#keywords = journals["title"].apply(lambda x: x.split(' '))