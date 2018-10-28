#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os
import time
from datetime import datetime

import feedparser
# Global Variables
import pytz

TIME_FORMAT = "%Y.%m.%d-%H.%M.%S %z"
CONFIG_FILE = "./config.json"
LOG_FILE = "./temp.log"

PARSER = None

USER = None
PASS = None
IP = None
SLEEPTIMER = None
LOCAL_TIMEZONE = None

URL = None
FEED_TIMEZONE = None
FEED_TIMEZONE_CORRECT = None
ADDITIONAL_ARGUMENT = None
SHOWS = None


# TODO add proper logger
# TODO support for multiple RSS feeds
# TODO proper config reload

def load_config():
    print("[%s] Loading Config" % (time.strftime(TIME_FORMAT)))
    logging.info("[%s] Loading Config" % (time.strftime(TIME_FORMAT)))
    PARSER = json.load(open(CONFIG_FILE))

    global USER, PASS, IP, SLEEPTIMER, LOCAL_TIMEZONE, URL, ADDITIONAL_ARGUMENT, SHOWS

    USER = PARSER["username"]
    PASS = PARSER["password"]
    IP = PARSER["ip"]
    SLEEPTIMER = int(PARSER["timer"])
    LOCAL_TIMEZONE = PARSER["local_timezone"]

    URL = PARSER["url"]
    ADDITIONAL_ARGUMENT = PARSER["additional_argument"]
    SHOWS = PARSER["torrents"]


def check_releases():
    """
    Checks RSS feed for new releases and calls download() if one is found
    """
    print("[%s] Checking for new releases..." % (time.strftime(TIME_FORMAT)))
    logging.info("[%s] Checking for new releases..." % (time.strftime(TIME_FORMAT)))
    rss_feed = feedparser.parse(URL + ADDITIONAL_ARGUMENT)

    for entry in rss_feed.entries:
        for show in SHOWS:
            if show.lower() in entry.title.lower():
                entry_published = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                entry_published = pytz.utc.localize(entry_published)
                entry_published = entry_published.replace(tzinfo=pytz.timezone("CET"))

                # Check if torrent has already been downloaded
                if SHOWS[show] == "NA" or datetime.strptime(SHOWS[show], TIME_FORMAT) < entry_published:
                    # update_json(show)
                    print("[%s] Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    logging.info("[%s] Downloading %s" % (time.strftime(TIME_FORMAT), entry.title))
                    download(entry.link)
                    update_json(show)

                else:
                    print("[%s] %s already downloaded" % (time.strftime(TIME_FORMAT), entry.title))
                    logging.info("[%s] %s already downloaded" % (time.strftime(TIME_FORMAT), entry.title))


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


def main():
    load_config()
    check_releases()


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

    logging.info("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))
    print("[%s] RSSTorrentDownloader Started" % (time.strftime(TIME_FORMAT)))

    while 1:
        main()
        logging.info("[%s] Waiting %s seconds..." % (time.strftime(TIME_FORMAT), SLEEPTIMER))
        print("[%s] Waiting %s seconds..." % (time.strftime(TIME_FORMAT), SLEEPTIMER))
        time.sleep(SLEEPTIMER)
