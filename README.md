# Sparrow

Before I describe the nature of this program I should state that this program was made for practice and education in python, and should not be used for pirating.

However, this program is used to pull locations of movies online, and where they can be downloaded.

## Sparrow.py
This file contains a variety of functions for finding movie data
***getLink***
  Uses bs4 to find the the selected table in a given url
***getImdb***
  Uses getLink to search Imdb and return the link to the most relevant movie
***getMagnet***
  shamefully finds the link to the most reputable magnet on piratebay
***getImage***
  uses getImdb to find a link to the image associated with searched movie
***getRating**
  uses getImdb to return the imdb rating of the searched movie
***getGenres***
  uses getImdb to return the associated genres from a searched movie
***getDirector***
  self explanatory
***getCast***
  see getDirector
***getMovies***
  takes in a list of strings and writes a json file of their associated properties (listed above)
***waitandDownload***
  uses getMovies and pyautogui to begin downloading, and start utorrent
  
