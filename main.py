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
import pyautogui # for mouse clicking

from time import *
import datetime

###########################################################################################################################
"This Python file opens a browser (Firefox) page to chess.com's puzzle rush page, logs in and solves puzzles"

# defining a few variables that'll be needed thereafter
email = 'kjdnkjfnsjsdnjkjddds685454@gmail.com'
password = 'dfkjhfkjfdhfddfkjfdkjf646845' # TO DO: make it hidden

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
        sleep(1)
        banner = driver.find_elements_by_class_name("icon-font-chess x")
        for cross in banner:
            cross.click()
        driver.get("https://www.chess.com/puzzles/rush")
        sleep(1)
        # now a few precautions to remove potential annoying banners or pop-ups:
        annoying_banner = driver.find_elements_by_class_name('icon-font-chess x')
        for item in annoying_banner:
            try:
                item.click() 
            except:
                pass
        try:
            bg = driver.find_elements_by_class_name('core-modal-background')
            for item in bg:
                try:
                    item.click()
                except:
                    continue
        except:
            pass
        try:
            a = driver.find_element_by_partial_link_text("Sauter l'essai")
            a.click()
        except:
            pass
        try:
            a = driver.find_elements_by_class_name('icon-font-chess x ui_outside-close-icon')
            for item in a:
                try:
                    item.click()
                except:
                    continue
        except:
            pass
        try:
            a = driver.find_elements_by_class_name('icon-font-chess x')
            for item in a:
                try:
                    item.click()
                except:
                    continue
        except:
            pass
        try:
            a = driver.find_elements_by_class_name('core-modal-background')
            for item in a:
                try:
                    a.click()
                except:
                    continue
        except:
            pass
        play_button = driver.find_element_by_class_name('ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full')
        play_button.click()
        sleep(5)    # wait for the 3 countdown seconds + time for the first move being played
        try:
            a = driver.find_element_by_class_name('wrapper svelte-362hqn')
            a.click()
            print('removed the cookies banner successfully')
        except:
            pass

        ########## DONE SETTING UP EVERYTHING, NOW THE PUZZLE RUSH BEGINS ###################
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            board_desc, raw_content = get_chessdotcom_board_desc(soup)
            #print('Got board desc', board_desc)
            fen = chessdotcom_board_to_fen(board_desc, soup)
            #print(f'Current fen is: {fen}')
            best_move = str(engine_best_move(engine, fen))

            #print(f'Best move is {best_move}')
            
            best_move_start_square = squares_dict[best_move[:4][:2]][-2:]
            best_move_destination_square = squares_dict[best_move[:4][2:]][-2:]
            if is_black_turn(soup): # board is flipped, so I need to adapt the coordinates that I pass to pyautogui.click()
                best_move_start_square = str( 9 - int(best_move_start_square[0])) + str( 9 - int(best_move_start_square[1]))
                best_move_destination_square = str( 9 - int(best_move_destination_square[0])) + str( 9 - int(best_move_destination_square[1]))

            pyautogui.click( 262 + 130*(int(best_move_start_square[0])-1) , 87 + 130*8 - 130*(int(best_move_start_square[1])) )
            pyautogui.click( 262 + 130*(int(best_move_destination_square[0])-1) , 87 + 130*8 - 130*(int(best_move_destination_square[1])) )
            if len(best_move) > 4 :
                pyautogui.click( 262 + 130*(int(best_move_destination_square[0])-1) , 87 + 130*8 - 130*(int(best_move_destination_square[1])) )
            sleep(1)
            #print('\nraw content is',raw_content)

            # for item in raw_content:
            #     if best_move_start_square in item:
            #         startsquare = driver.find_element_by_class_name(item.replace(' ','.'))
            #         startsquare.click()
            #         break
                
            

            # print('destination square is', best_move_destination_square)
            # for item in raw_content:
            #     if best_move_destination_square in item:
            #         print(item)
            #         try:
            #             endsquare = driver.find_element_by_class_name('hint ' + best_move_destination_square)
            #             endsquare.click()
            #             break
            #         except:
            #             pass
            # for item in raw_content:
            #     if best_move_destination_square in item:
            #         try:
            #             endsquare = driver.find_element_by_class_name('capture-hint ' + best_move_destination_square)
            #             endsquare.click()
            #             break
            #         except:
            #             pass
            # for item in raw_content:
            #     if best_move_destination_square in item:
            #         try:
            #             endsquare = driver.find_element_by_class_name(item.replace(' ','.'))
            #             endsquare.click()
            #             break
            #         except:
            #             pass
    except Exception as e:
        print(f'Error encountered: {e}')

sleep(15)
now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
screenshot_name = f'scores_screenshots/{now}.png'
driver.save_screenshot(screenshot_name)
#driver.quit()

