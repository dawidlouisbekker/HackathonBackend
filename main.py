from flask import Flask, request, session, jsonify
from flask_session import Session
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
#from redis import Redis
import secrets
import random
import string
import hashlib
import os




app = Flask(__name__)

#for scalability of IV storage if redis server is running. Will use on cloud
#app.config["SESSION_TYPE"] = "redis"
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_USE_SIGNER"] = True
#app.config["SESSION_KEY_PREFIX"] = 'session:'
#app.config["SESSION_REDIS"] = Redis(host="localhost",port=6379,db=0)
app.config["SESSION_TYPE"] = 'filesystem'

Session(app)

key = "23908jowknw9n4wijnice"

def AESDecrypt(input, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(input.encode(),AES.block_size)
    

@app.route("/", methods = ["GET"])
async def verify():
    IV = GenerateIV()
    app.config["IV"] = IV
    hashobject = hashlib.md5(IV)
    app.config["Key"] = hashobject.hexdigest()
    print(app.config["Key"])
    print(IV)
    return IV

@app.route("/salt", methods=["POST"])
def GiveSalt():
    data = request.get_data()
    
    print(data.decode('utf-8'))
    a = secrets.choice(string.digits)
    b = secrets.choice(string.digits)
    c= secrets.choice(string.digits)
    x = secrets.choice(string.digits)
    context = random.randint(0,3)
    jsonvar = { "1": a,"2" : b,"3" : c, "4" : x, "5" : context} 
    return jsonify(jsonvar)


    
def GenerateIV():
    IV = get_random_bytes(16)
    return IV

@app.route("/login", methods=["POST"])
def login():
    print(app.config["IV"])
    credentials = request.get_json()
    
    username = credentials.get("username")
    password = credentials.get("password")
    hashed = str(hash(username))
    print(hashed)
    print(username, password)
    return "done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
