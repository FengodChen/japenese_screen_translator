from PIL import ImageGrab

class Screen_Cropper:
    def __init__(self):
        self.__h1 = None
        self.__h2 = None
        self.__w1 = None
        self.__w2 = None
        self.__init_flag = False
    
    def set_crop_pos(self, top_left, bottom_right):
        self.__h1 = top_left[0]
        self.__h2 = bottom_right[0]
        self.__w1 = top_left[1]
        self.__w2 = bottom_right[1]
        self.__init_flag = True
    
    def crop(self):
        assert self.__init_flag

        img = ImageGrab.grab(bbox=(self.__w1, self.__h1, self.__w2, self.__h2))
        return img
