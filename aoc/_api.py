import requests
from pathlib import Path
from datetime import datetime

_SESSION_FILE_NAME = "session.txt"
_YEAR_FILE_NAME = "year.txt"

try:
    with open(_SESSION_FILE_NAME) as file:
        SESSION = file.readline().strip()
except FileNotFoundError:
    with open(_SESSION_FILE_NAME, "w") as file:
        SESSION = input("Enter your session cookie: ")
        file.write(SESSION)

try:
    with open(_YEAR_FILE_NAME) as file:
        YEAR = file.readline().strip()
except FileNotFoundError:
    with open(_YEAR_FILE_NAME, "w") as file:
        YEAR = datetime.now().year
        file.write(str(YEAR))


def get_input(day: int, year: int = YEAR):
    Path("data").mkdir(exist_ok=True)

    file_name = f"data/{year}_{day}.txt"
    try:
        with open(file_name) as file:
            return file.read()
    except FileNotFoundError:
        with open(file_name, "w") as file:
            data = requests.get(
                f"https://adventofcode.com/{year}/day/{day}/input",
                cookies={"session": SESSION}
            ).text[:-1]
            file.write(data)
            return data


def set_year(year: int):
    with open(_YEAR_FILE_NAME, "w") as file:
        file.write(str(year))
