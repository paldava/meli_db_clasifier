from flask import Blueprint


ping = Blueprint("ping", __name__)


@ping.route("/ping")
def main():
    return "pong"
