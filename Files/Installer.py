### this is the installer for Sparrow
##first pip must be installed
import pip
import sys
import os

fileLink = None #Placeholder until app is completed
packages = ['httplib2','bs4','json','pyautogui','imdbpy']
for package in packages:
    pip.main(['install',package])



if not os.path.exists('C:\Sparrow\\'):
    os.makedirs('C:\Sparrow\Images\\')
    os.makedirs('C:\Sparrow\ObjectData.json')
    os.makedirs('C:\Sparrow\Buttons\\')
    os.makedirs('C:\Sparrow\Files\\')

##after file is completed, write everything to its respective folders
sys.path.append('C:\Sparrow\Files\\')
                
                      
    
