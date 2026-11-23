from flask import Flask, request, jsonify, make_response
import json

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]


def write(new_users):
   with open('{}/databases/users.json'.format("."), 'w') as f:
      full = {}
      full['users']=new_users
      json.dump(full, f)


def error_not_found(message: str):
   return make_response(jsonify({"error":message}), 404)


def response(message, error_code):
    return make_response(jsonify(message), error_code)


@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/json", methods=['GET'])
def get_json():
   return response(users, 200)


@app.route("/user/<user_id>", methods=['GET'])
def get_by_id(user_id):
   for user in users:
      if str(user["id"]) == str(user_id):
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/name/<user_name>", methods=["GET"])
def get_by_name(user_name):
   for user in users:
      if str(user["name"]) == str(user_name):
         return response(user, 200)
      
   return error_not_found("User name not found")


@app.route("/user/<user_id>/name/<new_name>", methods=["PUT"])
def update_user(user_id, new_name):
   for user in users:
      if str(user["id"]) == str(user_id):
         user["name"] = new_name
         write(users)
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
   for user in users:
      if str(user["id"]) == str(user_id):
         users.remove(user)
         write(users)
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/<user_id>", methods=['POST'])
def create_user(user_id):
   req = request.get_json()

   for user in users:
      if str(user["id"]) == str(user_id):
            print(user["id"])
            print(user_id)
            return response({"error": "User ID already exists"}, 500)

   # req["last_used"] = time.time_ns() # Pas certain de la methode
   users.append(req)
   write(users)
   return response({"message":"User added"}, 200)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
