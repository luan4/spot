import os
import base64
import requests
from datetime import datetime

class PlaylistConfigError(Exception):
    pass

class Playlist:
    def __init__(
        self,
        sp,
        id,
        name=None,
        description=None,
        log_file=None,
        image_path=None,
    ):

        self.sp = sp
        self.id = id

        new_data = self.sp.playlist(self.id)

        self.name = name or new_data['name']
        self.description = description or new_data['description'] or self.name
        self.image_path = image_path
        if not image_path:
            self.image_path = f"./images/{self.id}.jpeg"
            os.makedirs(
                os.path.dirname(self.image_path),
                exist_ok=True,
            )
            img_data = requests.get(
                new_data['images'][0]['url']
            ).content
            with open(self.image_path, 'wb') as f:
                f.write(img_data)
        if not os.path.isfile(self.image_path):
            raise PlaylistConfigError(f"Could not find a file at {self.image_path}")
        self.log_file = log_file or f"./logs/{self.name}.log"
        os.makedirs(
            os.path.dirname(self.log_file), exist_ok=True
        )

    def check(self):
        new_data = self.sp.playlist(self.id)
        print(f"Checking \"{self.name}\" {self.id}")
        if (new_data['name'], new_data['description']) != (self.name, self.description):
            with open(self.log_file, 'a') as f:
                f.write(
                    f"{datetime.utcnow()} - Detected changes on \"{self.name}\" {self.id}\n"
                )
            self.revert_changes()

    def revert_changes(self):
        print(f"{datetime.utcnow()} - Reverting changes to \"{self.name}\" {self.id}")

        self.sp.playlist_change_details(
            self.id,
            name=self.name,
            description=self.description,
        )
        with open(self.image_path, 'rb') as f:
            encoded_image = base64.b64encode(f.read())

        self.sp.playlist_upload_cover_image(
            self.id,
            encoded_image,
        )
