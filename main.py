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
import pyautogui  # for mouse clicking

from time import *
import datetime

###########################################################################################################################
"This Python file opens a browser (Firefox) page to chess.com's puzzle rush page, logs in and solves puzzles"

# defining a few variables that'll be needed thereafter

with open("credentials.txt") as f:
    content = f.readlines()
creds = [line.strip() for line in content if not "#" in line]
email, password = creds[0], creds[1]

with chess.engine.SimpleEngine.popen_uci(
    "stockfish_13_win_x64_avx2"
) as engine:  # initiating a chess engine (Stockfish 13)
    try:
        driver = webdriver.Firefox()
        driver.get("https://www.chess.com/login")
        driver.maximize_window()
        driver.fullscreen_window()  # this is like pressing the shortcut key F11
        username = driver.find_element_by_id("username")
        username.click()
        username.send_keys(email)
        pwd = driver.find_element_by_id("password")
        pwd.click()
        pwd.send_keys(password)
        log = driver.find_element_by_id("login")
        log.click()
        sleep(1)
        banner = driver.find_elements_by_class_name("icon-font-chess x")
        for cross in banner:
            cross.click()
        driver.get("https://www.chess.com/puzzles/rush")
        sleep(1)
        # now a few precautions to remove potential annoying banners or pop-ups:
        annoying_banner = driver.find_elements_by_class_name("icon-font-chess x")
        for item in annoying_banner:
            try:
                item.click()
            except:
                pass
        try:
            bg = driver.find_elements_by_class_name("core-modal-background")
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
            a = driver.find_elements_by_class_name(
                "icon-font-chess x ui_outside-close-icon"
            )
            for item in a:
                try:
                    item.click()
                except:
                    continue
        except:
            pass
        try:
            a = driver.find_elements_by_class_name("icon-font-chess x")
            for item in a:
                try:
                    item.click()
                except:
                    continue
        except:
            pass
        try:
            a = driver.find_elements_by_class_name("core-modal-background")
            for item in a:
                try:
                    a.click()
                except:
                    continue
        except:
            pass
        sleep(5)  # this leaves time for a human to click potential banners
        play_button = driver.find_element_by_class_name(
            "ui_v5-button-component.ui_v5-button-primary.ui_v5-button-large.ui_v5-button-full"
        )
        play_button.click()
        time_start = time()
        sleep(
            4
        )  # wait for the 3 countdown seconds + time for the first move being played
        try:
            a = driver.find_element_by_class_name("wrapper svelte-362hqn")
            a.click()
            print("removed the cookies banner successfully")
        except:
            pass

        ########## DONE SETTING UP EVERYTHING, NOW THE PUZZLE RUSH BEGINS ###################
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        time_now = time()
        time_elapsed = time_now - time_start
        nbpuzzles = 0
        while (
            time_elapsed < 305
        ):  # puzzle rush lasts 5 min so I took just beyond 5min*60sec. A cleaner, more robust way to loop would be to parse the HTML and detect the end of the rush
            timebegin = time()
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "board-board")))
            if (
                len(
                    soup.find_all(
                        class_="streak-indicator-streak streak-indicator-incorrect streak-indicator-link"
                    )
                )
                + len(
                    soup.find_all(
                        class_="streak-indicator-streak streak-indicator-correct streak-indicator-link"
                    )
                )
                > nbpuzzles
            ):
                nbpuzzles += 1
                print("NEW PUZZLE")

            html = driver.page_source
            print("Took", time() - timebegin, " to get html")
            timebegin = time()
            soup = BeautifulSoup(html, "html.parser")
            print("Took", time() - timebegin, " to parse html")

            timebegin = time()

            board_desc = get_chessdotcom_board_desc(soup)
            print("Took", time() - timebegin, " to get boarddesc")

            # print('Got board desc', board_desc)
            timebegin = time()

            fen = chessdotcom_board_to_fen(board_desc, soup)
            print("Took", time() - timebegin, " to make the FEN: ", fen)

            timebegin = time()

            # print(f'Current fen is: {fen}')
            best_move = str(engine_best_move(engine, fen))
            print("Took", time() - timebegin, " to get the best move\n")

            # print(f'Best move is {best_move}')
            best_move_start_square = squares_dict[best_move[:4][:2]][-2:]
            best_move_destination_square = squares_dict[best_move[:4][2:]][-2:]
            if is_black_turn(
                soup
            ):  # board is flipped, so I need to adapt the coordinates that I pass to pyautogui.click()
                best_move_start_square = str(9 - int(best_move_start_square[0])) + str(
                    9 - int(best_move_start_square[1])
                )
                best_move_destination_square = str(
                    9 - int(best_move_destination_square[0])
                ) + str(9 - int(best_move_destination_square[1]))
            pyautogui.click(
                262 + 130 * (int(best_move_start_square[0]) - 1),
                87 + 130 * 8 - 130 * (int(best_move_start_square[1])),
            )
            pyautogui.click(
                262 + 130 * (int(best_move_destination_square[0]) - 1),
                87 + 130 * 8 - 130 * (int(best_move_destination_square[1])),
            )
            if (
                len(best_move) > 4
            ):  # meaning the move is a promotion and thus ends with a piece symbol (ex: "d7d8q"). Thus I need to click on queen (I don't consider underpromotion yet)
                pyautogui.click(
                    262 + 130 * (int(best_move_destination_square[0]) - 1),
                    87 + 130 * 8 - 130 * (int(best_move_destination_square[1])),
                )
            sleep(
                1
            )  # this one is crucial to avoid the error "engine process died unexpectedly (exit code: 3221225477)"
            time_now = time()
            time_elapsed = time_now - time_start
    except Exception as e:
        print(f"Error encountered: {e}")
        driver.quit()

sleep(5)
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
screenshot_name = f"scores_screenshots/{now}.png"
driver.save_screenshot(screenshot_name)
driver.quit()
