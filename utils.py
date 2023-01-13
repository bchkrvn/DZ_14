import sqlite3
import json

DB_PATH = './netflix.db'


def title_search(title):
    """
    Ищет последний фильм по названию
    :param title: название фильма
    :return: информация о фильме
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title LIKE '%{title}%'
                ORDER BY release_year DESC
                LIMIT 1
            """
    cursor.execute(query)
    result = cursor.fetchall()
    film = {
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "genre": result[0][3],
        "description": result[0][4],
    }

    return film


def year_to_year_search(year_1, year_2):
    """
    Ищет фильмы, выпущенные с year_1 года по year_2 года
    :param year_1: год от
    :param year_2: год до
    :return: список фильмов
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {year_1} AND {year_2}
                ORDER BY release_year
                LIMIT 100
            """
    cursor.execute(query)
    result = cursor.fetchall()

    movies = []
    for movie in result:
        one_movie = {
            "title": movie[0],
            "release_year": movie[1],
        }
        movies.append(one_movie)

    return movies


def rating_movies(rating):
    """
    Ищет фильмы согласно рейтингу
    :param rating: нужный рейтинг
    :return: список фильмов
    """
    symbol_rating = []
    if rating == 'children':
        symbol_rating = ["'G'"]
    elif rating == 'family':
        symbol_rating = ["'G'", "'PG'", "'PG-13'"]
    elif rating == 'adult':
        symbol_rating = ["'R'", "'NC-17'"]

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({', '.join(symbol_rating)})
            """
    cursor.execute(query)
    result = cursor.fetchall()

    movies = []
    for movie in result:
        one_movie = {
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]
        }
        movies.append(one_movie)

    return movies


def genre_search(genre):
    """
    Ищет фильмы по нужному жанру
    :param genre: жанр фильма
    :return: список фильмов
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre.capitalize()}%'
            ORDER BY release_year DESC
            LIMIT 10
            """
    cursor.execute(query)
    result = cursor.fetchall()

    movies = []
    for movie in result:
        one_movie = {
            "title": movie[0],
            "description": movie[1],
        }
        movies.append(one_movie)

    return json.dumps(movies)


def find_actors(name_1, name_2):
    """
    Находит актеров, которые играли с актерами name_1 и name_2 более двух раз
    :param name_1: имя первого актера
    :param name_2: имя второго актера
    :return: список актеров
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
                SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE '%{name_1}%'
                AND netflix.cast LIKE '%{name_2}%'
                """
    cursor.execute(query)
    result = cursor.fetchall()

    # список всех актеров
    all_actors = []
    for film in result:
        all_actors.extend(film[0].split(', '))

    # поиск нужных актеров
    need_actors = []
    for actor in set(all_actors):
        if actor not in [name_1, name_2] and all_actors.count(actor) > 2:
            need_actors.append(actor)

    return need_actors


def find_for_type_year_genre(type_: str, year: int, genre: str):
    """
    Ищет картины по типу, году и жанру
    :param type_: тип картины
    :param year: год выпуска
    :param genre: жанр
    :return: список картин
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE netflix.type = '{type_.capitalize()}'
                    AND release_year = {year}
                    AND listed_in LIKE '%{genre.capitalize()}%'
                    """
    cursor.execute(query)
    result = cursor.fetchall()

    movies = []
    for movie in result:
        one_movie = {
            "title": movie[0],
            "description": movie[1],
        }
        movies.append(one_movie)

    return movies
