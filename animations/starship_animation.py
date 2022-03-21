import asyncio
import curses
from itertools import cycle

import globals
from animations.fire_animation import fire
from constants import STATUS_BAR_HEIGHT
from curses_tools import draw_frame, get_frame_size, read_controls
from draw_tools import show_gameover
from explosion import explode
from obstacles import Obstacle
from physics import update_speed


async def animate_spaceship(canvas, max_y, max_x, frames, speed=1):
    row = int(max_y / 2)
    column = int(max_x / 2)
    row_speed = 0
    column_speed = 0
    box = Obstacle(row, column)

    while True:
        for frame in cycle(frames):
            draw_frame(canvas, row, column, frame)
            size = get_frame_size(frame)
            box.rows_size = size[0]
            box.columns_size = size[1]
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)
            rows_direction, columns_direction, space_pressed = (
                read_controls(canvas)
            )
            row_speed, column_speed = update_speed(
                row_speed, column_speed, rows_direction, columns_direction
            )
            row += row_speed
            column += column_speed
            if row < 1:
                row = 1
            elif row > max_y - size[0] - STATUS_BAR_HEIGHT:
                row = max_y - size[0] - STATUS_BAR_HEIGHT
            if column < 1:
                column = 1
            elif column > max_x - 1 - size[1]:
                column = max_x - 1 - size[1]
            box.row = row
            box.column = column
            if space_pressed and globals.YEAR >= 1969:
                globals.coroutines.append(fire(canvas, row, column + size[1] // 2))
            for obs in globals.obstacles:
                if box.has_collision(obs.row, obs.column, obs.rows_size, obs.columns_size):
                    await explode(canvas, row + size[0] // 2, column + size[1] // 2)
                    if globals.LIFE > 1:
                        globals.obstacles_in_last_collisions.append(obs)
                        globals.LIFE -= 1
                    else:
                        curses.wrapper(show_gameover)
