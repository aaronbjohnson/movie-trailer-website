import fresh_tomatoes
import media
import requests
import json

youtube_key = 'AIzaSyCmJT7e_pi5-5yWNi4F9UXuV8j1fUTlIm8'
youtube_prefix = 'https://www.youtube.com/watch?v='

# Movie list -- Here you can add and subtract movies as your tastes change

movie_list = ["There Will Be Blood", "The Life Aquatic", "Unforgiven", 
              "Gladiator", "About Time", "The 'Burbs"]

movies = []


def get_info(video):
    """Fetches movie info from Open Movie Database"""

    # Request data from Youtube

    youtube = requests.get('https://www.googleapis.com/youtube/v3/search?part=s'
                           'nippet&q=' + video + 'trailer&maxResults=1&key=' +
                           youtube_key, timeout=20)
    youtube_str = youtube.text
    youtube_dict = json.loads(youtube_str)
    video_id = youtube_dict['items'][0]['id']['videoId']
    video_url = youtube_prefix + video_id

    # Request data from OMDB

    result = requests.get('http://www.omdbapi.com/?t=' + video + '&y=&plot='
                          'short&r=json', timeout=20)
    resp_str = result.text

    # Convert data into a python dictionary
    # http://stackoverflow.com/questions/12788217/extract-single-value-from-json-response-python

    resp_dict = json.loads(resp_str)

    trailer = video_url
    title = resp_dict["Title"]
    poster = resp_dict["Poster"]
    release = resp_dict["Released"]
    rating = resp_dict["Rated"]
    runtime = resp_dict["Runtime"]
    genre = resp_dict["Genre"]
    director = resp_dict["Director"]
    plot = resp_dict["Plot"]
    actors = resp_dict["Actors"]

    movies.append(media.Movie(trailer, title, poster, release, rating, runtime, 
                              genre, director, plot, actors))

# Create movie instances and add them to the movies list

for movie in movie_list:
    get_info(movie)

fresh_tomatoes.open_movies_page(movies)
