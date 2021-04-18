#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:13:23 2021
@author: obooklage
Huion Pen Display Kamvas 13 setup https://www.huion.com/pen_display/Kamvas/kamvas-13.html
"""

import os
import tkinter as tk
import subprocess

'''
My current four screens configuration

******* ******* ******* *******
|  1  | |HUION| |  3  | |  4  |
******* ******* ******* *******

'''

# Total Screen size

total_width = 4*1920 # Four monitors 1920 pixels width, 4*1920=7680 pixels
total_height = 1080  # All monitors horizontal

# Huion Screen resolution

touch_area_width = 1920 # Huion width
touch_area_height = 1080 # Huion height

# Huion Screen localization

touch_area_x_offset = 1920 # Huion start at 1920 pixels from left
touch_area_y_offset = 0 # no offset vertically

# Pen adjustment

x_correction = -0.0037 # Negative=to left, Positive=To right
y_correction = -0.005 # Negative=to Up, Positive=To Down

# Matrix

c0 = touch_area_width / total_width # 1920/7680 = 0.25
c2 = touch_area_height / total_height # 1080/1080 = 1
c1 = touch_area_x_offset / total_width + x_correction # 1920/7680 -0.003 = 0.247
c3 = touch_area_y_offset / total_height + y_correction # 0/1080 -0.005 = -0.005

# print(c0, c1, c2, c3)

def SetPen(c0, c1, c2, c3):
    lines = subprocess.check_output(["xinput", "list"]).decode('utf-8').splitlines()
    
    for line in lines:
        if ("Tablet Monitor Pen" in line) and ("pointer" in line):
            parts = line.split("\t")
            for part in parts:
                if "id=" in part:
                    id = part.split("=")[1]
                    subprocess.Popen(['xinput set-prop %s --type=float "Coordinate Transformation Matrix" %s 0 %s 0 %s %s 0 0 1' % (id, c0, c1, c2, c3)], shell = True)
                    return(int(id))
    return(-1)
                
def center_window(window, w=300, h=50):
    # get screen width and height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

id = SetPen(c0, c1, c2, c3)
if( id > 0 ):
    message = "Tablet Monitor Pen (pointer) id " + str(id) + " setup done."
else:
    message = "ERROR\nTablet Monitor Pen (pointer) not found\nUse the pen for activate the USB detection"
    
racine = tk.Tk()
racine.iconphoto(False, tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), 'huion_logo.png')))
racine.title("HUION SETUP")
center_window(racine)
label = tk.Label(racine, text=message)
bouton = tk.Button(racine, text="Quit", fg="red", command=racine.destroy)
label.pack()
bouton.pack()
racine.mainloop()
