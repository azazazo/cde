from hashlib import sha256
from paillier import Paillier


class Server:
    def __init__(self, candidates=None):
        if candidates is None:
            candidates = []
        self.phe = Paillier()
        self.keys = self.phe.public_keys
        self.voters = {}
        self.candidates = candidates

    def public_key(self):
        return {"n": hex(self.keys)[2:]}


class Voter:
    def __init__(self, username, id):
        self.username = username
        # self.id = sha256((username + password).encode('utf-8'))
        self.id = id


class Candidate:
    def __init__(self, name: str) -> None:
        self.name = name
