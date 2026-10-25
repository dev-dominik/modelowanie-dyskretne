
import json
from fractions import Fraction
from pathlib import Path


def kernel(nazwa):
    # Ścieżka do pliku kernels.json
    sciezka = Path(__file__).resolve().parent / "data/kernels.json"

    # Wczytanie pliku JSON
    with open(sciezka, "r", encoding="utf-8") as plik:
        filtry = json.load(plik)

    # Sprawdzenie, czy kernel istnieje
    if nazwa not in filtry:
        raise ValueError(f"Nie znaleziono kernela: {nazwa}")

    # Pobranie macierzy wag
    dane = filtry[nazwa]
    r = dane["r"]

    # Konwersja liczb i ułamków na float
    kernel = [
        [float(Fraction(str(waga))) for waga in wiersz]
        for wiersz in dane["kernel"]
    ]

    # Sprawdzenie rozmiaru kernela
    if not isinstance(r, int) or not 0 <= r <= 10:
        raise ValueError("Promień musi być w zakresie 0-10")

    rozmiar = 2 * r + 1

    if len(kernel) != rozmiar or any(
        len(wiersz) != rozmiar for wiersz in kernel
    ):
        raise ValueError("Nieprawidłowy rozmiar kernela")

    return kernel, r
