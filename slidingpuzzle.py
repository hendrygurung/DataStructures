#Sliding Puzzle

from collections import deque

class BadMoveException (Exception):
    def __init__(self):
        pass


class PuzzleState (object):
    '''
    Abstracts a sliding puzzle with one gap. Internally stored as a flattened
    list called 'gamestate', with the gap represented as None.

    For details, see: https://github.com/rfdickerson/CS241/tree/master/A5
    '''

    def __init__(self, dimensions, gamestate, parent, lastMove):
        self.dimensions = dimensions
        self.gamestate = gamestate
        self.parent = parent
        self.lastMove = lastMove

    def coordToIndex(self, coord):
        '''Given an (x, y) tuple, return the index in the gamestate list
        corresponding to the tile at (x, y). Coordinates are zero-indexed.'''
        index = coord[1]*self.dimensions[0] + coord[0]
        return index
        

    def indexToCoord(self, index):
        '''Given a tile index into gamestate list, return the (x, y) tuple
        corresponding to that tile. Coordinates are zero-indexed.'''
        coord0 = index % self.dimensions[0]
        coord1 = index // self.dimensions[0]
        return (coord0, coord1) 
    
    def moveUp(self):
        '''Returns a new instance of PuzzleState where the gap and the value
        above it are flipped.'''
        count = 0
        for free in self.gamestate:
            if free == None:
                coord = self.indexToCoord(count)
                index = count
            else:
                count += 1
        if coord[1] == 0:
            raise BadMoveException
        else:
            tempgamestate = self.gamestate[:]
            replacendex = self.coordToIndex((coord[0], coord[1]-1))
            tempgamestate[index], tempgamestate[replacendex] = tempgamestate[replacendex], tempgamestate[index]
            return PuzzleState(self.dimensions, tempgamestate, self, 'Up')        

    def moveDown(self):
        '''Returns a new instance of PuzzleState where the gap and the value
        below it are flipped.'''
        count = 0
        for free in self.gamestate:
            if free == None:
                coord = self.indexToCoord(count)
                index = count
            else:
                count += 1
        if coord[1] == self.dimensions[1]-1:
            raise BadMoveException
        else:
            tempgamestate = self.gamestate[:]
            replacendex = self.coordToIndex((coord[0], coord[1]+1))
            tempgamestate[index], tempgamestate[replacendex] = tempgamestate[replacendex], tempgamestate[index]
            return PuzzleState(self.dimensions, tempgamestate, self, 'Down')

    def moveLeft(self):
        '''Returns a new instance of PuzzleState where the gap and the value
        to its left are flipped.'''
        count = 0
        for free in self.gamestate:
            if free == None:
                coord = self.indexToCoord(count)
                index = count
            else:
                count += 1
        if coord[0] == 0:
            raise BadMoveException
        else:
            tempgamestate = self.gamestate[:]
            replacendex = self.coordToIndex((coord[0]-1, coord[1]))
            tempgamestate[index], tempgamestate[replacendex] = tempgamestate[replacendex], tempgamestate[index]
            return PuzzleState(self.dimensions, tempgamestate, self, 'Left')        
    

    def moveRight(self):
        '''Returns a new instance of PuzzleState where the gap and the value
        to its right are flipped.'''
        count = 0
        for free in self.gamestate:
            if free == None:
                coord = self.indexToCoord(count)
                index = count
            else:
                count += 1
        if coord[0] == self.dimensions[0]-1:
            raise BadMoveException
        else:
            tempgamestate = self.gamestate[:]
            replacendex = self.coordToIndex((coord[0]+1, coord[1]))
            tempgamestate[index], tempgamestate[replacendex] = tempgamestate[replacendex], tempgamestate[index]
            return PuzzleState(self.dimensions, tempgamestate, self, 'Right')

    def __str__(self):
        '''Returns a string giving a human-readable representation of the
        puzzle's state.'''
        count = 0
        puzzle = ""
        for item in self.gamestate:
            puzzle += str(item)
            count += 1
            if count % self.dimensions[0] == 0:
                puzzle += "\n"
            else: 
                puzzle += " "
        return puzzle

    def __eq__(self, other):
        '''Tests whether two PuzzleState instances have the same gamestates.'''
        return self.gamestate == other.gamestate
             


class PuzzleSolver (object):
    '''Takes two instances of PuzzleState, an initial and final state, and
    determines the solution and some statistics to the problem.

    For details, see: https://github.com/rfdickerson/CS241/tree/master/A5'''

    def __init__(self, initial, goal):
        assert initial.dimensions == goal.dimensions, "initial and goal dimensions must be the same"
        self.initial = initial
        self.goal = goal

    def solve(self):
        '''Solves the puzzle and returns a list of the PuzzleStates used to get
        from the initial state to the goal state. The 0th element of the list
        should be the initial state stored at self.initial, and the last
        element of the list should be the goal state stored at self.goal.
        
        Tips! (er, requirements...)
        - Use deque from the collections module to keep track of pending
          states, that is, parents whose children need finding. Use append and
          popleft to push and pop items, respectively.
        - Keep track of states you've already found so you don't move back and
          forth between the same states forever. A Python list is fine here.
        - Keeping track of parents and moves in the constructor of the
          PuzzleState class means you don't need to do any weird additional
          linking stuff to keep track of the solution. It's already done!'''
        puzzlestates = deque()
        puzzlestates.append(self.initial)
        allpuzzle = []
        solution = []
        while len(puzzlestates):
            popleft = puzzlestates.popleft()
            if popleft == self.goal:
                while popleft != None:
                    solution.append(popleft)
                    popleft = popleft.parent
                break
            else:
                allpuzzle.append(popleft)
                try:
                    if popleft.moveUp() not in allpuzzle:
                        puzzlestates.append(popleft.moveUp())
                except:
                    BadMoveException
                try: 
                    if popleft.moveDown() not in allpuzzle:
                        puzzlestates.append(popleft.moveDown())
                except:
                    BadMoveException
                try: 
                    if popleft.moveLeft() not in allpuzzle:
                        puzzlestates.append(popleft.moveLeft())
                except:
                    BadMoveException
                try: 
                    if popleft.moveRight() not in allpuzzle:
                        puzzlestates.append(popleft.moveRight())
                except:
                    BadMoveException        
        return solution[::-1]
    
                    
            
    def movesToSolve(self):
        '''Returns a list of strings (in English) representing the directions
        to move the blank space in order to solve the puzzle. Depends on the
        solve method, above.'''

        solution = self.solve()

        # [1:] slicing omits the lastMove of the initial state, which is None
        return [ state.lastMove for state in solution[1:] ]


if __name__ == "__main__":
    dimensions = (3, 3)
    parent = lastMove = None
    initial = PuzzleState(dimensions, [2,8,3,1,6,4,7,None,5], parent, lastMove)
    goal = PuzzleState(dimensions, [None,2,3,1,8,6,7,5,4], parent, lastMove)
    solver = PuzzleSolver(initial, goal)
    soln = solver.solve()
    
