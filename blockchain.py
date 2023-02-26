import json
from hashlib import sha256
import time

DIFFICULTY = 2


class Block:
    def __init__(self, index: int, transactions: list, timestamp: float, previous_hash: str, nonce: int = 0) -> None:
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def is_valid_proof(self, block_hash: str) -> bool:
        return self.hash == block_hash and block_hash.startswith("0" * DIFFICULTY)

    @property
    def hash(self) -> str:
        return sha256(str(self).encode('utf-8')).hexdigest()

    def __str__(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True)


class Blockchain:
    def __init__(self) -> None:
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = Block(0, [], time.time(), "")
        self.chain.append(genesis_block)

    def proof(self, block: Block) -> str:
        block.nonce = 0
        while not block.hash.startswith("0" * DIFFICULTY):
            block.nonce += 1
        return block.hash

    def push(self, block: Block, proof: str) -> bool:
        previous_hash = self.back.hash
        if block.previous_hash != previous_hash:
            return False
        if not block.is_valid_proof(proof):
            return False
        # block.hash = proof
        self.chain.append(block)
        return True

    def transact(self, transaction: str) -> None:
        self.unconfirmed_transactions.append(transaction)

    def mine(self) -> int:
        if not self.unconfirmed_transactions:
            return -1

        last_block = self.back

        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof(new_block)
        self.push(new_block, proof)
        self.unconfirmed_transactions = []

        return new_block.index

    @property
    def back(self):
        return self.chain[-1]
