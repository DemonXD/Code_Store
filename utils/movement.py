#!/usr/bin/env python

'''
SYNOPSIS

    movement.py [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    This is a tool that will watch the output of a video camera. It will
    highlight any movement that it sees. It also detects the relative amount of
    motion and stillnes and indicates significant changes on stdout.
    During period of movement the individual camera frames will be saved.

    THIS IS A ROUGH DRAFT, BUT EVERYTHING WORKS.

    On OS X:
        brew tap homebrew/science
        brew install opencv  # or, "brew install opencv --env=std"
        export PYTHONPATH=/usr/local/lib/python2.7/site-packages:${PYTHONPATH}

    Video playback on OS X:
        brew install mplayer  # takes a long time (~ 5 minutes)
        brew install mencoder
        mplayer -vo corevideo "mf://movement*.png" -mf type=png:fps=30 -loop 0

    Video encoding on OS X:
        mencoder "mf://*.png" -mf type=png:fps=25 -ovc lavc -lavcopts vcodec=mpeg4 -o output.mov

    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    The following are some examples of how to use this script.
    $ movement.py --version
    1

EXIT STATUS

    This exits with status 0 on success and 1 otherwise.
    This exits with a status greater than 1 if there was an
    unexpected run-time error.

AUTHOR

    Noah Spurrier <noah@noah.org>

LICENSE

    This license is approved by the OSI and FSF as GPL-compatible.
        http://opensource.org/licenses/isc-license.txt

    Copyright (c) 2015, Noah Spurrier
    PERMISSION TO USE, COPY, MODIFY, AND/OR DISTRIBUTE THIS SOFTWARE FOR ANY
    PURPOSE WITH OR WITHOUT FEE IS HEREBY GRANTED, PROVIDED THAT THE ABOVE
    COPYRIGHT NOTICE AND THIS PERMISSION NOTICE APPEAR IN ALL COPIES.
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

VERSION

    Version 3
'''

__version__ = 'Version 3'
__date__ = '2015-05-01 15:46:55:z'
__author__ = 'Noah Spurrier <noah@noah.org>'

import sys
import os
import traceback
import optparse
import time
import logging
import cv2
import numpy
import sys
import time
#from pexpect import run, spawn

DELTA_COUNT_THRESHOLD = 1000

def delta_images(t0, t1, t2):
    d1 = cv2.absdiff(t2, t0)
    return d1
#    d1 = cv2.absdiff(t2, t1)
#    return d1
#    d2 = cv2.absdiff(t1, t0)
#    return cv2.bitwise_and(d1, d2)

#for cn in range(2,-1,-1):
for cn in range(0,3):
    cam = cv2.VideoCapture(cn)
    if cam.isOpened():
        break
if not cam.isOpened():
    sys.stderr.write('ERROR: Did not open a camera.\n')
    sys.exit(1)
print("Running with camera number %d." % cn)
print(type(cam))
print(str(cam))
#time.sleep(20)
# 76800 pixels
#cam.set(3,640)
#cam.set(4,480)
# 307200 pixels
cam.set(3,640)
cam.set(4,480)
#cam.set(3,1024)
#cam.set(4,768)

winName = "image diff"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# Fill the queue.
#t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
#t_now = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
#t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
#t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2BGR)
#t_now = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2BGR)
#t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2BGR)
t_minus = cam.read()[1]
t_now = cam.read()[1]
t_plus = cam.read()[1]
t_now = cv2.resize(t_now, (640, 480))
t_minus = cv2.resize(t_minus, (640, 480))
t_plus = cv2.resize(t_plus, (640, 480))
#kernel = numpy.ones((5,5), numpy.uint8)
delta_count_last = 1
#HYSTERESIS =

try:
    os.mkdir("MOVEMENT_FRAMES")
except:
    pass

start_time = time.time()
record_video_state = False
while True:
    delta_view = delta_images(t_minus, t_now, t_plus)
#    cv2.morphologyEx(delta_view, cv2.MORPH_OPEN, kernel)
#    cv2.morphologyEx(delta_view, cv2.MORPH_CLOSE, kernel)
    retval, delta_view = cv2.threshold(delta_view, 16, 255, 3)
    cv2.normalize(delta_view, delta_view, 0, 255, cv2.NORM_MINMAX)
    img_count_view = cv2.cvtColor(delta_view, cv2.COLOR_RGB2GRAY)
    delta_count = cv2.countNonZero(img_count_view)
    delta_view = cv2.flip(delta_view, 1)
    cv2.putText(delta_view, "DELTA: %d"%(delta_count), (5, 15), cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,255))
    cv2.imshow(winName, delta_view)
#    if delta_count_last != 0 or delta_count != 0:
#        sys.stdout.write("%d\n"%(delta_count))
    if (delta_count_last < DELTA_COUNT_THRESHOLD and delta_count >= DELTA_COUNT_THRESHOLD):
        record_video_state = True
        sys.stdout.write("MOVEMENT %f\n" % time.time())
        sys.stdout.flush()
    elif delta_count_last >= DELTA_COUNT_THRESHOLD and delta_count < DELTA_COUNT_THRESHOLD:
        record_video_state = False
        sys.stdout.write("STILL    %f\n" % time.time())
        sys.stdout.flush()
    now=time.time()
    if record_video_state == True:
        cv2.imwrite('MOVEMENT_FRAMES/movement-pong-%f.png' % (now-start_time),delta_view)
    delta_count_last = delta_count
    # move images through the queue.
    t_minus = t_now
    t_now = t_plus
    t_plus = cam.read()[1]
    t_plus = cv2.blur(t_plus,(8,8))
    t_plus = cv2.resize(t_plus, (640, 480))
    #t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2BGR)
    #t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    #t_plus = cv2.bilateralFilter(t_plus,9,75,75)

    # Wait up to 10ms for a key press.
    # If the key is the ESC or 'q' then quit.
    key = cv2.waitKey(10)
    if key == 0x1b or key == ord('q'):
        cv2.destroyWindow(winName)
        break

