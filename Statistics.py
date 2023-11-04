import json


class Statistics:
    """Klasa przechowująca dane statystyczne gracza."""

    def __init__(self):
        self.score = 0
        self.distance = 0
        self.bananas = 0
        self.hs = self.load_hs("SCORE")
        self.hd = self.load_hs("DISTANCE")
        self.hb = self.load_hs("BANANAS")

    def reset(self):
        """Tworzy domyślne zmienne klasy."""
        self.score = 0
        self.distance = 0
        self.bananas = 0
        self.load_highs()

    def load_highs(self):
        self.hs = self.load_hs("SCORE")
        self.hd = self.load_hs("DISTANCE")
        self.hb = self.load_hs("BANANAS")

    def compare(self):
        """Porównuje najlepszy wynik do aktualnie uzyskanego. Jeżeli jest
        większy zostaje podmieniony w pliku data.json."""
        if self.hs < self.score:
            self.save_hs(self.score, self.distance, self.bananas)

    def load_hs(self, type="SCORE"):
        """Wczytuje plik data.json z najwyższym wynikiem. Jeżeli taki
        istnieje zwraca trzy wartości kolejno: score, distance, bananas.
        Jeżeli taki nie istnieje, tworzy go z wartościami 0, 0, 0."""
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                for i in data:
                    if i == type:
                        return data[i]
                f.close()
        except FileNotFoundError:
            self.save_hs(0, 0, 0)

    def save_hs(self, score, distance, bananas):
        """Zapisuje najwyższy wynik do pliku data.json."""
        with open("data.json", "w") as f:
            text = {"SCORE": score,
                    "DISTANCE": distance,
                    "BANANAS": bananas}
            json.dump(text, f)
            f.close()
