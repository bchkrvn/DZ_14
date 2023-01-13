from flask import Flask
import utils

app = Flask(__name__)


@app.route('/movies/<title>')
def movie_title(title):
    movie = utils.title_search(title)
    return movie


@app.route('/movies/<int:year_1>/to/<int:year_2>')
def movies_year_to_year(year_1, year_2):
    movies = utils.year_to_year_search(year_1, year_2)
    return movies


@app.route('/rating/<rating>')
def movies_rating(rating):
    movies = utils.rating_movies(rating)
    return movies


@app.route('/genre/<genre>')
def genre_movies(genre):
    movies = utils.genre_search(genre)
    return movies


if __name__ == '__main__':
    app.run()
