from datetime import datetime
import requests


def get_datetime_str():
    # Get the current datetime
    current_time = datetime.now()
    # Format the datetime string
    datetime_str = current_time.strftime("%Y%m%d_%H%M%S")
    return datetime_str


class ResourceNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


def download_file(url, filename):
    response = requests.get(url)

    # Save only if request was successful
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        raise ResourceNotFoundException(f"Failed to download file: HTTP {response.status_code}")