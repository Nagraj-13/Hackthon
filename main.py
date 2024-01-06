import pandas as pd
import matplotlib.pyplot as plt
import csv
import requests
import numpy as np

movies_df = pd.read_csv('movies.csv') 
shape = movies_df.shape
print("Shape of movies.csv:", shape)


ratings_df = pd.read_csv('ratings.csv')  
shape = ratings_df.shape
print("Shape of ratings.csv:", shape)

ratings_df = pd.read_csv('ratings.csv')  
unique_user_ids = ratings_df['userId'].nunique()
print("Number of unique userIds:", unique_user_ids)

ratings_df = pd.read_csv('ratings.csv')  
movies_df = pd.read_csv('movies.csv')  
ratings_count = ratings_df.groupby('movieId').size()
max_ratings_movie_id = ratings_count.idxmax()
movie_title = movies_df[movies_df['movieId'] == max_ratings_movie_id]['title'].iloc[0]

print("Movie with the most ratings:",movie_title," Movie ID:max_ratings_movie_id")



movies_df = pd.read_csv('movies.csv')  
tags_df = pd.read_csv('tags.csv')  
matrix_movie_id = movies_df[movies_df['title'] == 'Matrix, The (1999)']['movieId'].iloc[0]
matrix_tags = tags_df[tags_df['movieId'] == matrix_movie_id]
tags_list = matrix_tags['tag'].tolist()
print("Tags for 'The Matrix (1999)':", tags_list)




movies_df = pd.read_csv('movies.csv')  
ratings_df = pd.read_csv('ratings.csv')  
terminator_movie_id = movies_df[movies_df['title'] == 'Terminator 2: Judgment Day (1991)']['movieId'].iloc[0]
terminator_ratings = ratings_df[ratings_df['movieId'] == terminator_movie_id]
average_rating = terminator_ratings['rating'].mean()
print(f"The average user rating for 'Terminator 2: Judgment Day (1991)' is {average_rating:.2f}")


movies_df = pd.read_csv('movies.csv')  
ratings_df = pd.read_csv('ratings.csv')  


fight_club_id = movies_df[movies_df['title'] == 'Fight Club (1999)']['movieId'].iloc[0]


fight_club_ratings = ratings_df[ratings_df['movieId'] == fight_club_id]


plt.figure(figsize=(10, 6))
plt.hist(fight_club_ratings['rating'], bins=9, edgecolor='black')
plt.title('Distribution of User Ratings for "Fight Club (1999)"')
plt.xlabel('Rating')
plt.ylabel('Number of Ratings')
plt.xticks(range(1, 6))
plt.grid(axis='y', alpha=0.75)
plt.show()




ratings_df = pd.read_csv('ratings.csv')  
movies_df = pd.read_csv('movies.csv')  

grouped_ratings = ratings_df.groupby('movieId').agg(count=('rating', 'size'), mean_rating=('rating', 'mean'))


merged_df = pd.merge(movies_df, grouped_ratings, on='movieId')
filtered_movies = merged_df[merged_df['count'] > 50]


# print(filtered_movies.head(50))



top_movies = filtered_movies.sort_values(by='count', ascending=False).head(5)
print(top_movies[['title', 'count']])



movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
sci_fi_movies_df = movies_df[movies_df['genres'].str.contains('Sci-Fi')]

sci_fi_with_ratings_df = pd.merge(sci_fi_movies_df, ratings_df, on='movieId')

grouped_sci_fi = sci_fi_with_ratings_df.groupby('title').agg({'rating':'count'}).reset_index()
sorted_sci_fi = grouped_sci_fi.sort_values(by='rating', ascending=False)

third_most_popular_sci_fi = sorted_sci_fi.iloc[2]
print("\n\n\n")
# print(third_most_popular_sci_fi)


from bs4 import BeautifulSoup
def scrapper(imdb_id):
    url = f"https://www.imdb.com/title/tt{str(imdb_id).zfill(7)}/reviews"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    reviews = []
    for review in soup.find_all('div', class_='text show-more__control'):
        reviews.append(review.get_text())

    return reviews


# links_df = pd.read_csv('links.csv')
# merged_df = pd.merge(movies_df, links_df, on='movieId')


# def scrapper(imdbId):
#     id = str(int(imdbId))
#     n_zeroes = 7 - len(id)
#     new_id = "0" * n_zeroes + id
#     URL = f"https://www.imdb.com/title/tt{new_id}/"
#     request_header = {
#         'Content-Type': 'text/html; charset=UTF-8', 
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', 
#         'Accept-Encoding': 'gzip, deflate, br'
#     }
#     response = requests.get(URL, headers=request_header)  # Corrected method
#     soup = BeautifulSoup(response.text, 'html.parser')  # Create a BeautifulSoup object
#     imdb_rating = soup.find('span', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})  # Corrected tag and attributes
#     return imdb_rating.text.strip() if imdb_rating else np.nan

# # imdb_col = merged_df['imdbVotes']

# for index, row in merged_df.iterrows():
#     imdb_id = row['imdbId']
#     reviews = scrapper(imdb_id)


# print(merged_df)
# links_df = pd.read_csv('links.csv')


# merged_df = pd.merge(movies_df, links_df, on='movieId')


# def scrape_imdb_reviews(imdb_id):
#     url = f"https://www.imdb.com/title/tt{str(imdb_id).zfill(7)}/reviews"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     reviews = []
#     for review in soup.find_all('div', class_='text show-more__control'):
#         reviews.append(review.get_text())

#     return reviews

# # Scrape reviews for each movie
# for index, row in merged_df.iterrows():
#     imdb_id = row['imdbId']
#     reviews = scrape_imdb_reviews(imdb_id)

links_df = pd.read_csv('links.csv')


merged_df = pd.merge(movies_df, links_df, on='movieId')
print(merged_df)

review_data = []

for index, row in merged_df.iterrows():
    imdb_id = row['imdbId']
    movie_id = row['movieId']
    reviews = scrapper(imdb_id)
    for review in reviews:
        review_data.append({'movieId': movie_id, 'IMDB ID': imdb_id, 'Review': review})


reviews_df = pd.DataFrame(review_data)


reviews_df.to_csv('movie_reviews.csv', index=False)

print("Reviews saved to movie_reviews.csv")