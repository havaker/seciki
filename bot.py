import subprocess

from dataclasses import dataclass

from scdl import client
from scdl import scdl

@dataclass
class Config:
    username: str
    path: str = None

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
        self.path = config.path

    def download(self, link):
        command = ["scdl", "--onlymp3", "-l", link]
        if self.path:
            subprocess.call(command, cwd=self.path)
        else:
            subprocess.call(command)

config = Config("djmcmostowiak", "hej/")

lister = FavsLister(config)
downloader = Downloader(config)

downloader.download(lister.list_urls()[0])
