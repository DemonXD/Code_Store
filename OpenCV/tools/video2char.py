import cv2
import numpy as np


def pixel2char(pixel):
    char_list = "@#$%&erytuioplkszxcv=+---.     "
    index = int(pixel / 256 * len(char_list))
    return char_list[index]


def get_char_img(img, scale=4, font_size=5):
    # 调整图片大小
    h, w = img.shape
    re_im = cv2.resize(img, (w//scale, h//scale))
    # 创建一张图片用来填充字符
    char_img = np.ones((h//scale*font_size, w//scale*font_size), dtype=np.uint8)*255
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 遍历图片像素
    for y in range(0, re_im.shape[0]):
        for x in range(0, re_im.shape[1]):
            char_pixel = pixel2char(re_im[y][x])
            cv2.putText(char_img, char_pixel, (x*font_size, y*font_size), font, 0.5, (0, 0, 0))
    return char_img


def generate(input_video, output_video):
    # 1、读取视频
    cap = cv2.VideoCapture(input_video)

    # 2、获取视频帧率
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 读取第一帧，获取转换成字符后的图片的尺寸
    ret, frame = cap.read()
    char_img = get_char_img(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 4)

    # 创建一个VideoWriter，用于保存视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_video, fourcc, fps, (char_img.shape[1], char_img.shape[0]))
    while ret:
        # 读取视频的当前帧，如果没有则跳出循环
        ret, frame = cap.read()
        if not ret:
            break
        # 将当前帧转换成字符图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        char_img = get_char_img(gray, 4)

        # 转换成BGR模式，便于写入视频
        char_img = cv2.cvtColor(char_img, cv2.COLOR_GRAY2BGR)
        writer.write(char_img)
    writer.release()


if __name__ == '__main__':
    generate(r'\path\to\your\test.mp4', r'\path\to\out.mp4')