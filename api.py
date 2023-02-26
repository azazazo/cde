from flask import Flask, request, Response
import json
from base64 import b64encode

from voting import Server
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

server = Server()


def b64(data: str) -> str:
    return b64encode(data.encode('utf-8')).decode('utf-8')


@app.route("/chain", methods=["GET"])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    return json.dumps({
        "length": len(chain),
        "chain": chain
    })

@app.route("/key", methods=["GET"])
def get_key():
    return json.dumps(server.public_key())

@app.route("/vote", methods=["POST"])
def post_vote():
    pass

@app.route("/results", methods=["GET"])
def get_results():
    pass

# @app.route("/voter/new", methods=["POST"])
# def create_voter():
#     assert request.headers.get("Content-Type") == "application/json"
#
#     data = request.json
#
#     if data["username"] in voters:
#         return Response("User with username already exists!", 400, mimetype="text/plain")
#
#     try:
#         voters[data["username"]] = voter = Voter(data["username"], data["password"])
#     except ValueError as e:
#         return e
#
#     # blockchain.transact(b64(f"{voter.id},{voter.key.n}"))
#     # blockchain.mine()
#     return Response(f"User with username {data['username']} successfully created.", 201, mimetype="text/plain")


@app.route("/keys", methods=["GET"])
def get_keys():
    return Response(json.dumps(server.exposed_keys()), 200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
