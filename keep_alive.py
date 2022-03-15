from flask import Flask, request, make_response, Response
from threading import Thread
import json

app = Flask("")


async def take_input() -> dict:
    new = json.loads(input())
    return new


@app.route("/refresh", methods=["POST"])
async def refresh() -> Response:
    if request.method == "POST":
        print(
            "repl.deploy" + str(request.get_json()) + request.headers.get("Signature")
        )
        new = await take_input()
        try:
            return make_response(new.get("body"), int(new.get("status")))
        finally:
            print("repl.deploy-success")


@app.route("/")
def main():
    return "Your bot is alive!"


def run():
    app.run(host="0.0.0.0", port=7887)


def keep_alive():
    server = Thread(target=run)
    server.start()
