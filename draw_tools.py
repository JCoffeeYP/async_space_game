import curses
import os
import sys
import time

import globals
from curses_tools import draw_frame, get_frame_size


def initial_prepare_canvas(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)


def close_draw(canvas):
    canvas.clear()
    initial_prepare_canvas(canvas)
    max_y, max_x = curses.window.getmaxyx(canvas)
    with open('frame_source/good_bye.txt', 'r') as file:
        good_bye_frame = file.read()
    size = get_frame_size(good_bye_frame)
    row = max_y
    while row > round(max_y / 2) - size[0] // 2:
        draw_frame(
            canvas, row, round(max_x / 2) - size[1] // 2, good_bye_frame
        )
        canvas.border()
        canvas.refresh()
        time.sleep(0.15)
        draw_frame(
            canvas, row, round(max_x / 2) - size[1] // 2, good_bye_frame, negative=True
        )
        row -= 1
        if row + size[0] + 1 == max_y:
            canvas.border()
    phrase = f'YOU HAVE DESTROYED {globals.destroyed_obstacles} SPACE TRASH'
    draw_frame(canvas, row, round(max_x / 2) - size[1] // 2, good_bye_frame)
    canvas.addstr(
        round(max_y / 2) + size[0], round(max_x / 2) - len(phrase) // 2, phrase, curses.A_DIM
    )
    canvas.refresh()
    time.sleep(3)


def show_gameover(canvas):
    canvas.clear()
    initial_prepare_canvas(canvas)
    max_y, max_x = curses.window.getmaxyx(canvas)
    with open('frame_source/game_over.txt', 'r') as file:
        game_over_frame = file.read()
    size = get_frame_size(game_over_frame)
    row = max_y
    while row > round(max_y / 2) - size[0] // 2:
        draw_frame(
            canvas, row, round(max_x / 2) - size[1] // 2, game_over_frame
        )
        canvas.border()
        canvas.refresh()
        time.sleep(0.15)
        draw_frame(
            canvas, row, round(max_x / 2) - size[1] // 2, game_over_frame, negative=True
        )
        row -= 1
        if row + size[0] + 1 == max_y:
            canvas.border()
    phrase = f'YOU HAVE DESTROYED {globals.destroyed_obstacles} SPACE TRASH'
    draw_frame(canvas, row, round(max_x / 2) - size[1] // 2, game_over_frame)
    canvas.addstr(
        round(max_y / 2) + size[0], round(max_x / 2) - len(phrase) // 2, phrase, curses.A_DIM
    )
    canvas.refresh()
    time.sleep(3)
    curses.endwin()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
