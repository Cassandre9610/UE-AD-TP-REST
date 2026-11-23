from flask import Flask, jsonify, make_response
import copy
import json
import requests

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'
DB_PATH = '{}/databases/times.json'.format(".")
MOVIE_SERVICE_HOST = 'localhost:3200'

with open(DB_PATH, "r") as jsf:
   schedule:dict = json.load(jsf)["schedule"]


def write(new_schedule):
   global schedule
   with open(DB_PATH, "w") as f:
      full = {}
      full['schedule']=new_schedule
      json.dump(full, f)
      schedule = new_schedule


def error_not_found(message: str):
   return make_response(jsonify({"error": message}), 404)


def response(message, error_code):
    return make_response(jsonify(message), error_code)


def check_if_movie_exists(movie_id:str):
   res = requests.get(f"http://{MOVIE_SERVICE_HOST}/movies/movie/{movie_id}")
   return res.status_code == 200


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/json", methods=['GET'])
def get_json():
   return response(schedule, 200)


@app.route("/schedule/date/<date>/movie/<movie_id>", methods=['POST'])
def add_schedule(date, movie_id):
   if not check_if_movie_exists(movie_id):
      return error_not_found("Movie not found")

   for day in schedule:
      if day["date"] == date:
         if day["movies"].count(movie_id) == 0:
            day["movies"].append(movie_id)
            return response(day, 201)
         else :
            return response({"error": "Movie already scheduled for this date"}, 500)
   # aucune date ne correspond
   new_day = {
      "date": date,
      "movies": [movie_id]
   }
   schedule.append(new_day)
   write(schedule)
   return response(new_day, 201)


@app.route("/schedule/date/<date>", methods = ['GET'])
def get_by_date(date):
   for day in schedule:
      if day["date"] == date:
         return response(day, 200)
   return response({"error": "No schedule found for this date"}, 404)


@app.route("/schedule/movie/<movie_id>", methods = ['GET'])
def get_by_movie(movie_id):
   return_json: list = []
   for day in schedule:
      if day["movies"].count(movie_id) > 0 :
         return_json.append(day["date"])

   if len(return_json) == 0:
      return response({"error": "No schedule found for this date"}, 404)
   return response(return_json, 200)


@app.route("/schedule/date/<date>", methods=['DELETE'])
def delete_by_date(date):
   old_schedule = schedule
   new_schedule = [day for day in old_schedule if day["date"] != date]
   if new_schedule == old_schedule:
      return error_not_found("No date to delete")
   write(new_schedule)
   return response(new_schedule, 200)


@app.route("/schedule/date/<date>/movie/<movie_id>", methods=['DELETE'])
def delete_movie_from_date(date, movie_id):
   old_schedule: list[dict] = schedule
   new_schedule = []
   for day in old_schedule :
      new_day = copy.deepcopy(day)
      if new_day["date"] == date :
         new_day["movies"] = [movie for movie in new_day["movies"] if movie != movie_id]
      
      if len(new_day["movies"]) > 0 :
         new_schedule.append(new_day)

   if new_schedule == old_schedule:
      return error_not_found("Movie not found for the given date")

   write(new_schedule)
   return response(new_schedule, 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
