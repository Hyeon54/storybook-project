#기본 라우팅 설정
from flask import Blueprint, jsonify
import os

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "Hello from Flask!"})

@main.route("/apikey")
def get_api_key():
    return jsonify({"api_key": os.getenv("OPENAI_API_KEY")})