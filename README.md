# URL HTML Downloader

This Python script downloads the HTML content of a given URL, counts the number of `<a>` (links) and `<img>` (images) tags, and saves the HTML file to your current working directory. It also logs the number of links and images, and displays the last time the file was fetched.

## Features

- Downloads HTML content from a given URL.
- Counts the number of links (`<a>` tags) and images (`<img>` tags).
- Saves the HTML to a file
- Displays the last modification time of the HTML file (if it was previously downloaded).
- Error handling for invalid URLs and download issues.

## Requirements

- Python 3.7+

Install dependencies with:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

You can run the script from the command line as follows:

```bash
# Help page
python main.py --help

python main.py <URL>
python main.py --metadata --debug <URL>
```

## Test

Unit test can be run from the command line as follows:

```bash
python -m unittest
```

## Running using Docker

```bash
docker build -t url-downloader .
docker run url-downloader python main.py --debug --metadata https://google.com
docker cp $conatiner_id:/app/google.com.html .
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
