import cv2 as cv
import numpy as np
import torch
from PIL import ImageGrab

class SreenSelector:
    def __init__(self):
        self.__img = None
        self.__img_base = None

        self.__left_button_down_flag = False
        self.__left_button_down_pos = (0, 0)
        self.__left_buttom_up_pos = (0, 0)

    def __init_screen_image(self):
        img = ImageGrab.grab()
        img = img.convert('RGB')
        img = np.array(img)
        img = img[:, :, ::-1].copy()

        self.__img = img
        self.__img_base = img.copy()
    
    def __opencv_mouse_event_callback(self, event, x, y, flags, parmas):
        if event == cv.EVENT_LBUTTONDOWN:
            self.__left_button_down_flag = True
            self.__left_button_down_pos = (x, y)
        elif event == cv.EVENT_MOUSEMOVE:
            if self.__left_button_down_flag == True:
                self.__img = self.__img_base.copy()
                cv.rectangle(self.__img, self.__left_button_down_pos, (x, y), (0, 0, 255), 5)
            else:
                pass
        elif event == cv.EVENT_LBUTTONUP:
            self.__left_buttom_up_pos = (x, y)
            self.__left_button_down_flag = False
    
    def ui_show(self, windows_name="image"):
        self.__init_screen_image()
        cv.namedWindow(windows_name, cv.WINDOW_NORMAL)
        cv.setWindowProperty(windows_name, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.setMouseCallback(windows_name, self.__opencv_mouse_event_callback)
        while True:
            cv.imshow(windows_name, self.__img)
            if cv.waitKey(20) & 0xFF == 27:
                break
        cv.destroyWindow(windows_name)
    
    def get_screen_pos(self):
        (w1, h1) = self.__left_button_down_pos
        (w2, h2) = self.__left_buttom_up_pos

        left = min(w1, w2)
        right = max(w1, w2)
        top = min(h1, h2)
        bottom = max(h1, h2)

        top_left = (top, left)
        bottom_right = (bottom, right)

        return (top_left, bottom_right)


if __name__ == "__main__":
    ss = SreenSelector()
    ss.ui_show()
    (p1, p2) = ss.get_screen_pos()
    print(p1)
    print(p2)