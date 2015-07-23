import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            margin-top: 10px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile-video', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        // Open More Info Modal when 'More Info' button is clicked
        $(document).on('click', '.info-btn', function (event) {
            var plot = $(this).attr('data-plot');
            var title = $(this).attr('data-title');
            var release = $(this).attr('data-release');
            var rating = $(this).attr('data-rating');
            var runtime = $(this).attr('data-runtime');
            var genre = $(this).attr('data-genre');
            var director = $(this).attr('data-director');
            var actors = $(this).attr('data-actors');
            $('.plot-info').append(plot);
            $('.modal-title').append(title);
            $('.release-info').append(release);
            $('.rating-info').append(rating);
            $('.runtime-info').append(runtime);
            $('.genre-info').append(genre);
            $('.director-info').append(director);
            $('.actors-info').append(actors);
        });
        // Close More Info Modal when the 'Close' button is clicked
        $(document).on('click', '.close-modal, #infoModal', function (event) {
            $('.plot-info').empty();
            $('.modal-title').empty();
            $('.release-info').empty();
            $('.rating-info').empty();
            $('.runtime-info').empty();
            $('.genre-info').empty();
            $('.director-info').empty();
            $('.actors-info').empty();
        });
        // Make all movie tiles have the same height
        // Source: http://stackoverflow.com/questions/23287206/same-height-column-bootstrap-3-row-responsive
        $(document).ready(function() {
            var heights = $(".movie-tile").map(function() {
                return $(this).height();
            }).get(),
            maxHeight = Math.max.apply(null, heights);
            $(".movie-tile").height(maxHeight);
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div id="infoModal" class="modal fade" role="dialog">
      <div class="modal-dialog">

        <!-- Modal content-->
        <div class="modal-content">
            <div id="info-modal-container">
                <div class="modal-header">
                    <h4 class="modal-title text-center"></h4>
                </div>
                <div class="modal-body">
                    <h5>Plot</h5>
                    <p class="plot-info"></p>
                    <h5>Release Date</h5>
                    <p class="release-info"></p>
                    <h5>Rating</h5>
                    <p class="rating-info"></p>
                    <h5>Runtime</h5>
                    <p class="runtime-info"></p>
                    <h5>Genre</h5>
                    <p class="genre-info"></p>
                    <h5>Director</h5>
                    <p class="director-info"></p>
                    <h5>Actors</h5>
                    <p class="actors-info"></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="close-modal btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand page-heading" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center">
    <div class="movie-tile-video" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <img src="{poster_image_url}" width="220" height="342">
        <h2>{movie_title}</h2>
    </div>
    <button type="button" class="info-btn btn btn-info btn-lg" data-plot="{plot}" data-title="{movie_title}" data-release="{release_date}" data-rating="{rating}" data-runtime="{runtime}" data-genre="{genre}" data-director="{director}" data-actors="{actors}" data-toggle="modal" data-target="#infoModal">More Info</button>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            release_date=movie.release_date,
            rating=movie.rating,
            runtime=movie.runtime,
            genre=movie.genre,
            director=movie.director,
            plot=movie.plot,
            actors=movie.actors
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)