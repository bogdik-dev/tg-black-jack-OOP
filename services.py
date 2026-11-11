#когда я создам игру(game = Game()) мне нужна будет колода, пустая рука игрока, пустая колода диллера
#self.deck.draw() - новая карта
#чтобы вызвать метод внутри другого метода того же класса, нужно писать self

from models import Koloda, Card

class Game:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = Koloda()  #готовая колода с перемешаными картами

    def start(self):
        for _ in range(2):  #просто а=выполни 2 раза - раздали по 2 карты
            self.player_hand.append(self.deck.draw())
            self.dealer_hand.append(self.deck.draw())

    def calculate_score(self, hand):
        summa = 0
        tysov = 0

        for i in hand:  #для каждой карты в руке
            summa += i.value() #мы можем пользоваться этим методом тк в hand лежат объекты class Card

            if i.sila == "Туз":
                tysov += 1

        while summa > 21 and tysov > 0: #tysov > 0 проверка есть ли тузы вообще
            summa -= 10
            tysov -= 1
        return summa

    def hit(self):  #выдать карту игроку
        self.player_hand.append(self.deck.draw())
        return self.player_hand

    def dealer_turn(self):  #логика диллера
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw())

    def winner(self):
        igrok_ocki = self.calculate_score(self.player_hand)
        diller_ocki = self.calculate_score(self.dealer_hand)
        if igrok_ocki > 21:
            return("Диллер выиграл")
        elif diller_ocki > 21:
            return("Игрок выиграл")
        elif igrok_ocki > diller_ocki:
            return("Игрок выиграл")
        elif diller_ocki > igrok_ocki:
            return("Диллер выиграл")
        else:
            return("Ничья")



