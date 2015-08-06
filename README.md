# Movie Trailer Website

**Movie Trailer Website** uses server-side code to store a list of
favorite movies. Youtube and OMDB APIs deliver current information about each
movie entered into the movie list array. This program will generate a static web
page allowing visitors to browse the movies, watch trailers, and get more
information about the movies.

## Installation

Make sure you have [Python 2.7.10](https://www.python.org/downloads/) installed.

Fork this repo or download the zip folder for the repository.

## Running the program

In the entertainment_center.py file you will need to replace the youtube_suffix
with your YouTube API key or create a config.py file to store the the API key.

Follow the instructions on the YouTube Data API website to create your API key:

https://developers.google.com/youtube/v3/getting-started

Once you have your API key in the youtube_suffix, open the repository and run 
entertainment_center.py:

```console
python entertainment_center.py
```

## Updating Movie List

In order to customize the movie list, simply open entertainment_center.py and
add the title of the movie to the 'movie_list' array.

## Bug reports

If you discover any bugs, feel free to create an issue on GitHub. I also
encourage you to help even more by forking and sending me a pull request.

https://github.com/aj65461/movie-trailer-website/issues

## Maintainers

* Aaron Johnson (https://github.com/aj65461)

## License

MIT License

