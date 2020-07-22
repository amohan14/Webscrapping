# Webscrapping yelp reviews of a restaurant to csv
from bs4 import BeautifulSoup
import requests
import csv
from time import sleep
from random import randint
import re

# storing response of a get request to a variable
response = requests.get('https://www.yelp.com/biz/celine-patisserie-seattle-2')

# creating an instance/object of class bs4.BeautifulSoup i.e reviews and storing the html parsed value of the response in it
soup = BeautifulSoup(response.text, 'html.parser')
# print(reviews)

num_reviews = soup.find(class_='lemon--div__373c0__1mboc arrange-unit__373c0__o3tjT border-color--default__373c0__3-ifU nowrap__373c0__35McF').get_text('p')
# print(num_reviews) 245 reviews

# To get the number of reviews as int
num_reviews = int(re.findall('\d+', num_reviews)[0])
print(num_reviews)

# Storing all review pages to a list; each page has 20 reviews(validated comparing the url of pages)
url_list = []
for i in range(0, num_reviews, 20):
    url_list.append('https://www.yelp.com/biz/celine-patisserie-seattle-2?start='+str(i))
    print(url_list)

# reviews = soup.find_all('div', attrs={'class' : 'lemon--div__373c0__1mboc review__373c0__13kpL sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__2C9bH gutter-2__373c0__1DiLQ grid__373c0__1Pz7f layout-stack-small__373c0__27wVp border-color--default__373c0__3-ifU'})
# print(len(reviews))

# Reviewer
# reviews = reviews[0]
# user = reviews.find('a', attrs={'class' : 'lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'}).string
# print(user)

# Location
# location = reviews.find('span', attrs={'class' : 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO'}).string
# print(location)

# Rating
# couldn't access the rating with the exact class so went to child-parent method
# rating = reviews.find('img', attrs={'class' : 'lemon--img__373c0__3GQUb offscreen__373c0__1KofL'}).parent.get('aria-label')
# rating = int(re.findall('\d+', rating)[0])
# print(rating)

# Date
# date = reviews.find('span', attrs={'class' : 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-'}).string
# print(date)

# Review content
# content = reviews.find('span', attrs={'class' : 'lemon--span__373c0__3997G raw__373c0__3rKqk'}).get_text()
# print(content)


def onepage_scrape(reviews, csvwriter):
    for review in reviews:
        dic = {}
        user = review.find('a', attrs={'class' : 'lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'}).string
        location = review.find('span', attrs={'class' : 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO'}).string
        rating = review.find('img', attrs={'class' : 'lemon--img__373c0__3GQUb offscreen__373c0__1KofL'}).parent.get('aria-label')
        rating = int(re.findall('\d+', rating)[0])
        date = review.find('span', attrs={'class' : 'lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-'}).string
        content = review.find('span', attrs={'class' : 'lemon--span__373c0__3997G raw__373c0__3rKqk'}).get_text()
        dic['user'] = user
        dic['location'] = location
        dic['rating'] = rating
        dic['date'] = date
        dic['content'] = content
        csvwriter.writerow(dic.values())

with open('yelpreviews.csv', 'w', encoding='utf-8', newline='') as csvfile:
    review_writer = csv.writer(csvfile)
    headers = ['User', 'Location', 'Rating', 'Date', 'Content']
    review_writer.writerow(headers)
    for index, url in enumerate(url_list):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('div', attrs={'class' : 'lemon--div__373c0__1mboc review__373c0__13kpL sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__2C9bH gutter-2__373c0__1DiLQ grid__373c0__1Pz7f layout-stack-small__373c0__27wVp border-color--default__373c0__3-ifU'})
        # function call
        onepage_scrape(reviews, review_writer)
        sleep(randint(1,5))
        print('Completed page'+str(index+1))