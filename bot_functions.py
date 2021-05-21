import chess
import chess.engine

color_dict = {'w':True, 'b':False}
type_dict = {'p':1,'n':2,'b':3,'r':4,'q':5,'k':6}

def get_squares_dict():
    '''Creates a dictionary where the conversion is made between Stockfish square notation and chessdotcom HTML square notation'''
    squares_dict = {}
    columns = ['a','b','c','d','e','f','g','h']
    for row in range(1,9):
        for letter in columns:
            squares_dict[letter + str(row)] = 'square-' + str(columns.index(letter)+1) + str(row)
    l = list(squares_dict.values())
    return squares_dict, l

squares_dict, l = get_squares_dict()

def get_chessdotcom_board_desc(soup):
    '''Scrapes the HTML content of the puzzle rush current page, and returns the board position (which pieces on which squares)'''
    def fill_pieces(stuff):
        return stuff['class'][1:]
    
    chesscom_board_desc = list(map(fill_pieces , [stuff for item in soup.find_all(id='board-board') for stuff in item.find_all('div')] ))
    chesscom_board_desc = [item for item in chesscom_board_desc if len(item) == 2] # for some reason it won't let me do a one-liner list comprehension
    # the len() thing is because the highlighted squares from the last move appear even without pieces on it, so I need to remove them
    
    #chesscom_board_desc = []
    # for item in soup.find_all(id='board-board'):
    #     for stuff in item.find_all('div'):
    #         chesscom_board_desc.append(stuff['class'][1:])
    for item in chesscom_board_desc:
        try:
            if 'square' in item[1]:
                item.reverse() # this is performed in place (even on copies)
        except:
            continue
    return chesscom_board_desc 

def is_black_turn(soup):
    try:
        return not not list(soup.find(class_ = 'board flipped'))
    except:
        return False

def chessdotcom_board_to_fen(board_desc, soup):
    '''Receives a chess board description as is currently (May 2021) used by chess.com in the puzzle rush page HTML, 
    and processes it to setup the position on Stockfish'''
    board = chess.Board(fen=None) # creating an empty board
    for item in board_desc:
        piece = chess.Piece(type_dict[item[1][1]], color_dict[item[1][0]])
        board.set_piece_at(l.index(item[0]) , piece)
    if is_black_turn(soup): # determines the side to move by looking at presence or not of "flipped board"
        board.turn = False
    else:
        board.turn = True
    return board.fen()
   
def engine_best_move(engine, fen, time = 0.1):
    '''input: a FEN / output: the best move in the position according to Stockfish 13's neural network under the given time constraint (in ms)'''
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=time))
    return info["pv"][0]



