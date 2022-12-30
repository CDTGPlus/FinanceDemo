from urllib import response
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd 
import matplotlib.pyplot as plt

finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN','GOOG','FB']
news_tables = {}
for ticker in tickers:
    url_user = finviz_url + ticker
    req = Request(url=url_user,headers={'user-agent':'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    print(html)
    

parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker,date,time,title])
    

vader = SentimentIntensityAnalyzer()

df = pd.DataFrame(parsed_data, columns=['ticker','date','time','title'])

#use lambda function to extract the compound(overall) polarity score of analyzed string element, add score to dataframe
fc = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(fc)

df['date'] = pd.to_datetime(df.date).dt.date



mean_df = df.groupby(['ticker','date']).mean()
#unstack in order to maintain date as the index (x axis)
mean_df = mean_df.unstack()
#apply cross section on compound column in order to maintain compound idenifier as second column
mean_df = mean_df.xs('compound',axis='columns').transpose()

mean_df.plot(kind='bar')
plt.show()
