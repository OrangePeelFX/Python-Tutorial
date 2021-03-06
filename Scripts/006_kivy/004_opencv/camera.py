#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la camera avec OpenCV

pip install opencv-python
"""
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class KivyCvCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCvCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCvCamera(capture=self.capture, fps=60)
        return self.my_camera

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
