"""Common functions"""

import time


def get_time_format(seconds):
    """return seconds in Hours, Minutes and Seconds as a String
    
    This function receives the time in seconds and returns in hours, minutes
    and seconds as a string if they are available.
    """

    total_time = time.strftime("%H:%M:%S", time.gmtime(seconds)).split(':')
    time_format = ''
    if int(total_time[0]) > 0:
        time_format = time_format + str(int(total_time[0])) + " Hours "
    if int(total_time[1]) > 0:
        time_format = time_format + str(int(total_time[1])) + " Minutes "
    if int(total_time[2]) > 0 or seconds == 0:
        time_format = time_format + str(int(total_time[2])) + " Seconds "
    return time_format


def get_distance_format(meters):
    """Display distance in KM and Meter if meter is greater than 1000"""

    distance_format = ''
    kilo_meters = int(meters / 1000)
    if kilo_meters > 0:
        distance_format = distance_format + str(kilo_meters) + " KM "
    if meters % 1000 > 0 or meters == 0:
        distance_format = (distance_format
                           + str(int(meters % 1000)) + " Meters ")
    return distance_format


def get_fare(distance_in_meters, waiting_time):
    """Calculate fare in $

    1 km Ride = 2$
    1 Minutes wait = 1$
    """

    distance_in_km = distance_in_meters / 1000
    minutes = waiting_time / 60
    return round((distance_in_km * 2) + minutes, 2)


