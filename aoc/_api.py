from typing import Union
import requests
from pathlib import Path
from datetime import datetime

_SESSION_FILE_NAME = "session.txt"
_YEAR_FILE_NAME = "year.txt"


def _set_read_file(filename: str, default: str = None) -> Union[str, None]:
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
assert SESSION is not None
SESSION = SESSION.strip()

YEAR = _set_read_file(_YEAR_FILE_NAME)
if not YEAR:
    YEAR = _set_read_file(
        _YEAR_FILE_NAME,
        str(datetime.now().year))
    assert YEAR is not None
YEAR = int(YEAR.strip())

def get_input(day: int, year: int = YEAR, overwrite: bool = False):
    """
    Usage:
    ```python
    import aoc
    data_rows = aoc.get_input(5).splitlines()
    ```python
    """

    Path("data").mkdir(exist_ok=True)

    file_name = f"data/{year}_{day}.txt"
    data = None if overwrite else _set_read_file(file_name)
    if not data:
        response = requests.get(
                f"https://adventofcode.com/{year}/day/{day}/input",
                cookies={"session": SESSION})
        if not response.ok:
            if response.status_code == 404:
                raise FileNotFoundError(response.text)
            raise RuntimeError(f"Request failed, code: {response.status_code}, message: {response.content}")
        data = _set_read_file(
            file_name,
            response.text[:-1])
    if data is None:
        raise FileNotFoundError(f"Data could not be fetched for day {day}")
    return data
