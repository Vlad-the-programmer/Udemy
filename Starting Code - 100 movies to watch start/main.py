import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"


# Write your code below this line 👇
response = requests.get(URL)
website_html = response.text

soupe = BeautifulSoup(website_html, "html.parser")
movies_titles = [title.getText() for title in soupe.find_all(name='h3', class_='title')]
print(movies_titles)

with open("movies.txt", "w") as file:
    for movie in reversed(movies_titles):
        file.write(movie + '\n')

