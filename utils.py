# utils.py
# 輔助工具模組：參數讀取、線段延伸等常用函式
# 用於 8BallPool_assist 的主程式與調參器

import json
import numpy as np
from config import config

def load_params():
    """
    從 config.PARAMS_FILE 讀取參數檔（JSON 格式），若失敗則回傳預設值。
    用於調參器與主程式同步參數。
    :return: dict 參數
    """
    try:
        with open(config.PARAMS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        # 回傳預設值（與 config.py 保持一致）
        return {
            'bilateral_d': config.BILATERAL_D,
            'bilateral_sigmaColor': config.BILATERAL_SIGMA_COLOR,
            'bilateral_sigmaSpace': config.BILATERAL_SIGMA_SPACE,
            'canny_threshold1': config.CANNY_THRESHOLD1,
            'canny_threshold2': config.CANNY_THRESHOLD2,
            'hough_threshold': config.HOUGH_THRESHOLD,
            'hough_minLineLength': config.HOUGH_MIN_LINE_LENGTH,
            'hough_maxLineGap': config.HOUGH_MAX_LINE_GAP,
            'min_inliers': config.MIN_INLIERS
        }

def extend_line_segment(line, bounds):
    """
    將一條 Hough 線段延伸為穿越整個畫面邊界的直線段。
    1. 以直線方程計算與四個邊界的交點。
    2. 篩選出落在畫面內的交點。
    3. 選出距離原始端點最遠的兩個作為延伸端點。
    4. 若無法延伸則回傳原始端點。
    :param line: Hough 線段 [x1, y1, x2, y2] 或 [[x1, y1, x2, y2]]
    :param bounds: 畫布邊界 dict（含 width, height）
    :return: ((x1, y1), (x2, y2)) 延伸後的兩端點
    """
    # 支援 line 為 [x1, y1, x2, y2] 或 [[x1, y1, x2, y2]]
    if isinstance(line, np.ndarray) and line.shape == (4,):
        x1, y1, x2, y2 = line
    elif isinstance(line, (list, np.ndarray)) and len(line) == 1 and len(line[0]) == 4:
        x1, y1, x2, y2 = line[0]
    else:
        x1, y1, x2, y2 = line  # fallback
    width = bounds['width']
    height = bounds['height']
    points = []
    # 垂直線
    if x1 == x2:
        points.append((x1, 0))
        points.append((x1, height))
    # 水平線
    elif y1 == y2:
        points.append((0, y1))
        points.append((width, y1))
    # 一般情況
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        # 與 x=0
        y_at_x0 = c
        if 0 <= y_at_x0 <= height:
            points.append((0, int(round(y_at_x0))))
        # 與 x=width
        y_at_xw = m * width + c
        if 0 <= y_at_xw <= height:
            points.append((width, int(round(y_at_xw))))
        # 與 y=0
        if m != 0:
            x_at_y0 = -c / m
            if 0 <= x_at_y0 <= width:
                points.append((int(round(x_at_y0)), 0))
        # 與 y=height
        if m != 0:
            x_at_yh = (height - c) / m
            if 0 <= x_at_yh <= width:
                points.append((int(round(x_at_yh)), height))
    # 篩選唯一點
    points = list(set(points))
    # 若交點超過2個，選距離原始線段中心最遠的兩個
    if len(points) > 2:
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        points.sort(key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2, reverse=True)
        return points[0], points[1]
    elif len(points) == 2:
        return points[0], points[1]
    else:
        return (x1, y1), (x2, y2) 