from flask import Flask, request, jsonify, make_response
import json
import time
from marshmallow import ValidationError
from schema.users_schema import UserCreateSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

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
@jwt_required()
def get_json():
   current_user = json.loads(get_jwt_identity())
   if current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)
   return response(users, 200)


@app.route("/user/<user_id>", methods=['GET'])
@jwt_required()
def get_by_id(user_id):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != user_id and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)
   
   for user in users:
      if str(user["id"]) == str(user_id):
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/name/<user_name>", methods=["GET"])
@jwt_required()
def get_by_name(user_name):
   current_user = json.loads(get_jwt_identity())
   if current_user["name"] != user_name and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   for user in users:
      if str(user["name"]) == str(user_name):
         return response(user, 200)
      
   return error_not_found("User name not found")


@app.route("/user/<user_id>/name/<new_name>", methods=["PUT"])
def update_user(user_id, new_name):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != user_id and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)
   
   for user in users:
      if str(user["id"]) == str(user_id):
         user["name"] = new_name
         write(users)
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/<user_id>", methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
   current_user = json.loads(get_jwt_identity())
   if current_user["id"] != user_id and current_user.get("admin") != True:
      return make_response({"error": "You don't have access to that information"}, 401)

   for user in users:
      if str(user["id"]) == str(user_id):
         users.remove(user)
         write(users)
         return response(user, 200)
      
   return error_not_found("User ID not found")


@app.route("/user/<user_id>", methods=['POST'])
def create_user(user_id):
   req = request.get_json(silent=True)
   if not req:
      return response({"error": "Invalid JSON data"}, 400)

   try:
      req = UserCreateSchema().load(req)
   except ValidationError as error:
      return response({"error": "Invalid JSON data", "details": error.messages}, 400)

   for user in users:
      if str(user["id"]) == str(user_id):
            return response({"error": "User ID already exists"}, 500)

   req["last_used"] = time.time_ns()
   users.append(req)
   write(users)
   return response({"message":"User added"}, 200)


@app.route("/login", methods=["POST"])
def login():
   req = request.get_json()
   for user in users:
      if user["id"] == req["id"]:
         token = create_access_token(identity = json.dumps(user))
         return make_response(jsonify(access_token = token), 200)

   return error_not_found("User ID not found")


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
