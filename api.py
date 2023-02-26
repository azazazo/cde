from flask import Flask, request, Response
import flask
from flask_cors import CORS, cross_origin
import json
from base64 import b64encode

from voting import Server
from blockchain import Blockchain

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

blockchain = Blockchain()

server = Server([
    "John Doe",
    "Jane Smith",
    "Mike Johnson"
])



def b64(data: str) -> str:
    return b64encode(data.encode('utf-8')).decode('utf-8')


@app.route("/chain", methods=["GET"])
@cross_origin()
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    return json.dumps({
        "length": len(chain),
        "chain": chain
    })

@app.route("/vote", methods=["POST"])
@cross_origin()
def post_vote():
    # sai use json pls
    # expecting in form of {"id": "...", "vote": index}
    user_id = request.json["id"]
    vote_index = request.json["vote"]
    if check_user(user_id):
        return Response('{"message": "User has already voted"}', 401)
    else:
        print("gwa")
        votes = [0, 0, 0]
        votes[vote_index] = 1
        encrypted_votes = [server.encrypt(vote) for vote in votes]
        for candidate, vote in zip(server.candidates, encrypted_votes):
            candidate.votes *= vote
            candidate.votes %= server.public_key() ** 2
        blockchain.transact(user_id)
        blockchain.transact(str(encrypted_votes))
        blockchain.mine()
        return Response('{"message": "Vote successful"}', 200)


def decrypt_votes():
    return [server.decrypt(candidate.votes) for candidate in server.candidates]


def check_user(user_id):
    for block in blockchain.chain:
        if user_id in block.transactions:
            return True
    return False


@app.route("/results", methods=["GET"])
def get_results():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    json_data = json.dumps({
        "length": len(chain),
        "chain": chain
    })
    return Response(json_data, 200, mimetype="application/json")


@app.route("/pkey", methods=["GET"])
def get_pkey():
    l, mu = server.phe.private_keys
    return Response(json.dumps({"l": l, "mu": mu}), 200, mimetype="application/json")


@app.route("/decrypted_results", methods=["GET"])
def get_decrypted_results():
    return [server.decrypt(candidate.votes) for candidate in server.candidates]


if __name__ == "__main__":
    app.run(debug=True)
