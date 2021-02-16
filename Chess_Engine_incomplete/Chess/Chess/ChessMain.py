"""
Main driver file. Handles user input and displays current GameState object.
"""
# Libraries
import pygame as p
from Chess import ChessEngine

# Global Parameters
WIDTH = HEIGHT = 512
DIMENSION = 8 # chess boards are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

# Loading in the images
'''
Initilialize a global dictionary of images. This will be called once in the main 
'''
def loadImages():
    pieces = ["wp", "bp", "wR", "bR", "wB", "bB", "wN", "bN", "wK", "bK", "wQ", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/"+piece+".png"),
                                          (SQ_SIZE, SQ_SIZE))
        # Can access an image by using the dictionary 'IMAGES["wp"]'
"""
Main driver for our code. Handel user input and update graphics 
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # only do this once
    running = True
    sqSelected = () #no square selected initialy. Keep track of last click of the user
    playerClicks = [] #keep track of the player clicks two tuples: [(6,4),(4,3)]

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x and y location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected=(row, col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd click
                if len(playerClicks) == 2: # After the 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getcoordssytem())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all the graphics within a game state
"""
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

"""
Draw the squares on the board 
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))
"""
Draw the pieces
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))


if __name__ == "__main__":
    main()

