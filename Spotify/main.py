from authorisation import SpotifyAuthorisation
from dbconnector import DatabaseHandler
from extractdata import DataExtracter

#Define the information needed to extract the data
client_id = ""
scope = "user-read-recently-played"
client_secret = ""
redirect_uri = "http://localhost:8888"

#Check for Authorisation and get a token to make the requests in the spotify webapi
sp = SpotifyAuthorisation(client_id, client_secret, scope, redirect_uri)

#Load the tokeninformation save as file in the same directionary
token_info = sp.get_tokeninfo()
token = token_info["access_token"]

#Extract the data
da = DataExtracter(token)
data = da.extract_data()

#Write the data into a dataframe
db = DatabaseHandler(host = "127.0.0.1",
                     database = "",
                     user = "",
                     password = "",
                     auth_plugin = "mysql_native_password")

db.connect()
db.write_to_db(data)
db.close()