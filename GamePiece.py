
class GamePiece:
    # pos = tuple of x,y coordinates
    # team = int 1 or 2
    # king = bool isKing
    def __init__(self, pos, team, king):
        self.pos = pos
        self.team = team
        self.king = king
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos):
        self.pos = pos

    def getTeam(self):
        return self.team
    
    def isKing(self):
        return self.king

    def kingMe(self):
        self.king = True
    
    def __str__(self):
        return f'{self.pos} team: {self.team} King: {self.king}'
