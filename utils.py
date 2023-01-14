import sqlite3
import json


def get_data(query: str):
    """
    Обращается к базе данных
    :param query: SQL запрос
    :return: результат запроса
    """
    DB_PATH = './netflix.db'

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def title_search(title: str) -> dict:
    """
    Ищет последний фильм по названию
    :param title: название фильма
    :return: информация о фильме
    """
    query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title LIKE '%{title}%'
                ORDER BY release_year DESC
                LIMIT 1
            """
    result = get_data(query)
    film = {
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "genre": result[0][3],
        "description": result[0][4],
    }

    return film


def year_to_year_search(year_1: int, year_2: int) -> list:
    """
    Ищет фильмы, выпущенные с year_1 года по year_2 года
    :param year_1: год от
    :param year_2: год до
    :return: список фильмов
    """
    query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {year_1} AND {year_2}
                ORDER BY release_year
                LIMIT 100
            """
    result = get_data(query)
    movies = [{"title": movie[0], "release_year": movie[1]} for movie in result]

    return movies


def get_symbol_rating(rating: str) -> list:
    if rating == 'children':
        return ["'G'"]
    elif rating == 'family':
        return ["'G'", "'PG'", "'PG-13'"]
    elif rating == 'adult':
        return ["'R'", "'NC-17'"]
    else:
        return []


def rating_movies(rating: str) -> list:
    """
    Ищет фильмы согласно рейтингу
    :param rating: нужный рейтинг
    :return: список фильмов
    """
    symbol_rating = get_symbol_rating(rating)

    query = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({', '.join(symbol_rating)})
            """
    result = get_data(query)

    movies = []
    for movie in result:
        one_movie = {
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]
        }
        movies.append(one_movie)

    return movies


def genre_search(genre: str):
    """
    Ищет фильмы по нужному жанру
    :param genre: жанр фильма
    :return: список фильмов
    """
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre.capitalize()}%'
            ORDER BY release_year DESC
            LIMIT 10
            """
    result = get_data(query)
    movies = [{"title": movie[0], "description": movie[1]} for movie in result]

    return json.dumps(movies)


def find_actors(name_1: str, name_2: str):
    """
    Находит актеров, которые играли с актерами name_1 и name_2 более двух раз
    :param name_1: имя первого актера
    :param name_2: имя второго актера
    :return: список актеров
    """
    query = f"""
                SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE '%{name_1}%'
                AND netflix.cast LIKE '%{name_2}%'
                """
    result = get_data(query)

    # список всех актеров с повторениями
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
    query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE netflix.type = '{type_.capitalize()}'
                    AND release_year = {year}
                    AND listed_in LIKE '%{genre.capitalize()}%'
                    """
    result = get_data(query)
    movies = [{"title": movie[0], "description": movie[1]} for movie in result]

    return movies
