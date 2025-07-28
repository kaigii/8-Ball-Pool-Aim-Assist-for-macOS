# vision_core.py
# 視覺核心模組：負責從畫面中提取邊緣點雲與 Hough 線段候選
# 用於 8BallPool_assist 的主要影像處理流程

import cv2
import numpy as np

class VisionProcessor:
    """
    視覺核心：負責從畫面中提取點雲與 Hough 線段候選。
    """
    def __init__(self, config):
        """
        初始化，保存全域設定。
        :param config: 全域設定物件
        """
        self.config = config

    def get_features(self, frame, params):
        """
        從輸入畫面同時提取：
        1. 邊緣點雲（用於驗證）
        2. Hough 線段候選（用於提案）
        流程：
        a. 轉灰階
        b. 雙邊濾波（保留邊緣、去除雜訊）
        c. Canny 邊緣偵測
        d. 轉點雲
        e. HoughLinesP 提案
        :param frame: 輸入畫面 (BGR)
        :param params: 影像處理參數 dict
        :return: (candidate_lines, points)
        """
        # a. 轉灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # b. 雙邊濾波（可調參數，預設值見 config）
        d = params.get('bilateral_d', self.config.BILATERAL_D)
        sigmaColor = params.get('bilateral_sigmaColor', self.config.BILATERAL_SIGMA_COLOR)
        sigmaSpace = params.get('bilateral_sigmaSpace', self.config.BILATERAL_SIGMA_SPACE)
        filtered = cv2.bilateralFilter(gray, d, sigmaColor, sigmaSpace)
        # c. Canny 邊緣偵測
        threshold1 = params.get('canny_threshold1', self.config.CANNY_THRESHOLD1)
        threshold2 = params.get('canny_threshold2', self.config.CANNY_THRESHOLD2)
        edges = cv2.Canny(filtered, threshold1, threshold2)
        # d. 點雲轉換（邊緣像素座標）
        ys, xs = np.where(edges == 255)
        points = np.stack([xs, ys], axis=1) if len(xs) > 0 else np.empty((0, 2), dtype=np.int32)
        # e. Hough 直線提案
        hough_threshold = params.get('hough_threshold', self.config.HOUGH_THRESHOLD)
        min_line_length = params.get('hough_minLineLength', self.config.HOUGH_MIN_LINE_LENGTH)
        max_line_gap = params.get('hough_maxLineGap', self.config.HOUGH_MAX_LINE_GAP)
        candidate_lines = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=hough_threshold,
            minLineLength=min_line_length,
            maxLineGap=max_line_gap
        )
        # 返回 Hough 線段與點雲
        return candidate_lines, points

    def get_features_dual_hough(self, frame, params):
        """
        進階：雙重 Hough 偵測，分別針對長線段與短線段
        :param frame: 輸入畫面 (BGR)
        :param params: 影像處理參數 dict
        :return: (candidate_lines, points)
        """
        # a. 轉灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # b. 雙邊濾波
        d = params.get('bilateral_d', self.config.BILATERAL_D)
        sigmaColor = params.get('bilateral_sigmaColor', self.config.BILATERAL_SIGMA_COLOR)
        sigmaSpace = params.get('bilateral_sigmaSpace', self.config.BILATERAL_SIGMA_SPACE)
        filtered = cv2.bilateralFilter(gray, d, sigmaColor, sigmaSpace)
        # c. Canny 邊緣偵測
        threshold1 = params.get('canny_threshold1', self.config.CANNY_THRESHOLD1)
        threshold2 = params.get('canny_threshold2', self.config.CANNY_THRESHOLD2)
        edges = cv2.Canny(filtered, threshold1, threshold2)
        # d. 點雲轉換
        ys, xs = np.where(edges == 255)
        points = np.stack([xs, ys], axis=1) if len(xs) > 0 else np.empty((0, 2), dtype=np.int32)
        # e1. Hough 長線段
        hough_threshold_long = params.get('hough_threshold_long', self.config.HOUGH_THRESHOLD)
        min_line_length_long = params.get('hough_minLineLength_long', max(20, self.config.HOUGH_MIN_LINE_LENGTH))
        max_line_gap_long = params.get('hough_maxLineGap_long', self.config.HOUGH_MAX_LINE_GAP)
        lines_long = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=hough_threshold_long,
            minLineLength=min_line_length_long,
            maxLineGap=max_line_gap_long
        )
        # e2. Hough 短線段
        hough_threshold_short = params.get('hough_threshold_short', max(1, self.config.HOUGH_THRESHOLD // 2))
        min_line_length_short = params.get('hough_minLineLength_short', 1)
        max_line_gap_short = params.get('hough_maxLineGap_short', self.config.HOUGH_MAX_LINE_GAP)
        lines_short = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            threshold=hough_threshold_short,
            minLineLength=min_line_length_short,
            maxLineGap=max_line_gap_short
        )
        # 合併去重
        all_lines = []
        seen = set()
        for group in [lines_long, lines_short]:
            if group is not None:
                for line in group:
                    key = tuple(line[0])
                    if key not in seen:
                        all_lines.append(line)
                        seen.add(key)
        candidate_lines = np.array(all_lines) if all_lines else None
        return candidate_lines, points 