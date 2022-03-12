import asyncio
import curses
import random


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 20))

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 20))

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(random.randint(1, 20))

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 20))
