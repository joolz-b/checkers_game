from GamePiece import GamePiece

class Board:
    # Can provide a 2D array of pieces to load an existing board, else, it will load a starting board based on the dimensions
    def __init__(self, dimension, pieces = None):
        self.dimension = dimension
        self.team_1 = []
        self.team_2 = []
        self.positions = [[]]*dimension
        for i in range(dimension):
            self.positions[i] = [None] * dimension
        if not pieces:
            for x in range(dimension//2-1):
                for y in range(dimension):
                    if(x % 2==0):
                        if(y%2==0):
                            piece = GamePiece((x,y), 1, False)
                            self.team_1.append(piece)
                            self.positions[x][y] = piece
                    else:
                        if(y%2==1):
                            piece = GamePiece((x,y), 1, False)
                            self.team_1.append(piece)
                            self.positions[x][y] = piece
            for x in range(dimension-1, dimension//2, -1):
                for y in range(dimension):
                    if(x % 2==0):
                        if(y%2==0):
                            piece = GamePiece((x,y), 2, False)
                            self.team_2.append(piece)
                            self.positions[x][y] = piece
                    else:
                        if(y%2==1):
                            piece = GamePiece((x,y), 2, False)
                            self.team_2.append(piece)
                            self.positions[x][y] = piece
        else:
            for piece in pieces:
                if piece.getTeam() == 1:
                    self.team_1.append(piece)
                else:
                    self.team_2.append(piece)
                pos = piece.getPos()
                self.positions[pos[0]][pos[1]] = piece


    def getDimension(self):
        return self.dimension

    def getNumPieces(self):
        return self.numPieces

    def checkMoveLegal(self, pos, movePos, team):
        moveLegal = True
        if self.checkMovePossible(pos, movePos, team) == False:
            moveLegal = False
        elif self.checkJumpAvailable(team):
            if self.checkMoveJump(pos, movePos)==False:
                moveLegal = False
        return moveLegal
    
    def movePiece(self, pos, movePos, team):
        makeAnotherMove = False
        if self.checkMoveLegal(pos, movePos, team):
            piece = self.positions[pos[0]][pos[1]]
            piece.setPos(movePos)
            self.positions[movePos[0]][movePos[1]] = piece
            self.positions[pos[0]][pos[1]] = None

            #Now King me
            if team ==1 and movePos[0] == self.dimension-1:
                piece.kingMe()
            elif team==2 and movePos[0] == 0:
                piece.kingMe()
            if self.checkMoveJump(pos, movePos):
                self.removeJumpedPiece(pos, movePos)
                if self.checkJumpAvailable(team):
                    makeAnotherMove = True
        else:
            print("Something went wrong, this is not a legal move")
        return makeAnotherMove

    # Returns 0 if game isn't over. Else returns winning team.
    def checkWinner(self):
        winner = 0
        if len(self.team_1) == 0:
            winner = 2
        elif len(self.team_2) == 0:
            winner = 1
        return winner

    def exportPieces(self):
        pieces = []
        for piece in self.team_1:
            pieces.append(piece)
        for piece in self.team_2:
            pieces.append(piece)
        return pieces

    # For troubleshooting
    def __str__(self):
        string  = ""
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.positions[x][y]:
                    string+= f' * {self.positions[x][y].getTeam()} * |'
                else:
                    string+=" Empty |"
            string += "\n"
        return string

    #for testing/troubleshooting
    def checkAllMoves(self):
        team = 1
        for x in range(self.dimension):
            for y in range(self.dimension):
                if self.positions[x][y]:
                    team = self.positions[x][y].getTeam()
                print(x, y, self.checkMoves((x,y), team))

    def checkMovePossible(self, pos, movePos, team):
        return movePos in self.checkMoves(pos, team)

    def checkMoveJump(self, pos, movePos):
        return abs(pos[0] - movePos[0])  == 2 and abs(pos[1] - movePos[1])  == 2

    def checkJumpAvailable(self, team):
        if team ==1:
            team_pieces = self.team_1
        else:
            team_pieces = self.team_2
        jumpAvailable = False
        for piece in team_pieces:
            pieceMoves = self.checkMoves(piece.getPos(), team)
            for move in pieceMoves:
                if move:
                    if self.checkMoveJump(piece.getPos(), move):
                        jumpAvailable = True
                        break
            else:
                continue
            break
        return jumpAvailable

    def removeJumpedPiece(self, pos, move):
        removeX = -1
        removeY = -1
        if pos[0] - move[0] == 2:
            removeX = pos[0]-1
        elif pos[0] - move[0] == -2:
            removeX = pos[0]+1
        if pos[1] - move[1] == 2:
            removeY = pos[1]-1
        elif pos[1] - move[1] == -2:
            removeY = pos[1]+1
        if removeX != -1 and removeY != -1:
            removePos = (removeX, removeY)
            team = self.positions[removeX][removeY].getTeam()
            self.positions[removeX][removeY] = None
            if team == 1:
                team_pieces = self.team_1
            else:
                team_pieces = self.team_2
            removeIndex = -1
            for index in range(len(team_pieces)):
                if team_pieces[index].getPos() == removePos:
                    removeIndex = index
                    break
            team_pieces.pop(removeIndex)
        else:
            print("Something went wrong, this move shouldn't remove anything")

    # given a position and the current team, it returns a list of possible moves that piece can make.
    # each index in the returned list represents a direction with order: Up-left, Up-Right, Down-Left, Down-Right
    def checkMoves(self, pos, team):
        possibleMoves = [None]*4
        piece = self.positions[pos[0]][pos[1]]
        if piece and piece.getTeam() == team:
            #Up-left
            if pos[0] != 0:
                if piece.getTeam() == 2 or piece.isKing():
                    if pos[1] != 0:
                        if self.positions[pos[0]-1][pos[1]-1] == None:
                            possibleMoves[0] = (pos[0]-1, pos[1]-1)
                        elif self.positions[pos[0]-1][pos[1]-1].getTeam() != team:
                            if pos[0] != 1 and pos[1] != 1:
                                if self.positions[pos[0]-2][pos[1]-2] == None:
                                    possibleMoves[0] = (pos[0]-2, pos[1]-2)
                    #Up-Right
                    if pos[1] != self.dimension-1:
                        if self.positions[pos[0]-1][pos[1]+1] == None:
                            possibleMoves[1] = (pos[0]-1, pos[1]+1)
                        elif self.positions[pos[0]-1][pos[1]+1].getTeam() != team:
                            if pos[0] != 1 and pos[1] != self.dimension-2:
                                if self.positions[pos[0]-2][pos[1]+2] == None:
                                    possibleMoves[1] = (pos[0]-2, pos[1]+2)
            #Down-left
            if pos[0] != self.dimension-1:
                if piece.getTeam() == 1 or piece.isKing():
                    if pos[1] != 0:
                        if self.positions[pos[0]+1][pos[1]-1] == None:
                            possibleMoves[2] = (pos[0]+1, pos[1]-1)
                        elif self.positions[pos[0]+1][pos[1]-1].getTeam() != team:
                            if pos[0] != self.dimension-2 and pos[1] != 1:
                                if self.positions[pos[0]+2][pos[1]-2] == None:
                                    possibleMoves[2] = (pos[0]+2, pos[1]-2)
                    # Down-Right
                    if pos[1] != self.dimension-1:
                        if self.positions[pos[0]+1][pos[1]+1] == None:
                            possibleMoves[3] = (pos[0]+1, pos[1]+1)
                        elif self.positions[pos[0]+1][pos[1]+1].getTeam() != team:
                            if pos[0] != self.dimension-2 and pos[1] != self.dimension-2:
                                if self.positions[pos[0]+2][pos[1]+2] == None:
                                    possibleMoves[3] = (pos[0]+2, pos[1]+2)
        return possibleMoves    


    
