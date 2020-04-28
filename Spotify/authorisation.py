import webbrowser
import requests
import json
import base64
import six

#To Do
# Save token in document in json format
# get the token out of the document, if token is expired access get new token and overwrite it

class SpotifyAuthorisation():
    
    """
    Class to handle the Authorization to the Spotify Web API. The class is initiated with a client_id, client_secret, scope and 
    redirect_uri. 
    
    Spotify Dashboard: https://developer.spotify.com/dashboard/login 
    Documentaton Spotify Web API: https://developer.spotify.com/documentation/web-api/quick-start/
    Authorization Guide: https://developer.spotify.com/documentation/general/guides/authorization-guide/
    
    client_id and client secret: Will be provided when an App is created on the Spotify Developer Pages
    Scope: Determines the authorization the user needs to provide to access specific data in the Spotify Web API. More information 
    can be found in the documentation for the spotify web api
    redirect_uri: Needs to be added to the white list of the App created on the Spotify Developer Pages
    """
    
    def __init__(self, client_id:str, client_secret:str, scope:str, redirect_uri:str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri
        
    def read_token(self, document):
        """
        Reads the file with the information about the token.
        """
        with open(r"C:\Users\KhacM\GitHub\MinhLe\Spotify\Authorisation\{}".format(document), "r") as file:
                token_info = file.read()
                file.close()

        token_info = json.loads(token_info)
        
        return token_info
    
    def get_tokeninfo(self):  
        """
        Get the current Token information saved in the document Token_info.txt. If the Document does not exist a new token will be 
        created. If the token is expired a new token will be created with the refresh token in the document. If there is no refresh 
        token a complete new token will be created and saved in .../Authorisation/Token_info.txt. 
        """
        try:
            token_info = self.read_token("Token_info.txt")
        except:
            print("It seems that there is no token available. A new token will be created.")
            self.get_token()
            
            token_info = self.read_token("Token_info.txt")
            
        #Test if the token is expired or not
        expired = self.test_token(token_info["access_token"])
        
        #If the token is expired a new one will be created with the refresh_token. If the refresh_token does not exist a complete 
        #new one will be created
        if expired:
            try:
                token_info = self.read_token("Refresh.txt")
                self.refresh_token(token_info["refresh_token"])
                token_info = self.read_token("Token_info.txt")
            except:
                print("No Refresh Token found...")
                self.get_token()
                token_info = self.read_token("Token_info.txt")
        return token_info

        
    def get_authorization_code(self):
        
        """
        Redirect the user to the page, where the Authorization Code in the url can be copied to get the access token
        """
        #Request to the spotify web api endpoint to access the authorization code
        query = "https://accounts.spotify.com/authorize"
        response = requests.get(query, 
                               params = {"client_id": self.client_id,
                                         "response_type": "code",
                                         "redirect_uri": self.redirect_uri,
                                         "scope": self.scope,
                                         "show_dialog": "false"
                                        })
        
        #Open the url, so that the url of the redirection page can be copied
        webbrowser.open(response.url)
        
    def get_token(self):
        """
        Function to get the Token with the Authorization Code. The URL of the page the user is redirect to needs to be copied into 
        the terminal. The response of the request to get the token will be saved in ./Authorisation/Token_info.txt to make it 
        accessable via the App
        """
        print("A new token will be created...")
        self.get_authorization_code()
        print("Please paste the url of the redirected into the console:")
        redirect_url = input()
        code_index = redirect_url.find("code")
        
        query = "https://accounts.spotify.com/api/token"
        code = redirect_url[code_index+5:]
        auth_header = base64.b64encode(six.text_type(self.client_id + ":" + self.client_secret).encode("ascii"))
        headers = {"Authorization": "Basic %s" % auth_header.decode("ascii"), "Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(query, 
                                 data = {"grant_type": "authorization_code",
                                          "code": code,
                                          "redirect_uri": "http://localhost:8888"},
                                 headers = headers)
        
        if response.status_code == 200:
            with open("Authorisation/Token_info.txt", "w+") as file:
                file.write(response.text)
                file.close
        else:
            print(response.content)
        
    def refresh_token(self, refresh_token):
        """
        Method to refresh the token with the help of a refresh token
        """
        
        print("The token will be refreshed...")
        query = "https://accounts.spotify.com/api/token"
        auth_header = base64.b64encode(six.text_type(self.client_id + ":" + self.client_secret).encode("ascii"))
        headers = {"Authorization": "Basic %s" % auth_header.decode("ascii"), "Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(query, 
                                 data = {"grant_type": "refresh_token",
                                          "refresh_token": refresh_token},
                                 headers = headers)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            with open("Authorisation/Token_info.txt", "w+") as file:
                file.write(response.text)
                file.close
            print("The token is refreshed.")
        else:
            print(response.content)
    
    def test_token(self, token): 
        """
        Test if the token is expired or not. Returns True if the token is expired.
        """
        spot_id = "4evmHXcjt3bTUHD1cvny97"
        endpoint = "https://api.spotify.com/v1/audio-features"
        header = {"Authorization": "Bearer {}".format(token)}
        
        response = requests.get("{}/{}".format(endpoint, spot_id),
                               headers = header)
        
        if response.status_code == 401:
            print("The token is expired")
            return True
        else:
            return False