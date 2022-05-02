import os
import time
import json
import threading

from playlist import Playlist

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Manager:
    def __init__(
        self,
        client_id,
        client_secret,
        playlists,
        wait_between_checks=15,
        error_file='./errors.log',
    ):

        self.error_file = error_file

        os.makedirs(
            os.path.dirname(self.error_file), exist_ok=True
        )

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://127.0.0.1:5907/callback",
                scope="ugc-image-upload playlist-modify-public",
            ),
            retries=5,
        )

        self.playlists = list()
        for pconf in playlists:
            self.playlists.append(
                Playlist(sp, **pconf)
            )

        self.wait_between_checks = wait_between_checks

    def check_playlist(self, pst):
        exception_counter = 0

        while True:
            try:
                pst.check()
                time.sleep(self.wait_between_checks)
            except Exception as e:
                exception_counter += 1
                print(f"Exception while checking for playlist {pst.name} ({pst.id}): {e}")
                with open(self.error_file, 'a') as f:
                    f.write(f"Exception while checking for playlist {pst.name} ({pst.id}): {e}\n")

            if exception_counter > 20:
                print(f"Aborting checks for playlist {pst.name} ({pst.id}) due to too many errors")
                with open(self.error_file, 'a') as f:
                    f.write(f"Aborting checks for playlist {pst.name} ({pst.id}) due to too many errors\n")
                break

    def run(self):
        for pst in self.playlists:
            threading.Thread(
                target=self.check_playlist, args=(pst,)
            ).start()
            time.sleep(1)

if __name__ == '__main__':
    manager = Manager(
        client_id='4c96da7ed3144e169fb236b6cb52738c',
        client_secret='95f881ebecca459898f66616d3712acc',
        config_file='./input_file.json',
    )
    manager.run()
