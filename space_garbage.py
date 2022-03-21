import asyncio

import globals
from curses_tools import draw_frame, get_frame_size
from explosion import explode
from obstacles import Obstacle


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """
    Animate garbage, flying from top to bottom.
    Сolumn position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1
    rows_number -= 1

    size = get_frame_size(garbage_frame)
    box = Obstacle(row, column, size[0], size[1])
    globals.obstacles.append(box)

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame, color=3)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        box.row = row
        if box in globals.obstacles_in_last_collisions:
            globals.obstacles.remove(box)
            globals.obstacles_in_last_collisions.remove(box)
            await explode(canvas, row + size[0] // 2, column + size[1] // 2)
            globals.destroyed_obstacles += 1
            return
    box.row += 1
    globals.obstacles.remove(box)
