#!/usr/bin/env python3

from typing_extensions import Annotated
from urllib.error import URLError
import datetime
import logging
import os
import sys
import typer
import urllib.request
import validators


def main(
    url: Annotated[str, typer.Argument(help="URL to donwload")],
    debug: Annotated[
        bool,
        typer.Option(
            help="Enable debugging.", rich_help_panel="Customization and Utils"
        ),
    ] = False,
    metadata: Annotated[
        bool,
        typer.Option(
            help="Enable metadata logging.", rich_help_panel="Customization and Utils"
        ),
    ] = False,
):
    """
    Download provided URL and store on current directory
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    # Check URL before downloading
    logging.debug(f"Validating url")
    validate_url(url)

    # Download HTML and count <a> and <img> tags
    logging.debug(f"Starting download for {url}")
    html = download_html(url)
    logging.debug(f"Counting links and images")
    num_links = get_number_of_links(html)
    num_images = get_number_of_images(html)

    # Remove http:// https:// and set filename
    site = get_site_name(url)
    filename = f"{site}.html"
    mtime = get_modified_time(filename)

    # Write to file
    logging.debug(f"Writing to file")
    write_to_file(filename, html)

    # Output metadata to user
    if metadata:
        logging.debug(f"Logging metadata")
        print("site: " + url)
        print("num_links: " + str(num_links))
        print("images: " + str(num_images))
        print("last_fetch: " + mtime.strftime("%a %b %d %Y %H:%M UTC"))


def validate_url(url):
    if not validators.url(url):
        logging.error("Invalid URL format")
        raise typer.Exit()


def download_html(url):
    try:
        with urllib.request.urlopen(url) as f:
            return f.read().decode("utf-8")
    except Exception as e:
        logging.error(f"Cannot download from {url}")
        raise typer.Exit()


def get_site_name(url):
    return url.removeprefix("http://").removeprefix("https://")


def get_number_of_links(html):
    return html.count("<a href=")


def get_number_of_images(html):
    return html.count("<img")


def get_modified_time(filename):
    logging.debug(f"Checking modified time for downloaded file")
    if os.path.exists(filename):
        return datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    return datetime.datetime.now()


def write_to_file(filename, html):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)
    except Exception as e:
        logging.error("Cannot write to file")
        raise typer.Exit()


if __name__ == "__main__":
    typer.run(main)
