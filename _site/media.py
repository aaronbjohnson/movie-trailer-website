import webbrowser


class Movie:

    """ This class provides a way to store movie-related information"""

    def __init__(self, trailer_youtube, movie_title, poster_image, release_date,
                 rating, runtime, genre, director, plot, actors):
        self.trailer_youtube_url = trailer_youtube
        self.title = movie_title
        self.poster_image_url = poster_image
        self.release_date = release_date
        self.rating = rating
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.plot = plot
        self.actors = actors

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
