#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__copyright__ = """
    RSSTorrentDownload - Automatically download new torrents from a RSS feed
    Copyright (C) 2018  RafaelRomon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__license__ = "GNU GPL 3"

import json
import logging
import os
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

import feedparser
import pytz

# Global Variables

TIME_FORMAT = "%Y.%m.%d-%H.%M.%S %z"
CONFIG_FILE = "./config.json"
PARSER = json.load(open(CONFIG_FILE))

LOG_FILE = PARSER["log_file"]
LOG_SIZE_LIMIT = PARSER["log_size_limit"] * 1024 * 1024  # Convert Mb to bytes
LOG_BACKUPS = PARSER["log_backups"]
USER = PARSER["username"]
PASS = PARSER["password"]
IP = PARSER["ip"]
SLEEPTIMER = int(PARSER["timer"])
LOCAL_TIMEZONE = PARSER["local_timezone"]

URL = PARSER["url"]
ADDITIONAL_ARGUMENT = PARSER["additional_argument"]
TORRENTS = PARSER["torrents"]


# TODO support for multiple RSS feeds


def reload_torrents():
    print("[%s] Reloading torrents" % (time.strftime(TIME_FORMAT)))
    logger.info("[%s] Reloading torrents" % (time.strftime(TIME_FORMAT)))

    global TORRENTS, PARSER

    PARSER = json.load(open(CONFIG_FILE))
    TORRENTS = PARSER["torrents"]


def check_releases():
    """
    Checks RSS feed for new releases and calls download() if one is found
    """
    print("[%s] Checking for new releases..." % (time.strftime(TIME_FORMAT)))
    logger.info("[%s] Checking for new releases..." % (time.strftime(TIME_FORMAT)))
    rss_feed = feedparser.parse(URL + ADDITIONAL_ARGUMENT)

    for entry in rss_feed.entries:
        for torrent in TORRENTS:
            if torrent.lower() in entry.title.lower():

                # Adding timezone and converting to local timezone
                entry_published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                entry_published = pytz.utc.localize(entry_published)
                entry_published = entry_published.replace(tzinfo=pytz.timezone(LOCAL_TIMEZONE))

                # Check if torrent has already been downloaded
                if TORRENTS[torrent] == "NA" or datetime.strptime(TORRENTS[torrent], TIME_FORMAT) < entry_published:
                    # update_json(torrent)
                    print("[%s] Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    logger.info("[%s] Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    download(entry.link)
                    update_json(torrent)

                else:
                    print("[%s] %s already downloaded" % (time.strftime(TIME_FORMAT), entry.title))
                    logger.info("[%s] %s already downloaded" % (time.strftime(TIME_FORMAT), entry.title))


def download(magnet):
    """
    Calls transmission-remote to download the specified magnet
    """
    cmd = "transmission-remote %s -n %s:%s --add '%s'" % (IP, USER, PASS, magnet)
    os.system("%s >/dev/null" % cmd)  # TODO check command response


def update_json(torrent):
    """
    Updates config with the last time the torrent was downloaded
    """
    with open(CONFIG_FILE, "r+") as f:
        data = json.load(f)
        data["torrents"][torrent] = time.strftime(TIME_FORMAT)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


if __name__ == '__main__':

    log_formatter = logging.Formatter("%(message)s")

    log_handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=LOG_SIZE_LIMIT, backupCount=LOG_BACKUPS,
                                      encoding=None, delay=0)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    logger.info("===================================================================================================")
    logger.info("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))
    print("===================================================================================================")
    print("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))

    while 1:
        reload_torrents()
        check_releases()
        logger.info("[%s] Waiting %s seconds..." % (time.strftime(TIME_FORMAT), SLEEPTIMER))
        print("[%s] Waiting %s seconds..." % (time.strftime(TIME_FORMAT), SLEEPTIMER))
        time.sleep(SLEEPTIMER)
