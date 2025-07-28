# capture.py
# 螢幕擷取模組：擷取指定矩形區域的螢幕畫面，並轉為 OpenCV BGR 格式
# 用於 8BallPool_assist 的畫面輸入

import numpy as np
import mss
import cv2

def capture_screen(rect):
    """
    擷取指定矩形區域的螢幕畫面，並轉為 BGR 格式（OpenCV 用）。
    :param rect: {'top', 'left', 'width', 'height'} 擷取區域
    :return: numpy.ndarray (H, W, 3) BGR
    """
    with mss.mss() as sct:
        img = np.array(sct.grab(rect))  # BGRA 格式
        # 轉為 BGR（去除 alpha）
        bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return bgr 