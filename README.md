# RSSTorrentDownloader
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

RSSTorrentDownloader checks for text occurences on a torrent RSS Feed, and start downloading them on a tranmission-server.

### Features
* Support for multiple RSS feeds.

### Upcoming Features
* Improved logger by checking transmission-remote command output.
* Whatever stupid feature i come up with.

## Getting Started

### Prerequisites

* Any GNU/Linux Distro, i have tested it on Arch and Raspbian.
* A Transmission Server, see [Deployment](https://github.com/rafaelromon/RSSTorrentDownloader#deployment) for additional information.
* python3 and transmission-remote packages.
* Additional Python packages: feedparser and pytz.

##### On Debian based Distros
```
sudo apt install python3, transmission-remote, python3-pip
sudo pip3 install -r requirements.txt
```

##### Arch based Distros
```
sudo pacman -S python, transmission-remote, python-pip
sudo pip install -r requirements.txt
```

### Installing
1. Clone this repo into your local machine.

  ```
git clone https://github.com/rafaelromon/RSSTorrentDownloader
```
2. Edit the config file using your editor of choice see our [Wiki](https://github.com/rafaelromon/RSSTorrentDownloader/wiki/Configuration-File) for further explanation.
3. Change the path to the config file on line 36 inside rss_torrent_downloader.py, make sure you use absolute paths.

  ```
CONFIG_FILE = "/path/to/RSSTorrenTDownloader/config.json"
```

Additionally if you want to execute this at system startup

1. Open cron file.

  ```
crontab -e
```

2. Add this line at the end of your file, this will not work if you didn't use absolute paths.

  ```
@reboot sleep 60; python3 /path/to/RSSTorrentDownload/rss_torrent_download.py
```

## Deployment

For RSSTorrentDownloader to work at it's fullest it should be run 24h a day, for that i recommend using a Raspberry Pi or any other small GNU/Linux enviroment that can be left turned on.

It is also recommended to leave the transmission server on the same system, as this should also remain running all day, you can also create a samba share on your machine to access those downloaded files from other computers on your network, all of this is covered in this [tutorial](https://www.raspberrypi.org/forums/viewtopic.php?t=51219). 

## Contributing

- As the license states, you can fork and redistribute this as long as it remains as a GPL project.
- If you are not that tech savvy feel free to send me any bug reports, ask me any questions or request any features via email, just keep in mind I do this as side project hobby.

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) for details.
