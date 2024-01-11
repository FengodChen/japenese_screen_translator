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


def screen_cropper_process(pipe_mainGUI, pipe_ocr):
    screen_cropper = Screen_Cropper()

    while True:
        try:
            msg = pipe_mainGUI.recv()
            if msg["comm"] == "start crop":
                img = screen_cropper.crop()
                msg = dict(
                    comm = "push crop img",
                    data = img
                )
                pipe_mainGUI.send(msg)
            elif msg["comm"] == "set crop pos":
                (top_left, bottom_right) = msg["data"]
                screen_cropper.set_crop_pos(top_left, bottom_right)
            elif msg["comm"] == "end":
                break
        except Exception as e:
            print(str(e))