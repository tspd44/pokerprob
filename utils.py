#!/usr/bin/python3
# -*- coding: utf-8 -*-

import poker

def format_num(num):

    if num == "1":
        return "A"
    if num == "11":
        return "J"
    if num == "12":
        return "Q"
    if num == "13":
        return "K"
    return num


def flush_type(cards):

    scards = sorted(cards, key=lambda card: int(card.num))
    hands = dict()
    for c in scards:
        if c.suit() not in hands:
            hands[c.suit()] = [c]
        else:
            hands[c.suit()].append(c)

    # check if royal
    for h in hands.values():
        if len(h) < 5:
            continue
        if not h[0].numb() == "1":
            continue
        tpl_nums = ["10", "11", "12", "13"]
        for c in reversed(h):
            if c.num != tpl_nums.pop():
                break
            if len(tpl_nums) == 0:
                return True, True

    # check if straight
    for h in hands.values():
        if len(h) < 5:
            continue
        if h[0].numb() == "1":
            h.append(h[0])
        res = 0
        last = -1
        for c in reversed(h):
            if last == -1:
                last = int(c.numb())
                res += 1
                continue
            if last == 1 and c.numb() == "13":
                last = 13
                res += 1
                continue
            if (last - int(c.numb())) != 1:
                res = 0
            else:
                res += 1
            last = int(c.numb())
            if res > 4:
                return True, False

    return False, False


def has_flush(cards_suis):

    if 5 in cards_suis.values() or \
       6 in cards_suis.values() or \
       7 in cards_suis.values():
        return True
    return False


def has_straight(cards_nums):

    list_num = []
    for x in poker.numbs_symb:
        list_num.append(cards_nums[x])
    list_num.append(cards_nums["1"])
    res = 0
    for it in reversed(list_num):
        if it > 0:
            res += 1
        else:
            res = 0
        if res > 4:
            return True
    return False


def compute(cards):

    # Init arrays
    cards_nums = dict()
    for itn in poker.numbs_symb:
        cards_nums[itn] = 0 
    cards_suis = dict()
    for its in poker.suits_symb:
        cards_suis[its] = 0 

    for c in cards:
        # Summing how many occurence by kind
        cards_nums[c.numb()] += 1
        # Summing how many occurence by suit
        cards_suis[c.suit()] += 1

    flush = has_flush(cards_suis)
    straight = has_straight(cards_nums)

    if flush and straight:

        fstraight, froyal = flush_type(cards)
        # ROYAL FLUSH
        if froyal:
            return "royal flush"
        # STRAIGHT FLUSH
        if fstraight:
            return "straight flush"

    # FOUR OF A KIND
    if 4 in cards_nums.values():
        return "four of a kind"

    # FULL HOUSE
    three_same_kind = False
    at_least_two_same_kind = False
    for occ in cards_nums.values():
        if occ == 3 and not three_same_kind:
            three_same_kind = True
            continue
        if occ > 1:
            at_least_two_same_kind = True

    if three_same_kind and at_least_two_same_kind:
        return "full house"

    # FLUSH
    if flush:
        return "flush"

    # STRAIGHT
    if straight:
        return "straight"

    # THREE OF A KIND
    if three_same_kind:
        return "three of a kind"

    # ONE OR TWO PAIRS
    pairs = 0
    for occ in cards_nums.values():
        if occ == 2:
            pairs += 1

    if pairs > 1:
        return "2 pairs"
    if pairs > 0:
        return "pair"

    return "nothing"


