# Spotify Data Collector

## To Do
- Create Tableau Dashboard providing interesting insights into listening habits  
- edit the path where the token is saved to a flexible path
- automate the renaming of the token information with the refresh token, when there is no document with the refresh token

## Purpose of the Project

The purpose of this project is to collect the most recent heard songs on spotify and collect and store them into a MySql Database. The data should be used to visualize interesting insights about the personal music habits into a Tableau Dashboard. If the main.py is executed the a MySQL Database will be written with the most recently listened songs. The app access thereby the Spotify Web Api to extract these songs. For more information about the Spotify Web Api, please check their pages (https://developer.spotify.com/documentation/web-api/quick-start/). 

## First Steps

1. Create an App on the Spotify for Developer Page (https://developer.spotify.com/dashboard/).
2. Add a redirect URL to the white list of the created Application.
3. Set up a MySQL Database. More information can be found on the MySQL Pages (https://dev.mysql.com/doc/mysql-getting-started/en/). The database with the neccessary tables and columns can be created by running the SQL Code in the folder "SQL".
4. Edit the main.py file with your personal information. Add your client_id and secret which can be found in the view of your application on Spotify for Developer. Edit also the redirect_url to one specified in the white list of your app. Add your MySQL Database information, so that the client can connect to your database and write the information in. 
5. Specify the path in the authorization.py file in the read_token method to the file which leads to the Authorization folder in your local client.
6. Run the main.py file for the first time to get your Authorization Information. After running main.py you will be redirected to your redirect_url. Copy the url of in paste it into the terminal. The code will extract the neccessary information on its own. 
7. The document will be saved in the folder Authorization. If you run the code the first time, rename your file to "Refresh.txt". This file will include your refresh token, which the app will access to get access in the future. 
8. Automate the execution of the main.py file. If you have windows you can do that easily with the Windows Task Scheduler.

## Content of the Modules
**main.py**: The main Python File to execute the data collection.
**authorization.py**: Handles the Authorization of to access the Spotify Web Api after the Authorization Code Flow. More information about the Authorization and the Authoriztion Code Flow can be found here: https://developer.spotify.com/documentation/general/guides/authorization-guide/
**dbconnector.py**: Handles the connection to the MySQL database and writes the information provided by the Spotify Web Api to it.
**extractdata.py**: Handles the extraction of the recently listened songs and some audio features of this song. The extracted data will be returned as pandas Dataframe

## Restrictions
- The Spotify Web Api can return a maximum of the last 50 listened songs. Keep that in mind if you want to collect the data to avoid gaps in it.
