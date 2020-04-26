CREATE DATABASE spotify;

CREATE TABLE Spotify_History(
	ID int NOT NULL auto_increment,
	Time datetime UNIQUE,
    Song_Name varchar(100),
    Spotify_ID varchar(100),
    Spotify_URI varchar(100),
    Popularity int,
    Object_Type varchar(50),
    primary key(ID)
);

CREATE TABLE Song_Data(
	Spotify_ID varchar(100) UNIQUE,
    Spotify_URI varchar(100),
    Artist varchar(100),
    Album  varchar (100),
    Duration int,
    Acousticness float,
    Danceability float,
    Energy float,
    Instrumentalness float,
    key_spotify int, 
    Liveness float,
    Loudness float,
    Mode int,
    Speechiness float,
    Tempo float,
    Time_Signature int,
    Valence float,
    primary key(Spotify_ID)
);