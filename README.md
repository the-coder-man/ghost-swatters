Instructions:
If you’re seeing this then congratulations! You just downloaded ghost swatters. Now I know you probably can’t wait to play this game but before you do it requires some setup. Fortunately it’s very easy just copy and paste the following commands into your terminal and then press the play button.

Note: these commands should be used depending on your preferences and python virtual environment.


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
