import mysql
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

class DatabaseHandler():
    
    """
    Class to write the spotify data into a MySql Database. The database has two tables with the names [spotify_history, song_data]
    spotify_history has the following colums in that order: (ID (primary key, auto increment), Time, Song_Name, Spotify_ID, 
    Spotify_URI, Popularity, Object_Type)
    song_data has the following colums in that order: (Spotify_ID (primary key), Spotify_URI, Artist, Album, Duration, Acousticness, 
    Danceability, Energy, Instrumentalness, key_spotify, Liveness, Loudness, Mode, Speechiness, Tempo, Time_Signature, Valence)
    """
    def __init__(self, host, database, user, password, auth_plugin = None):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.auth_plugin = auth_plugin
        
        
    def connect(self):
        """
        Function to connect to a database and the feedback, if that connection was succesful or not
        """
        self.connection = mysql.connector.connect(host=self.host, 
                                                  database=self.database, 
                                                  user=self.user, 
                                                  password=self.password, 
                                                  auth_plugin=self.auth_plugin)
        if self.connection.is_connected():
            print("Succesful connection to the database {} as {}".format(self.database, self.user))
            self.cursor = self.connection.cursor()
        else:
            print("The connection to the database was not successful.")
    
    def close(self):
        """
        Closing of the database connection
        """
        self.connection.close()
        
    def write_to_db(self, df):
        
        """
        Write to the MySql Database
        """
        #query for the history data
        query = "INSERT IGNORE INTO spotify_history (Time, Song_Name, Spotify_ID, Spotify_URI, Popularity, Object_Type) VALUES (%s, %s, %s, %s, %s, %s)"
        
        val = []
        for index, row in df.iterrows():
            #some songs don't have milisecond, so the dateformat needs to be adapted
            try:
                timestamp = datetime.strptime(row["timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                datetime.strptime(row["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
            finally:
                val.append((timestamp, 
                            row["name"], 
                            row["id"], 
                            row["uri"], 
                            row["popularity"], 
                            row["object_type"]))

        self.cursor.executemany(query, val)
        print("New Songs in the History {}".format(self.cursor.rowcount))
        
        #query for the song properties
        query = "INSERT IGNORE INTO song_data (Spotify_ID, Spotify_URI, Artist, Album, Duration, Acousticness, Danceability, Energy, Instrumentalness, key_spotify, Liveness, Loudness, Mode, Speechiness, Tempo, Time_Signature, Valence) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = []
        for index, row in df.iterrows():
            val.append((row["id"], 
                       row["uri"], 
                       row["artist"], 
                       row["album"], 
                       row["duration_ms"], 
                       row["acousticness"],
                       row["danceability"],
                       row["energy"],
                       row["instrumentalness"],
                       row["key"],
                       row["liveness"],
                       row["loudness"],
                       row["mode"],
                       row["speechiness"],
                       row["tempo"],
                       row["time_signature"],
                       row["valence"])
                      )
        
        print("New Songs in the database: {}".format(self.cursor.rowcount))
        self.cursor.executemany(query, val)
        
        self.connection.commit()


    def query_data(self, sql_query):
        pass