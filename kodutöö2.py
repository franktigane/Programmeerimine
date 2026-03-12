from abc import ABC, abstractmethod
import random


# ABSTRAKTSIOON
# Tegelane on abstraktne klass.
# See määrab üldise struktuuri kõikidele tegelastele.

class Tegelane(ABC):

    def __init__(self, nimi, elu):

        # KAPSELDAMINE

        # Elupunktid on peidetud (_elu)
        # Neid ei tohi muuta otse väljastpoolt
        self.nimi = nimi
        self._elu = elu

    # abstraktne meetod – iga alamklass peab selle ise ümber muutma temale vastavaks
    @abstractmethod
    def ründa(self, vastane):
        pass

    # ühine meetod kõigile tegelastele
    def võta_kahju(self, kahju):
        self._elu -= kahju

        # elu ei tohi minna alla 0
        if self._elu < 0:
            self._elu = 0

        print(f"{self.nimi} sai {kahju} kahju. Elu alles: {self._elu}")

    def on_elus(self):
        return self._elu > 0



# PÄRILUS

# Sõdalane pärib klassist Tegelane

class Sõdalane(Tegelane):


    # POLÜMORFISM

    # sama meetod ründa(), aga erinev käitumine
    def ründa(self, vastane):
        kahju = random.randint(10, 20)
        print(f"{self.nimi} lööb mõõgaga!")
        vastane.võta_kahju(kahju)


class Maag(Tegelane):

    def __init__(self, nimi, elu, mana):
        super().__init__(nimi, elu)


        # KAPSELDAMINE

        self._mana = mana

    # POLÜMORFISM
    def ründa(self, vastane):

        if self._mana <= 0:
            print(f"{self.nimi} üritab loitsu teha, aga mana on otsas!")
            return

        kahju = random.randint(15, 25)
        self._mana -= 10

        if self._mana < 0:
            self._mana = 0

        print(f"{self.nimi} viskab tuleloitsu! Mana alles: {self._mana}")
        vastane.võta_kahju(kahju)


class Vibukütt(Tegelane):

    def __init__(self, nimi, elu, nooled):
        super().__init__(nimi, elu)


        # KAPSELDAMINE

        self._nooled = nooled

    # POLÜMORFISM
    def ründa(self, vastane):

        if self._nooled <= 0:
            print(f"{self.nimi} tahab tulistada, aga nooled on otsas!")
            return

        kahju = random.randint(8, 18)
        self._nooled -= 1

        if self._nooled < 0:
            self._nooled = 0

        print(f"{self.nimi} laseb noole! Nooled alles: {self._nooled}")
        vastane.võta_kahju(kahju)



# LAHINGU FUNKTSIOON
# Polümorfism: funktsioon ei kontrolli tüüpe
# Ta kasutab lihtsalt meetodit ründa()

def lahing(t1, t2):

    print(f"\nAlgab lahing: {t1.nimi} vs {t2.nimi}\n")

    while t1.on_elus() and t2.on_elus():

        t1.ründa(t2)

        if not t2.on_elus():
            print(f"\n{t2.nimi} sai surma!")
            print(f"Võitja on {t1.nimi}")
            break

        t2.ründa(t1)

        if not t1.on_elus():
            print(f"\n{t1.nimi} sai surma!")
            print(f"Võitja on {t2.nimi}")
            break


# PROGRAMMI TEST

s1 = Sõdalane("Kapten Ameerika", 100)
m1 = Maag("Gandalf", 80, 50)
v1 = Vibukütt("Andrus", 90, 10)

lahing(s1, m1)

# Kui lisada uus tegelane (nt "Rüütel" või "Meelis"),
# siis tuleb:
# 1. Luua uus klass, mis pärib klassist Tegelane
# 2. Implementerida meetod ründa()
# Lahingu funktsiooni ei pea muutma, sest see kasutab polümorfismi.