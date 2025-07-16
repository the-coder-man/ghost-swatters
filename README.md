Instructions:
If you’re seeing this then congratulations! You just downloaded ghost swatters. Now I know you probably can’t wait to play this game but before you do it requires some setup. Fortunately it’s very easy just copy and paste the following commands into your terminal and then press the play button.
Note: these commands should be used depending on your preferences and python virtual environment.

what is ghost swatters?

first of all what is ghost swatters? Well it's a tech demo for the python libary openCV that also uses pygame. But also a video game where you earns points by swatting ghosts, and the game ends when a ghost reaches the bottom of the screen this game is diffrent from most other games the reason? it uses your computer's web cam to track your hand movements that inturn moves the white square (the repersentation of the player) on the screen that is required to move in order to collect the ghosts to earn points. another fun thing about this game is that
this game only requires three physical things to play: a computer, a webcam and your hand no external acessories required!  

Commands (required):

pip install pygame

pip install opencv-python 


Commands (optional):

If you need a specific version use:
 pip install opencv-python==4.5.1 
(or the version of your choice)

If you need extra modules use:

pip install opencv-contrib-python

If you’re using conda use this command:

conda install -c conda-forge opencv

Finally to verify the installation open a new python file and use:

import cv2
print("OpenCV version:", cv2.__version__)

If OpenCV is installed correctly, you should see the version number printed in the console.
