import requests
from bs4 import BeautifulSoup #used for web scrapping
import smtplib #Used for the email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import datetime #system date and time
now = datetime.datetime.now()

#email content placeholder
content = ' '


#Extracting Hacker News Stories
def extract_news(url):
    print('Extracting news stories...')
    cnt = ''
    cnt +=('<br>HN Top Stories:</br>\n' + '<br>' + '-' * 50 + '<br>\n')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: ' +tag.text + "\n" + '<br>')if tag.text!='More' else '')
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------<br>')
content +=('<br><br>End of Message')

print(content)