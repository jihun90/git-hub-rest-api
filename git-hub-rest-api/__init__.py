from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os
import requests
from urllib.parse import urlencode
from .Exception import GitHubException


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            headers = {"Accept": "application/json"}
            query_string = urlencode(request.get_json())
            github_oauth_url = f"{os.environ.get('GITHUB_OAUTH_URL')}?{query_string}"

            response = requests.post(github_oauth_url, headers=headers)
            token_json = response.json()
            error = token_json.get("error", None)

            if error is not None:
                raise GitHubException("can not have git acess tocken")

            return token_json

        return "Error"

    @app.route("/user", methods=["POST"])
    def get_user_info():
        acess_token = request.get_json()["access_tocken"]
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {acess_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(
            os.environ.get("GITHUB_API_URL") + "/user", headers=headers
        )

        if response.status_code != 200:
            raise GitHubException("can not have user info")

        return response.json()

    return app
