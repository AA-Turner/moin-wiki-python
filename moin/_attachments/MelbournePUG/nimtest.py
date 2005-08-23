#!/usr/bin/env python

import unittest
from nim import *

class GameTests(unittest.TestCase):
    def testEmptyGame(self):
        game = Game([])
        self.assertEquals(len(game.board), 0)

    def testGameWithOnePileOfOneMatch(self):
        game = Game([1])
        self.assertEquals(len(game.board), 1)
        self.assertEquals(game.board[0], 1)

    def testGameWithTwoPiles(self):
        game = Game([1, 1])
        self.assertEquals(len(game.board), 2)
        
    def testTakeOneMatchFromOnePile(self):
        game = Game([1])
        win = game.takeMatches(matches=1, pile=0)
        self.assertEquals(game.board[0], 0)
        self.assertEquals(win, True)
        self.assertEquals(len(game.board), 1)

    def testTakeOneMatchFromTwoPiles(self):
        game = Game([1, 6])
        win = game.takeMatches(matches=1, pile=0)
        self.assertEquals(game.board[1], 6)
        self.assertEquals(win, False)
        self.assertEquals(len(game.board), 2)

    def testTakeTwoMatchesWhenTheresOnlyOne(self):
        game = Game([1])
        self.assertRaises(NotEnoughMatchesError, game.takeMatches, matches=2, pile=0)

    def testTakeNegativeMatches(self):
        game = Game([1])
        try:
            win = game.takeMatches(matches=-1, pile=0)
            self.fail()
        except MustTakePositiveMatchesError, e:
            # Expected
            pass

    def testTakeZeroMatches(self):
        game = Game([1])
        try:
            win = game.takeMatches(matches=0, pile=0)
            self.fail()
        except MustTakePositiveMatchesError, e:
            # Expected
            pass

    

if __name__ == "__main__":
    unittest.main()

