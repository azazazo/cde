from hashlib import sha256
from paillier import Paillier


class Server:
    def __init__(self, candidates=None):
        if candidates is None:
            candidates = []
        self.phe = Paillier()
        self.keys = self.phe.public_keys
        self.voters = {}
        self.candidates = [Candidate(candidate) for candidate in candidates]
        for candidate in self.candidates:
            candidate.votes = self.encrypt(0)

    def public_key(self):
        return self.keys

    def encrypt(self, message):
        return self.phe.encrypt(message)

    def decrypt(self, ciphertext):
        return self.phe.decrypt(ciphertext)


class Voter:
    def __init__(self, username, id):
        self.username = username
        # self.id = sha256((username + password).encode('utf-8'))
        self.id = id


class Candidate:
    def __init__(self, name: str) -> None:
        self.name = name
        self.votes = 0
