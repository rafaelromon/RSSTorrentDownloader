#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time

import feedparser

CONFIG_FILE = "./config.json"
PARSER = json.load(open('config.json'))

USER = PARSER["username"]
PASS = PARSER["password"]
IP = PARSER["ip"]
SLEEPTIMER = int(PARSER["timer"])

URL = PARSER["url"]
ADDITIONAL_ARGUMENT = PARSER["additional_argument"]
SHOWS = PARSER["torrents"]


# TODO add logger

def check_releases():
    """
    Checks RSS feed for new releases and calls download() if one is found
    """
    print("[%s] Checking for new releases..." % (time.strftime("%Y.%m.%d-%H.%M.%S")))
    rss_feed = feedparser.parse(URL + ADDITIONAL_ARGUMENT)

    for entry in rss_feed.entries:
        for show in SHOWS:
            if show.lower() in entry.title.lower():
                # Check if torrent has already been downloaded
                if SHOWS[show] == "NA" or time.strptime(SHOWS[show], "%Y.%m.%d-%H.%M.%S") < entry.published_parsed:
                    update_json(show)
                    print("[%s] Downloading %s" % (time.strftime("%Y.%m.%d-%H.%M.%S"), entry.title))
                    download(entry.link)
                else:
                    print("[%s] %s already downloaded" % (time.strftime("%Y.%m.%d-%H.%M.%S"), entry.title))


def download(magnet):
    """
    Calls transmission-remote to download the specified magnet
    """
    cmd = "transmission-remote %s -n %s:%s --add '%s'" % (IP, USER, PASS, magnet)
    os.system("%s >/dev/null" % (cmd))  # TODO check command response


def update_json(torrent):
    """
    Updates config with the last time the torrent was downloaded
    """
    with open(CONFIG_FILE, "r+") as f:
        data = json.load(f)
        data["torrents"][torrent] = time.strftime("%Y.%m.%d-%H.%M.%S")
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def main():
    print("[%s] RSSTorrentDownloader Started" % (time.strftime("%Y.%m.%d-%H.%M.%S")))
    check_releases()


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(SLEEPTIMER)
