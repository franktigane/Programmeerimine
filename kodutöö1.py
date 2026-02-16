import unittest
# Impordime Python standardteegist unittest mooduli,
# mida kasutatakse ühikutestide (unit tests) kirjutamiseks ja käivitamiseks.


class Solution:
    # Solution klass vastab LeetCode'i nõuetele:
    # LeetCode kutsub selle klassi meetodit automaattestides

    def romanToInt(self, s: str) -> int:
        """
        Muudab Rooma numbrites esitatud arvu täisarvuks.

        :param s: Rooma number stringina (nt "MCMXCIV")
        :return: Vastav täisarv (nt 1994)
        """

        # Sõnastik, mis seob Rooma numbrid nende täisarvuliste väärtustega
        roman_values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        # Muutuja lõpptulemuse hoidmiseks
        total = 0

        # Käime Rooma numbri stringi läbi indeksite abil
        for i in range(len(s)):

            # Kontrollime, kas:
            # 1) järgmine sümbol eksisteerib
            # 2) praeguse sümboli väärtus on väiksem kui järgmise oma
            #
            # See katab lahutava notatsiooni juhud nagu:
            # IV (1 < 5), IX (1 < 10), XL (10 < 50), CM (100 < 1000)
            if i + 1 < len(s) and roman_values[s[i]] < roman_values[s[i + 1]]:
                # Lahutava notatsiooni puhul lahutame väärtuse
                total -= roman_values[s[i]]
            else:
                # Tavalisel juhul liidame väärtuse
                total += roman_values[s[i]]

        # Tagastame arvutatud täisarvu
        return total


class TestRomanToInteger(unittest.TestCase):
    # Testklass, mis pärib unittest.TestCase'ist
    # Iga meetod, mille nimi algab test_, on eraldi test

    def setUp(self):
        # setUp() käivitatakse ENNE igat testi
        # Siin loome Solution objekti, mida testides kasutada
        self.solution = Solution()

    def test_simple_numbers(self):
        # Testime lihtsaid Rooma numbreid ilma lahutava notatsioonita
        self.assertEqual(self.solution.romanToInt("I"), 1)
        self.assertEqual(self.solution.romanToInt("III"), 3)
        self.assertEqual(self.solution.romanToInt("VI"), 6)

    def test_subtractive_cases(self):
        # Testime lahutava notatsiooni juhte
        self.assertEqual(self.solution.romanToInt("IV"), 4)
        self.assertEqual(self.solution.romanToInt("IX"), 9)
        self.assertEqual(self.solution.romanToInt("XL"), 40)
        self.assertEqual(self.solution.romanToInt("CM"), 900)

    def test_complex_numbers(self):
        # Testime keerukamaid Rooma numbreid,
        # kus esinevad nii liitmine kui lahutamine
        self.assertEqual(self.solution.romanToInt("LVIII"), 58)
        self.assertEqual(self.solution.romanToInt("MCMXCIV"), 1994)
        self.assertEqual(self.solution.romanToInt("MMXXIII"), 2023)


# See tingimus tagab, et testid käivitatakse
# ainult siis, kui see fail käivitatakse otse
# (mitte siis, kui see imporditakse teise faili)
if __name__ == "__main__":
    unittest.main()
