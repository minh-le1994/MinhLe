import requests
import pandas as pd
import json
from authorisation import SpotifyAuthorisation

class DataExtracter():
    
    """
    Class to extract the data from the Spotify Web Api regarding the last 50 songs played and the audio features of this songs. The 
    class is initiated with the token needed to access the spotify web api
    """
    
    def __init__(self, token): 
        self.base_query = "https://api.spotify.com/v1"
        self.token = token

    #Read last fifty songs
    def get_recent_songs(self):
        """
        Sends a request to the spotify web api and returns the last 50 played songs from the respective user.
        """
        endpoint = "/me/player/recently-played"
        params = {"limit": 50}
        header = {"Authorization": "Bearer {}".format(self.token)}

        response = requests.get("{}{}".format(self.base_query, endpoint),
                                params = params,
                                headers = header
                               )
        print("Song History Request Status: {}".format(response.status_code))
        return response
    
    def get_song_properties(self, spotify_ids:list):
        """
        Returns the song audio features given an list of spotify ids
        """
        endpoint = "audio-features"
        response = requests.get("{}/{}".format(self.base_query, endpoint), 
                                params = {"ids": ",".join(spotify_ids)}, 
                                headers = {"Authorization": "Bearer {}".format(self.token)})
        
        print("Song Properties Request Status: {}".format(response.status_code))
        return response

    def extract_data(self):
        """
        Extract the recently last 50 songs and the audio features to return it as a pandas DataFrame
        """
        response = self.get_recent_songs()
        dic = {"timestamp": [], "name": [], "id": [], "uri": [], "popularity": [], "object_type": [], "artist": [], "album": []}

        for element in response.json()["items"]:
            dic["timestamp"].append(element["played_at"])
            dic["name"].append(element["track"]["name"])
            dic["id"].append(element["track"]["id"])
            dic["uri"].append(element["track"]["uri"])
            dic["object_type"].append(element["context"]["type"])
            dic["popularity"].append(element["track"]["popularity"])
            dic["album"].append(",".join([artist["name"] for artist in element["track"]["artists"]]))
            dic["artist"].append(element["track"]["album"]["name"])
        
        
        keys = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", 
        "valence", "tempo", "duration_ms", "time_signature", "id", "uri"]
    
        response = self.get_song_properties(dic["id"])
        
        for key in keys:
            dic[key] = []
            
        for element in response.json()["audio_features"]:
            print(element)
            for key in keys:
                try:
                    dic[key].append(element[key])
                except: 
                    dic[key].append(0)
   
        self.song_data = pd.DataFrame(dic)
        
        return self.song_data    