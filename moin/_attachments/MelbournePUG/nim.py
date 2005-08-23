
class Game:
    def __init__(self, initialBoard):
        self.board = initialBoard
    def takeMatches(self, matches, pile):
        if matches < 1:
            raise MustTakePositiveMatchesError("Get real")
        if self.board[pile] < matches:
            raise NotEnoughMatchesError("Oh dear: pile " + str(pile) + " not big enough")
        self.board[pile] -= matches
        nonZeroPiles = [pile
                        for pile in self.board
                        if pile > 0]
        return len(nonZeroPiles) == 0

class NotEnoughMatchesError(Exception):
    pass
class MustTakePositiveMatchesError(Exception):
    pass
