from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)


from models.user import UserModel
from schemas.user import UserSchema

USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.set_password(user.password)
        user.save_to_db()
        return {"message": CREATED_SUCCESSFULLY}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user :
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

class ListUser(Resource):
    @classmethod
    def get(cls):
        return {"users": user_list_schema.dump(UserModel.find_all())}, 200

class LoginUser(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)

        if not user:
            return {"message": INVALID_CREDENTIALS}, 401

        if not user.check_password(user_data.password):
            return {"message": INVALID_CREDENTIALS}, 401

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {"username": user.username, "token":
                {
                    "access_token": access_token,
                    "resfresh_token": refresh_token
                }
        }, 200

class TokenRefresh(Resource):
     @classmethod
     @jwt_required(refresh=True)
     def post(cls):
         current_user = get_jwt_identity()
         new_token = create_access_token(identity=current_user, fresh=False)
         return {"access_token": new_token}, 200


