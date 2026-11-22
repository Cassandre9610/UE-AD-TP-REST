from flask import Flask, request, jsonify, make_response
import requests
import json

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

SCHEDULE_API_URL = "http://127.0.0.1:3202/schedule"


with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

def response(message, error_code):
    return make_response(jsonify(message), error_code)


def write(bookings):
    with open('{}/databases/bookings.json'.format("."), 'w') as f:
        full = {}
        full['bookings']=bookings
        json.dump(full, f)


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/json", methods=['GET'])
def get_json():
    return response(bookings, 200)


@app.route("/bookings/user/<userid>", methods=['GET'])
def get_booking_by_userid(userid):
    print(userid)
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return response(booking, 200)
    return response({"error":"User ID not found"}, 404)


@app.route("/bookings/date/<date>", methods=['GET'])
def get_booking_by_date(date):
    data = []
    movies = []
    for booking in bookings:
        for booking_date in booking["dates"]: 
            if str(booking_date["date"]) == str(date):
                movies.extend(booking_date["movies"])
        data.append({"userid": booking["userid"], "movies": movies})
        movies = []
    return response({"bookings": data}, 200)


@app.route("/bookings/movie/<movieid>", methods=['GET'])
def get_booking_by_movieid(movieid):
    data = []
    for booking in bookings:
        dates = [
            booking_date["date"]
            for booking_date in booking["dates"]
            if any(str(booked_movie) == str(movieid) for booked_movie in booking_date["movies"])
        ]
        data.append({"userid": booking["userid"], "dates": dates})
    return response({"bookings": data}, 200)
    

@app.route("/bookings/user/<userid>/date/<date>", methods=['GET'])
def get_movies_by_userid_and_date(userid, date):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            for d in booking["dates"]:
                if str(d["date"]) == str(date):
                    return response({"movies": d["movies"]}, 200)
    return response({"error": "Movie not found"}, 404)


# @app.route("/bookings", methods=['POST'])
# def add_booking():
#     # TODO
#     req = request.get_json()
#     if not req:
#         return response({"error": "Invalid JSON data"}, 400)
    
#     data = requests.get(SCHEDULE_API_URL + "/date/" + req["date"]).json()
#     print(data)
#     for movie in data["movies"]:
#         if str(movie) == str(req["movieid"]):
#             bookings.append(req)
#             write(bookings) # ajouter correctement le booking à l'utilisateur existant !!!!!!!!!!!!!!!!!!!!!!!!!
#             return response({"message": "Booking added"}, 200)
#     return response({"error": "Movie not found for the given date"}, 404)

@app.route("/bookings", methods=['POST'])
def add_booking():
    req = request.get_json()
    if not req:
        return response({"error": "Invalid JSON data"}, 400)
    
    schedule_response = requests.get(
        SCHEDULE_API_URL + "/date/" + req["date"],
        timeout=5
    )
    

    if schedule_response.status_code != 200:
        return response({"error": "Nothing found for this date"}, 404)

    schedule_response = schedule_response.json()
    if str(req["movieid"]) not in [str(movie) for movie in schedule_response["movies"]]:
        return response({"error": "Movie not found for the given date"}, 404)

    print(schedule_response)
    for booking in bookings:
        if str(booking["userid"]) == str(req["userid"]):
            for booking_date in booking["dates"]:
                if str(booking_date["date"]) == str(req["date"]):
                    if str(req["movieid"]) not in [
                        str(movie) for movie in booking_date["movies"]
                    ]:
                        booking_date["movies"].append(req["movieid"])
                        write(bookings)

                    return response({"message": "Booking added"}, 200)

            booking["dates"].append({
                "date": req["date"],
                "movies": [req["movieid"]]
            })
            write(bookings)
            return make_response(jsonify({"message":"Booking added"}), 200)
    
    bookings.append({
        "userid": req["userid"],
        "dates": [
            {
                "date": req["date"],
                "movies": [req["movieid"]]
            }
        ]
    })
    write(bookings)
    return make_response(jsonify({"message":"Booking added"}), 200)


@app.route("/bookings/user/<userid>/date/<date>/movie/<movieid>", methods=['DELETE'])
def delete_movie(userid, date, movieid):
    for index_booking, booking in enumerate(bookings):
        if str(booking["userid"]) == str(userid):
            for index_booking_date, booking_date in enumerate(booking["dates"]):
                if str(booking_date["date"]) == str(date):
                    for index_booked_movie, booked_movie in enumerate(booking_date["movies"]):
                        if str(booked_movie) == str(movieid):
                            booking_date["movies"].pop(index_booked_movie)
                            if not booking_date["movies"]:
                                booking["dates"].pop(index_booking_date)
                            if not booking["dates"]:
                                bookings.pop(index_booking)
                            write(bookings)
                            return response({"message": "Movie successfully deleted"}, 204)
    return response({"error": "Movie not found"}, 404)


@app.route("/bookings/user/<userid>", methods=['DELETE'])
def delete_user_from_booking(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            bookings.remove(booking)
            write(bookings)
            return response({"message": "User successfully deleted"}, 204)
    return response({"error": "User ID not found"}, 404)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
