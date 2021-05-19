# puzzle_rush_bot
A bot coded in python that plays puzzle rush on chess.com.

OS: Windows 10
File launched via Powershell.

It uses the firefox driver for Selenium (this requires to add Geckodriver to PATH) and the stockfish engine (in the same directory as the main Python file).
Warning you may have to disable manually the cookies-related banner at the bottom of the page; moreover disable the squares highlighting and legal moves highlighting (else, parsing the HTML may fail.) 

The program does not account yet for underpromotions, castling or en passant rights but can still solve most puzzles. Therefore, you should manually tick autopromotion to queen in the settings.
