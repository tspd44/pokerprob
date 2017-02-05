#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, string, sys
import random
import utils

numbs_symb = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"]
suits_symb = [u"\u2660", u"\u2665", u"\u2666", u"\u2663"]

class Card():

    def __init__(self, sui, num):
        self.num = num
        self.sui = sui

    def numb(self):
        return self.num

    def suit(self):
        return self.sui

    def to_string(self):
        return "{:>2}{}".format(utils.format_num(self.num), self.sui)


class Player():

    def __init__(self, id):
        self.id = id
        self.hand = ""
        self.cards = []

    def give_card(self, card):
        self.cards.append(card)

    def clear_cards(self):
        self.cards.clear()

    def get_hand(self):
        return self.hand

    def set_hand(self, hand):
        self.hand = hand

    def idt(self):
        return self.id

    def get_cards(self):
        return self.cards

    def cards_to_string(self):
        return "{}".format(self.cards[0].to_string()+
                           " "+
                           self.cards[1].to_string())


class Game():

    def __init__(self):

        self.players = []
        self.game = []
        self.flop = []
        self.ginst = []
        for its in suits_symb:
            for itn in numbs_symb:
                card = Card(its, itn)
                self.game.append(card)


    def fill_and_randomize(self):

        self.flop.clear()
        self.ginst.clear()
        random.shuffle(self.game)
        self.ginst.extend(self.game)
        for p in self.players:
            p.clear_cards()


    def compute(self):

        hands = []
        for p in self.players:
            avhand = p.get_cards() + self.flop
            hand = utils.compute(avhand)
            hands.append(hand)
            p.set_hand(hand)
        return hands


    def show(self):

        print("****************************************")
        print("flop :", end='')
        for c in self.flop:
            print(" {} ".format(c.to_string()), end='')
        print()
        print("****************************************")
        for p in self.players:
            print("player {:>2} | {} | has {}".format(p.idt(),
                p.cards_to_string(), p.get_hand()))
        print("****************************************")


    def show_stack(self):

        for i in range(len(self.game)):
            print("{},".format(self.game[i].to_string()), end='')
            if (i+1) % 13 == 0:
                print()


    def add_player(self, p):

        self.players.append(p)


    def deal_players(self):

        for x in range(2):
            for p in self.players:
                p.give_card(self.ginst.pop())


    def deal_flop(self):

        for i in range(3):
            self.flop.append(self.ginst.pop())
            # burn on
            self.ginst.pop()


    def deal_flop2(self):

        self.ginst.pop()
        self.flop.append(self.ginst.pop())


    def deal_flop3(self):

        self.ginst.pop()
        self.flop.append(self.ginst.pop())


## Main
#
if __name__ == '__main__':

    num_players = 1
    printing = False

    res = dict()
    game = Game()
    for i in range(num_players):
        game.add_player(Player(i+1))

    runs = 0
    while True:

        runs += 1

        game.fill_and_randomize()
        game.deal_players()
        game.deal_flop()
        game.deal_turn()
        game.deal_river()
 
        restmp = game.compute()
        for h in restmp:
            if h not in res:
                res[h] = 1
            else:
                res[h] += 1
 
        if runs % 500000 == 0:

            game.show()
            
            print("runs : {}".format(runs))
            keys = sorted(res, key=res.__getitem__)
            for key in keys:
                dec = "{:.5f}".format(res[key] * 100 / runs)
                print("{:>9} % {} ({})".format(dec, key, res[key]))
 
