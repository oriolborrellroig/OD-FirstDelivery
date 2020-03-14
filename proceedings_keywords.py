import pandas as pd
import csv

proceeding = pd.read_csv("./dblp2/output_inproceedings.csv", error_bad_lines=False, sep=';', 
                      converters={i: str for i in range(0, 100)},  nrows=3000)

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

columns2 = ['id', 'author', 'title', 'keywords']
keywords = pd.DataFrame(columns=columns2)
keywords.to_csv("keywords_proceedings.csv", mode='w', index=False, sep=';', header=True)
for index, row in workshops.iterrows():
    for keyword in row['title'].split(' '):
        keyword = ''.join(filter(lambda c: c.isalpha(), keyword))
        if (len(keyword) > 3):
            k = [[row['id'], row['author'], row['title'], keyword]]
            df = pd.DataFrame(k, columns=columns2)
            keywords = keywords.append(df)

for index, row in conferences.iterrows():
    for keyword in row['title'].split(' '):
        keyword = ''.join(filter(lambda c: c.isalpha(), keyword))
        if (len(keyword) > 3):
            keyword = keyword.lower()
            k = [[row['id'], row['author'], row['title'], keyword]]
            df = pd.DataFrame(k, columns=columns2)
            keywords = keywords.append(df)

keywords.to_csv("keywords_proceedings.csv", mode='a', index=False, sep=';',  quoting=csv.QUOTE_ALL, header=False)