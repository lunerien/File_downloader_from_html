"""Script searching for files in html then download missing"""

import typing
from pathlib import Path
import os
import logging
import re

import requests


def setup_custom_logger(name: str) -> None:
    """Setup cutoms logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("root_srcipt_download.log")
    file_handler.setLevel(logging.ERROR)

    channel = logging.StreamHandler()
    channel.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    channel.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(channel)
    logger.addHandler(file_handler)


def search_html_for_files(
    file: str, formats_list: typing.List
) -> typing.List[typing.Tuple[str, str]]:
    """Function searching for files url in html"""
    with open(file, "r", encoding="utf8") as file_source:
        data = file_source.read()

        formats_regex_or_string = "".join(
            [
                format + "|" if not format == formats_list[-1] else format
                for format in formats_list
            ]
        )

        files_links = re.findall(
            "(https://.*?[.](" + formats_regex_or_string + "))", data
        )

        return files_links


def main(links: typing.List[typing.Tuple[str, str]], path_directory: str):
    """Function downloading found files"""
    logger = logging.getLogger("root_srcipt_download")

    with open(path_directory + "out.txt", "w", encoding="utf8") as file_out:
        for link in links:
            directory_name = link[1]
            url = link[0]
            file_out.write(url + "\n")
            file_name = re.findall(".*/(.*)", url)[0]
            if not os.path.exists(
                path_directory + "download\\" + directory_name + "\\" + file_name
            ):
                logger.info("Downloading: %s", file_name)
                req = requests.get(url, allow_redirects=True)
                remote_file_size = str(req.headers.get("content-length", None))
                Path(path_directory + "download\\" + directory_name).mkdir(
                    parents=True, exist_ok=True
                )

                with open(
                    path_directory + "download\\" + directory_name + "\\" + file_name,
                    "wb",
                ) as file_to_write:
                    file_to_write.write(req.content)

                if os.path.exists(
                    path_directory + "download\\" + directory_name + "\\" + file_name
                ):
                    with open(
                        path_directory
                        + "download\\"
                        + directory_name
                        + "\\"
                        + file_name,
                        "rb",
                    ) as file2:
                        local_file_size = len(file2.read())
                        if int(local_file_size) == int(remote_file_size):
                            logger.debug("Download success: %s", file_name)
                        else:
                            logger.critical(
                                "Download failed: File not downloaded\
                                     completly remote_size: %s local_size: %i",
                                remote_file_size,
                                local_file_size,
                            )
                else:
                    logger.error(
                        "Download failed: file not exists: %sdownload\\%s\\%s",
                        path_directory,
                        directory_name,
                        file_name,
                    )
            else:
                logger.debug("Exists: %s", file_name)


if __name__ == "__main__":
    setup_custom_logger("root_srcipt_download")
    formats = ["pdf", "epub", "mobi", "7z", "zip", "rar", "azw3", "gz", "tar"]
    full_path = os.path.realpath(__file__)
    path, _ = os.path.split(full_path)
    path += "\\"
    links_from_html = search_html_for_files(path + "file.html", formats)
    main(links_from_html, path)
    input("end")
