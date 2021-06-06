# importing necessary packages
from pymongo import MongoClient
from selenium import webdriver
import pandas as pd


# for holding the resultant list
element_list = []

for page in range(1, 3, 1):

    # scraping the main page using selenium
    page_url = "https://www.cnas.org/articles-multimedia/p" + str(page)
    driver = webdriver.Chrome('/Users/monekaruhiil/Downloads/chromedriver')
    driver.get(page_url)

    # getting the relevant data such as title, author etc using selenium
    for i in range(1, 20):
        title = driver.find_elements_by_css_selector(f'li.-with-image:nth-child({i}) > a:nth-child(3)')
        article = driver.find_elements_by_css_selector(f'li.-with-image:nth-child({i}) > p:nth-child(4)')
        author = driver.find_elements_by_xpath(f'//*[@id="content"]/section/ul/li[{i}]/p[2]')
        para = driver.find_elements_by_xpath(f'//*[@id="content"]/section/ul/li[{i}]/a')

        # getting the URL links for articles and appending element_list
        for i in range(len(title)):
            article_url = (para[i].get_attribute('href'))
            print(article_url)
            try:
                element_list.append([author[i].text[3:], title[i].text, article[i].text, para[i].get_attribute('href')])
            except:
                print("Link doesn't exist!")

# creating a pandas dataframe to send data to mongoDB
df = pd.DataFrame(element_list, columns=['Author', 'Title', 'Text', 'URL'])
print(df)

# getting the articles text for further processing
para_text = ''
for i in df['URL']:
    driver.get(i)
    article_text = driver.find_elements_by_xpath('//*[@id="mainbar"]')

    for i in range(len(article_text)):
        para_text += article_text[i].text

print(para_text)

# creating a output file for the articles text
outfile = open('article_text.txt', 'w')
print(para_text, file=outfile)

# closing the driver
driver.quit()

# sending data to mongoDB
client = MongoClient(
    "mongodb+srv://moneka:NoAQWRYG0s1lOjoC@cluster0.zgi2n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['dev']
collection = db['NewsScraping']
df.reset_index(inplace=True)
data_dict = df.to_dict("records")
collection.insert_many(data_dict)


