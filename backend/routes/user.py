from flask import request, jsonify
from config.db import user
from bson import ObjectId

def register():
    details = request.json
    check = list(user.find({"email":details['email']}))
    details['limit'] = 25
    if len(check) > 0 :
        return jsonify({"ok":False, "message":"User Already Registered"}), 400
    else :
        user.insert_one(details)
        return jsonify({"ok":True, "message":"Registration successfull"})


def login():
    details = request.json
    check = list(user.find({"email": details['email'], "password":details['password']}))
    if len(check) > 0:
        user_data = check[0]
        user_data['_id'] = str(user_data['_id'])  # Convert ObjectId to str
        
        return jsonify({
            "ok": True,
            "message": "Login Successful",
            "data": {
                'name': user_data['name'],
                'email': user_data['email'],
                'limit': user_data['limit'],
                'id': user_data['_id']
            },
        })
    else:
        return jsonify({"ok": False, "message": "Invalid Email or Password"})