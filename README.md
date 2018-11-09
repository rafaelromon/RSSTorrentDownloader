# RSSTorrentDownloader
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

Automatically download new torrents from a RSS feed

### Upcoming Features
* Support for multiple RSS feeds
* Limited log file size
* Improved logger by checking transmission-remote command output
* Whatever stupid feature i come up with

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them
* Any GNU/Linux Distro, i have tested it on Arch and Raspbian.
* A Transmission Server, see [Deployment](Deployment) for additional information.
* python3 and transmission-remote packages.
* Additional Python packages: feedparser and pytz.

##### On Debian based Distros
```
sudo apt install python3, transmission-remote, python-pip
pip install feedparser, pytz
```

##### Arch based Distros
```
sudo pacman -S python3, transmission-remote, python3-pip
pip3 install feedparser, pytz
```

### Installing
1. Clone this repo into your local machine.

  ```
git clone https://github.com/rafaelromon/RSSTorrentDownloader
```
2. Edit the config file using your editor of choice see our [Wiki](https://github.com/rafaelromon/RSSTorrentDownloader/wiki/Configuration-File) for further explanation.
3. Change path to config file on line 36 inside rss_torrent_downloader.py.

  ```
CONFIG_FILE = "/path/to/RSSTorrenTDownloader/config.json"
```

Additionally you may want to execute this at startup

1. Open cron file.

  ```
crontab -e
```

2. Add this line at the end of your file, this will not work if you didnt use absolute paths.

  ```
@reboot sleep 60; python3 /path/to/RSSTorrentDownload/rss_torrent_download.py
```

## Deployment

Raspberry Pi

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) for details
