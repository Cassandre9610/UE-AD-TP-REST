from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'


with open('{}/databases/movies.json'.format("."), 'r') as jsf:
    movies = json.load(jsf)["movies"]
    print(movies)


def write(movies):
    with open('{}/databases/movies.json'.format("."), 'w') as f:
        full = {}
        full['movies']=movies
        json.dump(full, f)


def response(message, error_code):
    return make_response(jsonify(message), error_code)


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Movie service!</h1>"


@app.route("/json", methods=['GET'])
def get_json():
    return response(movies, 200)


@app.route("/movies/movie/<movie_id>", methods=['GET'])
def get_movie_byid(movie_id):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            return response(movie, 200)
    return response({"error": "Movie not found"}, 404)


@app.route("/movies/title", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = response({"error": "Movie title not found"}, 404)
    else:
        res = response(json, 200)
    return res


@app.route("/movies/movie/<movie_id>", methods=['POST'])
def add_movie(movie_id):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            print(movie["id"])
            print(movie_id)
            return response({"error": "Movie already exists"}, 500)

    movies.append(req)
    write(movies)
    return response({"message": "Movie added"}, 200)


@app.route("/movies/movie/<movie_id>/rating/<rating>", methods=['PUT'])
def update_movie_rating(movie_id, rating):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            movie["rating"] = rating
            write(movies)
            return response(movie, 200)

    return response({"error": "Movie not found"}, 404)


@app.route("/movies/movie/<movie_id>", methods=['DELETE'])
def del_movie(movie_id):
    for movie in movies:
        if str(movie["id"]) == str(movie_id):
            movies.remove(movie)
            write(movies)
            return response(movie, 200)

    return response({"error": "Movie not found"}, 404)


if __name__ == "__main__":
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
