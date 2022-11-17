import cv2
import pandas as pd
import time
import dropbox
import os
import numpy as np
from PIL import ImageGrab
import random


start_time = time.time()


# def take_snapshot():
#
#     number = random.randint(0, 100)
#
#     videoCaptureObject=cv2.VideoCapture(0)
#
#     result = True
#     while(result):
#         ret, frame = videoCaptureObject.read()
#         img_name = "img" + str(number) + ".png"
#         cv2.imwrite(img_name, frame)
#         color_detect(img_name)
#         color_grab(img_name)
#         start_time = time.time()
#         result = False
#     return img_name
#     print("snapshot taken")
#
#     videoCaptureObject.release()
#     cv2.destroyAllWindows()


def color_detect(file_path):

    # Reading the image with opencv

    img = cv2.imread(file_path, cv2.IMREAD_COLOR)

    # Declaring global variables (are used later on)
    global b, g, r, x_pos, y_pos, clicked
    clicked = False
    r = g = b = x_pos = y_pos = 0

    # Reading csv file with pandas and giving names to each column
    index = ["color", "color_name", "hex", "Red", "Green", "Blue"]
    df = pd.read_csv('colors.csv', names=index, header=None)

    # Function to calculate minimum distance from all colors and get the most matching color
    def get_color_name(R, G, B):
        minimum = 10000
        for i in range(len(df)):
            dist = abs(R - int(df.loc[i, "Red"])) + abs(G - int(df.loc[i, "Green"])) + abs(B - int(df.loc[i, "Blue"]))
            if dist <= minimum:
                minimum = dist
                color_name = df.loc[i, "color_name"]
        return color_name

    # Function to get x,y coordinates of mouse double click
    def draw_function(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            global b, g, r, x_pos, y_pos, clicked
            clicked = True
            x_pos = x
            y_pos = y
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)

    while True:

        cv2.imshow("image", img)
        if clicked:

            # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

            # Creating text string to display (Color name and RGB values)
            text = get_color_name(r, g, b) + ' | R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # cv2.putText(img, text, start, font(0-7),fontScale, color, thickness, lineType)
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # For very light colours we will display text in black colour
            if r+g+b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            clicked = False

        # Break the loop when user hits 'ese' key
        if cv2.waitKey(20) & 0XFF == 27:
            break

    cv2.destroyAllWindows()


def color_grab(img_name):

    # 擷取帶RGB回應的影像, 目前預設全螢幕
    img = ImageGrab.grab()
    img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)

    # 建立儲存路徑
    screen_path = os.path.join(os.path.dirname(__file__), 'screen')
    if not os.path.exists(screen_path):
        os.makedirs(screen_path)

    # 保存圖片到儲存路徑
    image_name = os.path.join(screen_path, img_name)
    t = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    cv2.imwrite(('%s_%s.png' % (image_name, t)), img)
    # img.save('%s_%s.png' % (image_name, t))

    cv2.destroyAllWindows()


def upload_file(img_name):

    access_token = "xxxxxx"
    file = img_name
    file_from = file
    file_to = "/python/" + (img_name)
    dbx = dropbox.Dropbox(access_token)

    with open(file_from, 'rb') as f:
        dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)
        print("file uploaded")


# def main():
#     while(True):
#         if ((time.time() - start_time) >= 5):
#             # name = color_grab()
#             # name = take_snapshot()
#             upload_file()
#
#     main()


if __name__ == '__main__':
    # take_snapshot()
    color_detect()
    color_grab()
    upload_file()
    # main()

    # webcam.display_on_opencv_windows()
    def count_test():
        for i in range(1000):
            print(i)
            time.sleep(0.1)

