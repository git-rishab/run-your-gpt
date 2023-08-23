from config.db import user
from flask_jwt_extended import create_access_token

# Creating a class to interact with database in more structured way

class User:
    def __init__(self, details):
        self.details = details

    def save(self):
        check = list(user.find({"email": self.details['email']}))
        if len(check) > 0:
            return {"ok": False, "message": "User Already Registered"}, 400
        else:
            user.insert_one(self.details)
            return {"ok": True, "message": "Registration successful"}

    @staticmethod
    def login(email, password):
        check = list(user.find({"email": email, "password": password}))
        if len(check) > 0:
            user_data = check[0]
            user_data['_id'] = str(user_data['_id'])  # Convert ObjectId to str
            access_token = create_access_token(identity=user_data)
            return {
                "ok": True,
                "message": "Login Successful",
                'token': access_token,
                "data": {
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'limit': user_data['limit'],
                    'id': user_data['_id'],
                },
            }
        else:
            return {"ok": False, "message": "Invalid Email or Password"}