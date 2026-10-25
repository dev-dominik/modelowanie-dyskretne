from kernel import kernel
from operation import dylatacja, erozja, otwarcie, domkniecie, splot

kwadrat = "image/kwadrat.png"
kaczki = "image/kaczki.png"

bitmapa = "image/bitmapa.png"
bitmapa_zbinaryzowana = "image/bitmapa_zbinaryzowana.png"

# bialy:
# Piksele poza granicami obrazu przyjmują wartość 255 (biały kolor).

# zero:
# Piksele poza granicami obrazu przyjmują wartość 0 (czarny kolor).

# powielanie:
# Piksele poza granicami obrazu przyjmują wartość
# najbliższego piksela znajdującego się na krawędzi obrazu.

# odbicie:
# Piksele poza granicami obrazu są wyznaczane poprzez
# lustrzane odbicie pikseli znajdujących się wewnątrz obrazu.
# Piksele leżące na samej krawędzi nie są powtarzane.
warunek = "powielanie"

#ZADANIA

#operacje nałożenia filtru gaussa na własnej bitmapie i pochwal się efektem.
#zmodyfikuj filtr gaussa pokazując jak zmiana wartości w tym filtrze wpłynie na obraz
# (2 dodatkowe przypadki).

#JAK ZMIANA WARTOSCI W FILTRZE GAUSSA WPŁYWA NA ROZMYCIE OBRAZU???
#im większa waga środka, tym słabsze rozmycie,
#im większy udział sąsiadów, tym mocniejsze rozmycie,

if 1:
    kernel0, r0 = kernel("gauss")
    wynik = splot(bitmapa, kernel0, r0, warunek)
    wynik.save("wyniki_gauss/splot.png")

    kernel_gauss_1, r1 = kernel("gauss1")
    wynik = splot(bitmapa, kernel_gauss_1, r1, warunek)
    wynik.save("wyniki_gauss/splot_gauss_1.png")

    kernel_gauss_2, r2 = kernel("gauss2")
    wynik = splot(bitmapa, kernel_gauss_2, r2, warunek)
    wynik.save("wyniki_gauss/splot_gauss_2.png")

#3 różne operacje morfologiczne na własnej zbinaryzowanej bitmapie
if 0:
    wynik = erozja(bitmapa_zbinaryzowana, 5, warunek)
    wynik.save("wyniki_operacje_morfologiczne/erozja.png")
    wynik = dylatacja(bitmapa_zbinaryzowana, 5, warunek)
    wynik.save("wyniki_operacje_morfologiczne/dylatacja.png")
    wynik = otwarcie(bitmapa_zbinaryzowana, 5, warunek)
    wynik.save("wyniki_operacje_morfologiczne/otwarcie.png")

#własny filtr dolno-/górnoprzepustowy i zastosuj go na bitmapie z poprzedniego ćwiczenia
if 0:
    kernel_dolnoprzepustowy, r = kernel("dolnoprzepustowy")
    wynik = splot(bitmapa, kernel_dolnoprzepustowy, r, warunek)
    wynik.save("wyniki_filtry/dolnoprzepustowy.png")

    kernel_gornoprzepustowy, r = kernel("gornoprzepustowy")
    wynik = splot(bitmapa, kernel_gornoprzepustowy, r, warunek)
    wynik.save("wyniki_filtry/gornoprzepustowy.png")