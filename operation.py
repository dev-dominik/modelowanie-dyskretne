from PIL import Image

def przygotuj_obraz(zrodlo):
    if isinstance(zrodlo, Image.Image):
        obraz = zrodlo.convert("L")
    else:
        with Image.open(zrodlo) as plik:
            obraz = plik.convert("L")

    # Zmniejszenie rozdzielczości
   # obraz.thumbnail((300, 300))

    return obraz


def warunek_brzegowy(piksele, x, y, szerokosc, wysokosc, warunek="bialy"):

    if 0 <= x < szerokosc and 0 <= y < wysokosc:
        return piksele[y * szerokosc + x]

    if warunek == "zero":
        return 0

    elif warunek == "bialy":
        return 255

    elif warunek == "powielanie":
        x = max(0, min(x, szerokosc - 1))
        y = max(0, min(y, wysokosc - 1))

    elif warunek == "odbicie":

        def odbij(wspolrzedna, rozmiar):
            if rozmiar == 1:
                return 0

            okres = 2 * rozmiar - 2
            wspolrzedna %= okres

            if wspolrzedna >= rozmiar:
                wspolrzedna = okres - wspolrzedna

            return wspolrzedna

        x = odbij(x, szerokosc)
        y = odbij(y, wysokosc)

    else:
        raise ValueError("Nieznany warunek brzegowy")

    return piksele[y * szerokosc + x]


def dylatacja(zrodlo, i, warunek="bialy"):
    if not 3 <= i <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")

    obraz = przygotuj_obraz(zrodlo)

    szerokosc, wysokosc = obraz.size
    piksele = list(obraz.getdata())
    nowe_piksele = []

    for y in range(wysokosc):
        for x in range(szerokosc):

            nowa_wartosc = 255

            for dy in range(-i, i + 1):
                for dx in range(-i, i + 1):

                    piksel = warunek_brzegowy(
                        piksele,
                        x + dx,
                        y + dy,
                        szerokosc,
                        wysokosc,
                        warunek
                    )

                    # Jeśli choć jeden piksel jest czarny
                    if piksel == 0:
                        nowa_wartosc = 0
                        break

                if nowa_wartosc == 0:
                    break

            nowe_piksele.append(nowa_wartosc)

    wynik = Image.new("L", (szerokosc, wysokosc))
    wynik.putdata(nowe_piksele)

    return wynik


def erozja(zrodlo, i, warunek="bialy"):
    if not 3 <= i <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")

    obraz = przygotuj_obraz(zrodlo)

    szerokosc, wysokosc = obraz.size
    piksele = list(obraz.getdata())
    nowe_piksele = []

    for y in range(wysokosc):
        for x in range(szerokosc):

            nowa_wartosc = 0

            for dy in range(-i, i + 1):
                for dx in range(-i, i + 1):

                    piksel = warunek_brzegowy(
                        piksele,
                        x + dx,
                        y + dy,
                        szerokosc,
                        wysokosc,
                        warunek
                    )

                    # Jeśli choć jeden piksel jest biały
                    if piksel == 255:
                        nowa_wartosc = 255
                        break

                if nowa_wartosc == 255:
                    break

            nowe_piksele.append(nowa_wartosc)

    wynik = Image.new("L", (szerokosc, wysokosc))
    wynik.putdata(nowe_piksele)

    return wynik


def otwarcie(zrodlo, i, warunek="bialy"):
    if not 3 <= i <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")
    wynik_erozji = erozja(zrodlo, i, warunek)
    wynik_dylatacji = dylatacja(wynik_erozji, i, warunek)

    return wynik_dylatacji


def domkniecie(zrodlo, i, warunek="bialy"):
    if not 3 <= i <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")

    wynik_dylatacji = dylatacja(zrodlo, i, warunek)
    wynik_erozji = erozja(wynik_dylatacji, i, warunek)

    return wynik_erozji


def splot(sciezka, kernel, r, warunek="powielanie"):
    if not 3 <= r <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")

    # Wczytanie obrazu i konwersja na RGB
    obraz = Image.open(sciezka).convert("RGB")
    obraz.thumbnail((300, 300))
    obraz.save("splot_wejscie.png")

    szerokosc, wysokosc = obraz.size

    if not 3 <= r <= 10:
        raise ValueError("Promień musi być w zakresie 3-10")

    rozmiar = 2 * r + 1

    if len(kernel) != rozmiar or any(
        len(wiersz) != rozmiar for wiersz in kernel
    ):
        raise ValueError("Nieprawidłowy rozmiar kernela")

    # Pobranie pikseli do listy
    piksele = list(obraz.getdata())

    # Lista wynikowych pikseli
    nowe_piksele = []

    for y in range(wysokosc):
        for x in range(szerokosc):

            nowa_wartosc = [0.0, 0.0, 0.0]

            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):

                    nx = x + dx
                    ny = y + dy

                    # Warunki brzegowe
                    if warunek == "powielanie":
                        nx = max(0, min(nx, szerokosc - 1))
                        ny = max(0, min(ny, wysokosc - 1))
                        piksel = piksele[ny * szerokosc + nx]

                    elif warunek == "zero":
                        if 0 <= nx < szerokosc and 0 <= ny < wysokosc:
                            piksel = piksele[ny * szerokosc + nx]
                        else:
                            piksel = (0, 0, 0)

                    else:
                        raise ValueError("Nieznany warunek brzegowy")

                    # Waga z kernela
                    waga = kernel[r - dy][r - dx]

                    # Obliczenia dla R, G i B
                    for kanal in range(3):
                        nowa_wartosc[kanal] += piksel[kanal] * waga

            # Ograniczenie wartości do zakresu 0-255
            nowa_wartosc = [
                max(0, min(255, round(wartosc)))
                for wartosc in nowa_wartosc
            ]

            nowe_piksele.append(tuple(nowa_wartosc))

    # Utworzenie obrazu wynikowego
    wynik = Image.new("RGB", (szerokosc, wysokosc))
    wynik.putdata(nowe_piksele)

    return wynik

