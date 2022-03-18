import time


def initialize():
    global coroutines
    global obstacles
    global obstacles_in_last_collisions
    global obstacle_beat_spaceship
    global destroyed_obstacles
    global YEAR
    global LIFE
    global start_time
    coroutines = []
    obstacles = []
    obstacles_in_last_collisions = []
    destroyed_obstacles = 0
    obstacle_beat_spaceship = False
    YEAR = 1957
    LIFE = 3
    start_time = time.time()
