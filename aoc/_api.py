import requests
from pathlib import Path
from datetime import datetime

_SESSION_FILE_NAME = "session.txt"
_YEAR_FILE_NAME = "year.txt"


def _set_read_file(filename: str, default: str = None) -> str:
    try:
        with open(filename) as file:
            return file.read()
    except FileNotFoundError:
        if default:
            with open(filename, "w") as file:
                file.write(default)
                return default
        return None


SESSION = _set_read_file(_SESSION_FILE_NAME)
if not SESSION:
    SESSION = _set_read_file(
        _SESSION_FILE_NAME,
        input("Enter your session cookie: "))

YEAR = _set_read_file(_YEAR_FILE_NAME)
if not YEAR:
    YEAR = _set_read_file(
        _YEAR_FILE_NAME,
        str(datetime.now().year))


def get_input(day: int, year: int = YEAR):
    Path("data").mkdir(exist_ok=True)

    file_name = f"data/{year}_{day}.txt"
    data = _set_read_file(file_name)
    if not data:
        data = _set_read_file(
            file_name,
            requests.get(
                f"https://adventofcode.com/{year}/day/{day}/input",
                cookies={"session": SESSION}).text[:-1])
    return data
