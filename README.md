# Sparrow

Before I describe the nature of this program I should state that this program was made for practice and education in python, and should not be used for pirating.

However, this program is used to pull locations of movies online, and where they can be downloaded.

## Sparrow.py
This file contains a variety of functions for finding movie data\n
***getLink***\n
]tUses bs4 to find the the selected table in a given url\n
***getImdb***\n
\t Uses getLink to search Imdb and return the link to the most relevant movie\n
***getMagnet***\n
\t shamefully finds the link to the most reputable magnet on piratebay\n
***getImage***\n
\t uses getImdb to find a link to the image associated with searched movie\n
***getRating**\n
\t uses getImdb to return the imdb rating of the searched movie\n
***getGenres***\n
\t uses getImdb to return the associated genres from a searched movie\n
***getDirector***\n
\t self explanatory\n
***getCast***\n
\t see getDirector\n
***getMovies***\n
\t takes in a list of strings and writes a json file of their associated properties (listed above)\n
***waitandDownload***\n
\t uses getMovies and pyautogui to begin downloading, and start utorrent\n
  
