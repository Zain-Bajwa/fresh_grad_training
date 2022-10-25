"""Main file of Taxi Meter"""

import os

from taxi_meter import start_ride
from constants import HOME_MSG


def main():
    """Main Function"""

    os.system('clear')
    print(HOME_MSG)
    input("Press Enter to start ride...")
    os.system('clear')
    start_ride()


if __name__ == "__main__":
    main()
