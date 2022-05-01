1. Install the requirements with "pip install -r requirements.txt"
2. Go to "https://developer.spotify.com/dashboard/" log in, and create an app.
3. Click on your newly created app. Take note of the Client ID and Client Secret.
4. Edit the settings on your new app, by adding "http://127.0.0.1:5907/callback" to the Redirect URIs
5. Use the config.json file provided as a scaffold to set the desired parameters.
6. Launch the script with "python3 main.py config.json" (or replace config.json with another path)


Relevant details:

1.The only required parameter for the playlists in the config file is the "id".
If not provided, the rest of the parameters are assumed by checking the current ones via the API.

2. Deleteing a playlist description is not possible using the API. If the description is originally
empty, the script will set the playlist name as the description.
