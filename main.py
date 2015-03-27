#encoding=utf8
import json
import os,sys,webbrowser
import subprocess
import urllib
from wox import Wox
from os import listdir
from os.path import isfile, join

class Kitty(Wox):

    def load_session(self,kitty_path):
        session_path = os.path.join(kitty_path,"Sessions")
        files = [urllib.unquote(f) for f in listdir(session_path) if isfile(join(session_path,f))]
        return files

    def query(self,query):
        with open(os.path.join(os.path.dirname(__file__),"config.json"), "r") as content_file:
            config = json.loads(content_file.read())
        kitty_folder_path = os.path.expandvars(config["kittyPath"])
        kitty_path = os.path.join(kitty_folder_path,"kitty.exe")
        sessions = self.load_session(kitty_folder_path)
        res = []
        for p in sessions:
            if query in p:
                res.append({"Title": p,"IcoPath":"kitty.png","JsonRPCAction":{"method": "open_session", "parameters": [kitty_path.replace("\\","\\\\"),p]}})
        return res

    def open_session(self,kitty_path,session_name):
        subprocess.call('{} -load "{}"'.format(kitty_path,session_name))

if __name__ == "__main__":
    Kitty()
