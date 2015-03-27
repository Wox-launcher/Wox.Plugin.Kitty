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
        kitty_path = self.find_kitty_path(kitty_folder_path)
        sessions = self.load_session(kitty_folder_path)
        res = []
        for p in sessions:
            if query in p:
                res.append({"Title": p,"IcoPath":"kitty.png","JsonRPCAction":{"method": "open_session", "parameters": [kitty_path.replace("\\","\\\\"),p]}})
        return res

    def open_session(self,kitty_path,session_name):
        subprocess.call('{} -load "{}"'.format(kitty_path,session_name))

    def find_kitty_path(self,kitty_folder_path):
        """Returns the full path to the user's kitty executable"""

        exe_names = ['kitty.exe', 'kitty_portable.exe']
        for exe_name in exe_names:
            attempted_kitty_exe = os.path.join(kitty_folder_path,exe_name)
            if isfile(attempted_kitty_exe):
                return attempted_kitty_exe

        raise Exception("Could not find Kitty executable in %s" % kitty_folder_path)

if __name__ == "__main__":
    Kitty()
