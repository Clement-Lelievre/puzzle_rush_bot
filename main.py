# chess board processing related imports
from bot_functions import *

# chess engine - related imports
import chess
import chess.engine

# browser related imports

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from time import *
import datetime

###########################################################################################################################
"This Python file opens a browser (Firefox) page to chess.com's puzzle rush page, logs in and plays the game."

# defining a few variables that'll be needed thereafter
email = 'zeiejkejezezez@gmail.com'
password = 'akjankajna' # TO DO: make it hidden

with chess.engine.SimpleEngine.popen_uci("stockfish_13_win_x64_avx2") as engine:  # initiating a chess engine (Stockfish 13)
    try:
        driver = webdriver.Firefox() 
        driver.get("https://www.chess.com/login")
        driver.maximize_window()
        driver.fullscreen_window() #this is like pressing the shortcut key F11
        username = driver.find_element_by_id('username')
        username.click()
        username.send_keys(email)
        pwd = driver.find_element_by_id('password')
        pwd.click()
        pwd.send_keys(password)
        log = driver.find_element_by_id('login')
        log.click()
        sleep(2)
        banner = driver.find_elements_by_class_name("icon-font-chess x")
        for cross in banner:
            cross.click()
        driver.get("https://www.chess.com/puzzles/rush")
        sleep(3)
        annoying_banner = driver.find_elements_by_class_name('icon-font-chess x')
        for item in annoying_banner:
            try:
                item.click() 
            except:
                continue
        try:
            bg = driver.find_element_by_class_name('core-modal-background')
            bg.click()
        except:
            pass
        try:
            a = driver.find_element_by_partial_link_text("Sauter l'essai")
            a.click()
        except:
            pass
        play_button = driver.find_element_by_class_name('ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full')
        play_button.click()
        sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        chesscom_board_desc = []
        for item in soup.find_all(id='board-board'):
            for stuff in item.find_all('div'):
                chesscom_board_desc.append(stuff['class'])
        print(chesscom_board_desc)
        
        # fen = chessdotcom_board_to_fen(board_desc)
        #best_move = engine_best_move(engine, fen)
        # best_move_start_square = best_move[:2]
        # best_move_destination_square = best_move[2:]

        # driver.save_screenshot(screenshot_name)
        # now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # screenshot_name = f'scores_screenshots/{now}.png'
        
    except Exception as e:
        print(e)



#driver.quit()

