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

ENABLE_LOGGER = PARSER["enable_logger"]
LOG_FILE = PARSER["log_file"]
LOG_SIZE_LIMIT = PARSER["log_size_limit"] * 1024 * 1024  # Convert Mb to bytes
LOG_BACKUPS = PARSER["log_backups"]

USER = PARSER["username"]
PASS = PARSER["password"]
IP = PARSER["ip"]
SLEEPTIMER = int(PARSER["timer"])
LOCAL_TIMEZONE = PARSER["local_timezone"]

FEEDS = PARSER["feeds"]


# TODO support for multiple RSS feeds


def reload_feeds():
    print("[%s] Reloading torrents feeds" % (time.strftime(TIME_FORMAT)))

    global FEEDS, PARSER

    PARSER = json.load(open(CONFIG_FILE))
    FEEDS = PARSER["feeds"]


def check_releases(feed):
    """
    Checks RSS feed for new releases and calls download() if one is found
    """

    print("[%s] Checking for new Releases in %s:" % (time.strftime(TIME_FORMAT), feed))

    url = FEEDS[feed]["url"]
    additional_argument = FEEDS[feed]["additional_argument"]
    torrents = FEEDS[feed]["torrents"]

    rss_feed = feedparser.parse(url + additional_argument)

    for entry in rss_feed.entries:
        for torrent in torrents:
            if torrent.lower() in entry.title.lower():

                # Adding timezone and converting to local timezone
                entry_published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                entry_published = pytz.utc.localize(entry_published)
                entry_published = entry_published.replace(tzinfo=pytz.timezone(LOCAL_TIMEZONE))

                # Check if torrent has already been downloaded
                if torrents[torrent] == "NA" or datetime.strptime(torrents[torrent], TIME_FORMAT) < entry_published:
                    print("[%s] - Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    log("[%s] - Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    download(entry.link)
                    update_json(feed, torrent)


def download(magnet):
    """
    Calls transmission-remote to download the specified magnet
    """
    cmd = "transmission-remote %s -n %s:%s --add '%s'" % (IP, USER, PASS, magnet)
    os.system("%s >/dev/null" % cmd)  # TODO check command response


def update_json(feed, torrent):
    """
    Updates config with the last time the torrent was downloaded
    """
    with open(CONFIG_FILE, "r+") as f:
        data = json.load(f)
        data["feeds"][feed]["torrents"][torrent] = time.strftime(TIME_FORMAT)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def log(string):
    if ENABLE_LOGGER:
        logger.info(string)


if __name__ == '__main__':

    if ENABLE_LOGGER:
        log_formatter = logging.Formatter("%(message)s")

        log_handler = RotatingFileHandler(LOG_FILE, mode='a', maxBytes=LOG_SIZE_LIMIT, backupCount=LOG_BACKUPS,
                                          encoding=None, delay=0)
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(logging.INFO)

        logger = logging.getLogger('root')
        logger.setLevel(logging.INFO)
        logger.addHandler(log_handler)

    log("===================================================================================================")
    log("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))
    print("===================================================================================================")
    print("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))

    while 1:

        reload_feeds()

        # Calls check_releases() for every feed in FEEDS
        for feed in FEEDS:
            check_releases(feed)

        print("[%s] Waiting %s seconds..." % (time.strftime(TIME_FORMAT), SLEEPTIMER))
        time.sleep(SLEEPTIMER)
