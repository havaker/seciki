import argparse
import os
import subprocess

from dataclasses import dataclass
from xdg import XDG_DATA_HOME

from scdl import client
from scdl import scdl

@dataclass
class Config:
    username: str
    download_path: str = None
    index_path: str = os.path.join(XDG_DATA_HOME, "seciki/index.txt")

    @classmethod
    def from_args(cls):
        parser = argparse.ArgumentParser(description='Download some seciki.')
        parser.add_argument(
            "username",
            metavar="username",
            type=str,
            help="soundcloud username"
        )
        parser.add_argument(
            "--download-path",
            metavar="path",
            type=str,
            help="path where songs are saved"
        )
        parser.add_argument(
            "--index-path",
            metavar="path",
            type=str,
            help="path where index is saved"
        )
        args = parser.parse_args()

        default = cls(args.username)
        if args.download_path:
            default.download_path = args.download_path
        if args.index_path:
            default.index_path = args.index_path
        return default

class FavsLister:
    def __init__(self, config):
        user_link = "https://soundcloud.com/" + config.username
        self.user = scdl.get_item(user_link)

    def list_urls(self):
        dl_url = scdl.url["favorites"].format(self.user["id"])
        resources = scdl.client.get_collection(dl_url, None)
        return [resource["track"]["permalink_url"] for resource in resources]

class Downloader:
    def __init__(self, config):
        self.path = config.download_path

    def download(self, link):
        command = ["scdl", "--onlymp3", "-l", link]
        if self.path:
            subprocess.call(command, cwd=self.path)
        else:
            subprocess.call(command)

class Index:
    def __init__(self, config):
        self.path = config.index_path
        dirname = os.path.dirname(self.path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def load(self):
        try:
            with open(self.path) as f:
                return [line.rstrip() for line in f]
        except:
            return []

    def save(self, url):
        with open(self.path, 'a') as f:
            f.write(url + '\n')

config = Config.from_args()

index = Index(config)
lister = FavsLister(config)
downloader = Downloader(config)

fav_urls = lister.list_urls()
saved_urls = index.load()
unsaved_urls = set(fav_urls) - set(saved_urls)

for url in unsaved_urls:
    downloader.download(url)
    index.save(url)
