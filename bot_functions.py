import chess
import chess.engine


def get_squares_dict():
    '''Creates a dictionary where the conversion is made between Stockfish square notation and chessdotcom HTML square notation'''
    squares_dict = {}
    columns = ['a','b','c','d','e','f','g','h']
    for row in range(1,9):
        for letter in columns:
            squares_dict[letter + str(row)] = 'square-' + str(columns.index(letter)+1) + str(row)
    return squares_dict

squares_dict = get_squares_dict()

def chessdotcom_board_to_fen(board_desc):
    '''Receives a chess board description as is currently (May 2021) used by chess.com in the puzzle rush page HTML, 
    and processes it to return a FEN of the position'''
    board = chess.Board().clear_board()
    for square, piece in board_desc.items():
        board.set_piece_at(square, piece)
    return board.fen()
   


def engine_best_move(engine, fen : str, time = 0.01) -> str:
    '''input: a FEN / output: the best move in the position according to Stockfish 13's neural network under the given time constraint (in ms)'''
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=time))
    return info["pv"][0]