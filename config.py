# config.py
# 全域設定檔，集中管理所有參數與魔法數字
# 用途：統一調整遊戲視窗座標、影像處理參數、輔助線繪製、檔案名稱等

import numpy as np

class Config:
    # === 遊戲視窗座標與大小 ===
    # 請依實際情況調整，指定要擷取的遊戲區域（像素座標）
    GAME_WINDOW_RECT = {
        'top': 133,
        'left': 143,
        'width': 383,
        'height': 188
    }

    # === HSV 顏色過濾參數 ===
    # 用於過濾白色輔助線，對光線和螢幕非常敏感，建議視情況微調
    HSV_WHITE_LOWER = np.array([0, 0, 200])
    HSV_WHITE_UPPER = np.array([180, 30, 255])

    # === 影像處理參數（預設值，會被 params_ransac.json 覆蓋） ===
    BILATERAL_D = 20                # 雙邊濾波 d
    BILATERAL_SIGMA_COLOR = 200     # 雙邊濾波 sigmaColor
    BILATERAL_SIGMA_SPACE = 1       # 雙邊濾波 sigmaSpace
    CANNY_THRESHOLD1 = 500          # Canny 邊緣偵測 threshold1
    CANNY_THRESHOLD2 = 350          # Canny 邊緣偵測 threshold2
    HOUGH_THRESHOLD = 20            # Hough 直線 threshold
    HOUGH_MIN_LINE_LENGTH = 1       # Hough 最小線段長度
    HOUGH_MAX_LINE_GAP = 1          # Hough 最大線段間隙
    MIN_INLIERS = 20                # 驗證線段的最小支持點數

    # === Hough 雙重偵測參數 ===
    # 長線段
    HOUGH_THRESHOLD_LONG = 20
    HOUGH_MIN_LINE_LENGTH_LONG = 20
    HOUGH_MAX_LINE_GAP_LONG = 1
    # 短線段
    HOUGH_THRESHOLD_SHORT = 5
    HOUGH_MIN_LINE_LENGTH_SHORT = 1
    HOUGH_MAX_LINE_GAP_SHORT = 1

    # === Hough 模式開關 ===
    USE_DUAL_HOUGH = True  # True: 雙重 Hough, False: 單一 Hough

    # === 輔助線繪製參數 ===
    LINE_ALPHA_DEFAULT = 40         # 輔助線初始透明度（0~255）
    LINE_FADE_STEP = 8              # 每幀淡出速度（數值越大淡出越快）
    LINE_WIDTH = 2                  # 輔助線寬度（像素）
    LINE_COLOR = (255, 255, 255)    # 輔助線顏色（純白）

    # === 參數檔案名稱 ===
    PARAMS_FILE = 'params_ransac.json'  # 供 utils.load_params 使用

    # === 其他開關 ===
    ENABLE_TUNER = True             # 是否自動啟動參數調整器

config = Config() 