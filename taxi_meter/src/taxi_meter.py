"""Taxi Meter

This is the main module of taxi meter that simulates the behavior of Taxi
Meter. 
"""

import time
import os

from pynput import keyboard

from utils import get_time_format, get_distance_format, get_fare
from constants import (
    START_RIDE_MSG,
    WAITING_STATE,
    WAITING,
    DRIVING,
    SPEED_UNIT,
    RIDE_TIME,
    SPEED,
    WAIT_TIME,
    FARE,
    DISTANCE,
    FARE_UNIT,
)


def initialize_perameters():
    global start_time
    global ride_time
    global current_time
    global waiting_time
    global current_wait
    global total_distance
    global status
    global speed

    start_time = time.time()
    ride_time = 0
    current_time = 0
    waiting_time = 0
    current_wait = 0
    total_distance = 0
    status = DRIVING
    print(START_RIDE_MSG)
    speed = 0


def end_ride():
    """This function ends the ride. It also calculates the fare and vilocity
    and display the result of the ride.
    """
    global ride_time
    global total_distance
    print(
        f"{RIDE_TIME} {get_time_format(ride_time)}\n"
        f"{DISTANCE} {get_distance_format(total_distance)}\n"
        f"{SPEED} {round(total_distance / ride_time, 2)} "
        f"{SPEED_UNIT}\n"
        f"{FARE} {get_fare(total_distance, waiting_time)}{FARE_UNIT}\n"
        f"{WAIT_TIME} {get_time_format(waiting_time)}\n"
    )


def on_press(key):
    """This functions is called when any key is pressed from the keyboard.
    There are five keys thar are handled in this function Up arrow key, Down
    arrow key and alphnumeric(P/p, R/r, E/e). All other keys are passed.
    """

    os.system("clear")
    global ride_time
    global current_time
    global waiting_time
    global current_wait
    global total_distance
    global status
    global speed

    if status == DRIVING:
        current_time = time.time() - current_time
        total_distance = total_distance + (speed * current_time)
        current_time = time.time()

    try:
        if key == keyboard.Key.up and status == DRIVING:
            speed = speed + 1
        elif key == keyboard.Key.down and status == DRIVING and speed > 0:
            speed = speed - 1
        elif (key.char == "p" or key.char == "P") and status != WAITING:
            current_wait = time.time()
            status = WAITING
        elif (key.char == "r" or key.char == "R") and status == WAITING:
            waiting_time = waiting_time + (time.time() - current_wait)
            current_wait = 0
            status = DRIVING
            current_time = time.time()
        elif key.char == "e" or key.char == "E":
            ride_time = (time.time() - start_time) - waiting_time
            end_ride()
            return False
    except AttributeError:
        pass
    if status == WAITING:
        print(WAITING_STATE)
    else:
        print(f"Current speed is {speed} {SPEED_UNIT}")


def start_ride():
    """Collect Events until Released

    This is a keyboard listener of threading.Thread, and all callbacks will be
    invoked from the thread. Return False from a callback to stop the listener.
    """

    initialize_perameters()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
