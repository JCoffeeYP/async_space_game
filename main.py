import curses
import os
import random
import sys
import time

import globals
from animations import animate_spaceship, blink, sleep
from constants import (NUMBER_OF_STARS, PATH_TO_GARBAGE_FRAMES,
                       PATH_TO_ROCKET_FRAMES, SPEED, STARS, TIC_TIMEOUT)
from draw_tools import close_draw, initial_prepare_canvas
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


async def fill_orbit_with_garbage(canvas, max_lenght, frames):
    length = len(frames)
    while True:
        globals.coroutines.append(
            fly_garbage(
                canvas,
                random.randint(0, max_lenght),
                frames[random.randint(0, length - 1)]
            )
        )
        await sleep(random.randint(1, 20))


def draw(canvas):
    initial_prepare_canvas(canvas)
    max_y, max_x = curses.window.getmaxyx(canvas)
    for i in range(NUMBER_OF_STARS):
        globals.coroutines.append(
            blink(
                canvas,
                random.randint(1, max_y - 2),
                random.randint(1, max_x - 2),
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
    try:
        curses.update_lines_cols()
        curses.wrapper(draw)
    except KeyboardInterrupt:
        curses.wrapper(close_draw)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
