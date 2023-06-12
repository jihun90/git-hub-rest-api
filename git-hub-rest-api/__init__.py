from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os
import requests
from urllib.parse import urlencode


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    @app.route("/")
    def hello_pybo():
        return "Hello, Pybo!"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # client_id = request.get_data("cleint_id")
            # client_secrets = request.get_data("client_secrets")
            headers = {"Accept": "application/json"}
            query_string = urlencode(request.get_json())
            github_oauth_url = f"{os.environ.get('GITHUB_OAUTH_URL')}?{query_string}"

            response = requests.post(github_oauth_url, headers=headers)
            token_json = response.json()
            error = token_json.get("error", None)

            if error is not None:
                raise Exception("Error")

            return token_json

        return "Error"

    def build_actual_response(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return app
