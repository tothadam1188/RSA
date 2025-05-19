import random
from math import gcd


def GyorsHatvanyozas(alap, kitevo, mod):
    eredmeny = 1
    alap %= mod
    while kitevo > 0:
        if kitevo % 2 == 1:
            eredmeny = (eredmeny * alap) % mod
        alap = (alap * alap) % mod
        kitevo //= 2
    return eredmeny


def MillerRabinTeszt(szam):
    if szam < 2 or szam % 2 == 0:
        return False
    d = szam - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in [2, 3]:
        if a >= szam:
            continue
        x = GyorsHatvanyozas(a, d, szam)
        if x == 1 or x == szam - 1:
            continue
        for _ in range(r - 1):
            x = GyorsHatvanyozas(x, 2, szam)
            if x == szam - 1:
                break
        else:
            return False
    return True


def PrimGeneralas(bitek=512):
    while True:
        p = random.getrandbits(bitek) | 1
        if MillerRabinTeszt(p):
            return p


def Euklideszi(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0


def KulcsGeneralas(bitek=512):
    p = PrimGeneralas(bitek)
    q = PrimGeneralas(bitek)
    while p == q:
        q = PrimGeneralas(bitek)
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    d, _ = Euklideszi(e, phi)
    d %= phi
    return (e, d, p, q)


def RSAKodolas(uzenet, e, p, q):
    n = p * q
    return GyorsHatvanyozas(uzenet, e, n)


def KinaiMaradektetel(c, d, p, q):
    M = p * q
    M1 = M // p
    M2 = M // q
    c1 = GyorsHatvanyozas(c, d % (p - 1), p)
    c2 = GyorsHatvanyozas(c, d % (q - 1), q)
    y1, y2 = Euklideszi(q, p)
    return (M1 * c1 * y1 + M2 * c2 * y2) % M


def RSADekodolas(c, d, p, q):
    n = p * q
    return KinaiMaradektetel(c, d, p, q) % n


def DigitalisAlairas(uzenet, d, p, q):
    n = p * q
    return GyorsHatvanyozas(uzenet, d, n)


def AlairasEllenorzes(uzenet, alairas, e, p, q):
    n = p * q
    ellenorzott_uzenet = GyorsHatvanyozas(alairas, e, n)
    return ellenorzott_uzenet == uzenet


if __name__ == "__main__":
    e, d, p, q = KulcsGeneralas(64)
    uzenet = 12345
    print("p:",p,"\tq:",q,"\te:",e,"\td:",d)
    kodolt = RSAKodolas(uzenet, e, p, q)
    dekodolt = RSADekodolas(kodolt, d, p, q)
    alairas = DigitalisAlairas(uzenet, d, p, q)
    ellenorzott = AlairasEllenorzes(uzenet, alairas, e, p, q)

    print("Eredeti:", uzenet)
    print("Titkositott:", kodolt)
    print("Visszafejtett:", dekodolt)
    print("Aláírás:", alairas)
    print("Ellenőrzés:", ellenorzott)
