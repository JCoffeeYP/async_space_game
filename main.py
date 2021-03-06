import curses
import os
import random
import sys
import time

import globals
from animations import animate_spaceship, blink, sleep
from constants import (NUMBER_OF_STARS, PATH_TO_GARBAGE_FRAMES,
                       PATH_TO_ROCKET_FRAMES, SPEED, STARS, STATUS_BAR_HEIGHT,
                       TIC_TIMEOUT)
from draw_tools import (close_draw, create_status_bar, initial_prepare_canvas,
                        status_bar_draw)
from game_scenario import get_garbage_delay_tics
# from obstacles import show_obstacles
from space_garbage import fly_garbage


def get_frames(filepath):
    frames = []
    file_names = os.listdir(f'{filepath}/.')
    for filename in file_names:
        with open(f'{filepath}/{filename}', 'r') as file:
            frame = file.read()
            frames.append(frame)
    return frames


async def time_counter():
    while True:
        end = time.time()
        if end - globals.start_time > 1.5:
            globals.YEAR += 1
            globals.start_time = end
        await sleep(1)


async def fill_orbit_with_garbage(canvas, max_lenght, frames):
    length = len(frames)
    while True:
        tic = get_garbage_delay_tics(globals.YEAR)
        if tic is not None:
            globals.coroutines.append(
                fly_garbage(
                    canvas,
                    random.randint(0, max_lenght),
                    frames[random.randint(0, length - 1)]
                )
            )
            await sleep(tic)
        else:
            await sleep(1)


def draw(canvas):
    initial_prepare_canvas(canvas)
    max_y, max_x = curses.window.getmaxyx(canvas)
    status_bar = create_status_bar(canvas)
    globals.coroutines.append(status_bar_draw(status_bar, canvas))
    for _ in range(NUMBER_OF_STARS):
        globals.coroutines.append(
            blink(
                canvas,
                random.randint(1, max_y - STATUS_BAR_HEIGHT - 1),
                random.randint(1, max_x - 1),
                random.choice(STARS)
            )
        )
    rocket_frames = get_frames(PATH_TO_ROCKET_FRAMES)
    globals.coroutines.append(
        animate_spaceship(canvas, max_y, max_x, rocket_frames, SPEED)
    )
    globals.coroutines.append(
        fill_orbit_with_garbage(
            canvas, max_x - 1, get_frames(PATH_TO_GARBAGE_FRAMES)
        )
    )
    globals.coroutines.append(time_counter())
    # globals.coroutines.append(show_obstacles(canvas, globals.obstacles))
    while True:
        for coroutine in globals.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                globals.coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(1 * TIC_TIMEOUT)
        canvas.border()


if __name__ == '__main__':
    globals.initialize()
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    try:
        curses.update_lines_cols()
        curses.wrapper(draw)
    except KeyboardInterrupt:
        curses.wrapper(close_draw)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
