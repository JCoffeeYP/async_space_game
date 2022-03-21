import curses
import os
import sys
import time

import globals
from animations.blink_animation import sleep
from constants import HEART, STATUS_BAR_HEIGHT
from curses_tools import draw_frame, get_frame_size
from game_scenario import PHRASES


def initial_prepare_canvas(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)


def create_status_bar(canvas):
    max_y, max_x = curses.window.getmaxyx(canvas)
    return canvas.derwin(STATUS_BAR_HEIGHT, max_x, max_y - STATUS_BAR_HEIGHT, 0)


async def status_bar_refresh(status_bar, canvas):
    status_bar.border()
    _, max_x = curses.window.getmaxyx(status_bar)
    score = f'SCORE: {globals.destroyed_obstacles}'
    year = f'YEAR: {globals.YEAR}'
    if globals.YEAR in PHRASES:
        year += f' - {PHRASES[globals.YEAR]}'
    life = f'LIFE: {(HEART + " ") * globals.LIFE}'
    indicators = f'{score}     {life}     {year}'
    whitespace = (max_x - len(indicators) - 2) * ' '
    status_bar.addstr(1, 1, f'{indicators}{whitespace}', curses.A_BOLD)
    status_bar.overlay(canvas)
    status_bar.refresh()


async def status_bar_draw(status_bar, canvas):
    while True:
        globals.coroutines.append(status_bar_refresh(status_bar, canvas))
        await sleep(1)


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
            canvas, row, round(max_x / 2) - size[1] // 2, good_bye_frame, color=3
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
    draw_frame(canvas, row, round(max_x / 2) - size[1] // 2, good_bye_frame, color=3)
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
            canvas, row, round(max_x / 2) - size[1] // 2, game_over_frame, color=3
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
    draw_frame(canvas, row, round(max_x / 2) - size[1] // 2, game_over_frame, color=3)
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
