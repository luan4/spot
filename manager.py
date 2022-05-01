import time
import json

from playlist import Playlist

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Manager:
    def __init__(
        self,
        client_id,
        client_secret,
        config_file,
        ):

        self.playlists = list()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:5907/callback",
            scope="ugc-image-upload playlist-modify-public",
        ))

        with open(config_file) as f:
            conf = json.load(f)
        for pconf in conf:
            self.playlists.append(
                Playlist(sp, **pconf)
            )

    def run(self):
        while True:
            for pst in self.playlists:
                try:
                    pst.check()
                except Exception as e:
                    print(f"Exception while checking for playlist {pst.name} ({pst.id}): {e}")
                time.sleep(1)

if __name__ == '__main__':
    manager = Manager(
        client_id='4c96da7ed3144e169fb236b6cb52738c',
        client_secret='95f881ebecca459898f66616d3712acc',
        config_file='./input_file.json',
    )
    manager.run()
