#Карта. У неё есть масть (пики, черви) и сила (Туз, Король, 2, 3). И у неё есть вес (сколько очков она дает)
#Колода. Коробка, в которой лежат 52 карты. Её можно перемешать и из неё можно вытянуть одну карту.
#Игрок и Дилер. У них есть руки, в которых лежат карты
#Карта, колода - это объект (экземпляр класса). Значит, нам нужны два класса: Card (карта) и Koloda (колода)
import random

class Card:
    ochki = {   #переменная класса, могу обращаться как self.ochki
        "Валет": 2,
        "Дама": 3,
        "Король": 4
    }

    def __init__(self, mast, sila):
        self.mast = mast  #"♠", "♥", "♦", "♣"
        self.sila = sila  #валет, дама, 2, 6

    def value(self):  #сколько очков дает карта
        if self.sila in self.ochki:  #если в силе есть что то из ключей словаря
            return self.ochki[self.sila]
        elif self.sila == "Туз":
            return 11
        else:
            return int(self.sila) #если это не валет дама король или туз то значит число

    def __str__(self):
        # Добавил, чтобы карты красиво печатались в боте (Валет♠)
        return f"{self.sila}{self.mast}"


class Koloda:
    def __init__(self):
        self.cards = []

        ranks = [str(x) for x in range(2,11)] + ["Валет", "Дама", "Король", "Туз"]
        suits = ["♠", "♥", "♦", "♣"]
                            #все внуть инит чтобы при вызове класса оно это все прочиталось
        for i in ranks:
            for i2 in suits:
                new_card = Card(i2, i)  #Композиция
                self.cards.append(new_card) #self.cards = [Card(...), Card(...), ...]

        random.shuffle(self.cards) # Перемешиваем колоду

    def draw(self):
        return self.cards.pop() #дает карту и забирает из колоды чтобы колода пустела