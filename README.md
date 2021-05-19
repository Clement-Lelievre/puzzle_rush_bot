# My puzzle-rush bot
![](https://github.com/Clement-Lelievre/puzzle_rush_bot/blob/main/scores_screenshots/2021-05-19_12-56-23.png)   

A bot coded in Python that plays puzzle rush on chess.com.

It performs the following actions:
-opens a browser (Firefox)
-visits chess.com, removes annoying banners then logs in (you need your own credentials)
-visits the puzzle rush page and clicks "Play"
-cracks puzzles one after the other* (sometimes it might fail a problem)
-once the 5 minutes countdown elapsed or if game aborted due 3 failures, takes a screenshot of its score and saves it locally in the appropriate folder

*Here is how it proceeds:
It loops over the following workflow:
-parses the HTML in order to get which pieces are on which squares (it disregards castling and en passant rights at this stage; I might add this later) => selenium
-processes that information (make a FEN) to convert it to Stockfish lingo => ad hoc functions
-passes the position FEN description to the Stockfish neural network, which in turn provides its best move => python-chess and ad hoc functions
-this best move is defined as a start and end square, hence pyautogui is used to click on these in order to actually complete the move
-repeats till game is over


There is still much room for improvement as this is only a first version.

OS: Windows 10
Launched via Powershell.

It uses:
- the firefox driver for Selenium (this requires to add Geckodriver to PATH) 
- the stockfish engine executable (to be placed in the same directory as the main Python file)

Warnings: 
- you may have to disable manually the cookies-related banner at the bottom of the page else clicks due to happen on the first rank will fail; moreover disable the squares highlighting and legal moves highlighting (else, parsing the HTML may fail.). Leave the coordinates inside board and set animation type to FAST.

- The program does not account yet for underpromotions, castling or en passant rights but can still solve most puzzles. 

- some of the clicks are not robust: while clicking on "Log in" and "Play" buttons is done via selenium (so, it is robust in the sense that it uses the HTML), clicking on the squares while making a move is done via pyautogui, because playing the move by clicking via selenium was too inconvenient.
Hence, this program is calibrated for a specific screen size (1920,1080). If your screen size is different, you need to adapt the coordinates of the points that are clicked (the squares) in main.py

- you cannot try accelerating the program by reducing the time.sleep() as this will induce "engine process died unexpectedly (exit code: 3221225477)"

Please use this program responsibly and respect chess.com terms of use.
