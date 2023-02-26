from Crypto.Util.number import getPrime, bytes_to_long, getRandomRange


class Paillier:
    def __init__(self, nbits=1024):
        self.p = getPrime(nbits)
        self.q = getPrime(nbits)

        self.n = self.p * self.q
        self.l = (self.p - 1) * (self.q - 1)

        self.mu = pow(self.l, -1, self.n)
        # value of n+1 satisfies the condition that n divides order of g in Zmod(n^2)
        # only including it here for ease of convenience; for actual public key will
        # only send value of n
        self.g = self.n + 1

    def encrypt(self, message):
        if isinstance(message, str):
            message = bytes_to_long(message.encode('utf-8'))
        # print(message)
        assert message < self.n
        r = self.p
        while r in [self.p, self.q]:
            r = getRandomRange(0, self.n)

        return (pow(self.g, message, self.n ** 2) * pow(r, self.n, self.n ** 2)) % self.n ** 2

    def decrypt(self, ciphertext):
        return ((pow(ciphertext, self.l, self.n ** 2) // self.n) * self.mu) % self.n

    @property
    def public_keys(self):
        return self.n

    @property
    def private_keys(self):
        return self.l, self.mu


if __name__ == "__main__":
    paillier = Paillier()
    for i in range(100):
        a = getRandomRange(0, 10 ** 9)
        b = getRandomRange(0, 10 ** 9)
        assert a + b == paillier.decrypt((paillier.encrypt(a) * paillier.encrypt(b)) % paillier.n ** 2)

    unique = set()
    for i in range(100):
        unique.add(paillier.encrypt(0))
    assert len(unique) == 100
