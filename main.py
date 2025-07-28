# main.py
# 8BallPool_assist 主程式入口
# 功能：擷取遊戲畫面、進行視覺分析、繪製輔助線於 overlay，並支援參數即時調整

import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from capture import capture_screen
from config import config
from vision_core import VisionProcessor
from overlay_window import OverlayWindow
import verifier
from line_tracker import LineTracker
from utils import load_params, extend_line_segment
import subprocess
import objc
from ctypes import c_void_p
from AppKit import NSApp


def main():
    """
    主程式入口：
    1. 初始化 QApplication、視覺處理器、Overlay 視窗、追蹤器
    2. 根據 config 決定是否啟動 tuner.py 參數調整器
    3. 啟動定時器，每 30ms 執行一次 main_loop_tick
    4. 設定 Overlay 為滑鼠穿透（macOS 專用）
    """
    # 啟動 tuner.py 作為子程序（非阻塞，僅當 ENABLE_TUNER 為 True）
    if config.ENABLE_TUNER:
        subprocess.Popen([sys.executable, 'tuner.py'])

    app = QApplication(sys.argv)
    vision_processor = VisionProcessor(config)
    overlay = OverlayWindow()
    overlay.update_geometry(config.GAME_WINDOW_RECT)
    overlay.setWindowFlags(
        Qt.FramelessWindowHint |
        Qt.WindowStaysOnTopHint
    )
    overlay.setAttribute(Qt.WA_TranslucentBackground)
    overlay.show()

    tracker = LineTracker()

    def main_loop_tick():
        """
        每一幀的主循環：
        1. 擷取遊戲區域畫面
        2. 讀取最新參數（支援即時調整）
        3. 提取 Hough 線段候選與點雲
        4. 用點雲驗證線段，篩選出最可靠的線段
        5. 用追蹤器平滑結果，消除偶發閃爍
        6. 將每條線段延伸到邊界，繪製到透明畫布上
        7. 更新 Overlay 視窗
        """
        params = load_params()  # 每一幀都即時讀取，支援 tuner.py 動態調整
        frame = capture_screen(config.GAME_WINDOW_RECT)
        if config.USE_DUAL_HOUGH:
            candidate_lines, points = vision_processor.get_features_dual_hough(frame, params)
        else:
            candidate_lines, points = vision_processor.get_features(frame, params)
        verified_lines = verifier.verify_lines(candidate_lines, points, min_inliers=params.get('min_inliers', config.MIN_INLIERS))
        tracker.update(verified_lines)
        stable_lines = tracker.get_stable_results()
        h, w = frame.shape[:2]
        overlay_image = np.zeros((h, w, 4), dtype=np.uint8)  # 透明畫布 (h, w, 4)
        bounds = {'left': 0, 'top': 0, 'width': w, 'height': h}
        # 根據 alpha 決定繪製方式：新線段延伸，淡出線段畫原始端點
        for line, alpha in stable_lines:
            if int(alpha) >= config.LINE_ALPHA_DEFAULT:
                # 剛偵測到，延伸到邊界
                end1, end2 = extend_line_segment(line, bounds)
                cv2.line(overlay_image, (int(end1[0]), int(end1[1])), (int(end2[0]), int(end2[1])), config.LINE_COLOR + (int(alpha),), config.LINE_WIDTH)
            else:
                # 淡出時，直接畫舊的線段端點
                if isinstance(line, np.ndarray) and line.shape == (4,):
                    x1, y1, x2, y2 = line
                elif isinstance(line, (list, np.ndarray)) and len(line) == 1 and len(line[0]) == 4:
                    x1, y1, x2, y2 = line[0]
                else:
                    x1, y1, x2, y2 = line
                cv2.line(overlay_image, (int(x1), int(y1)), (int(x2), int(y2)), config.LINE_COLOR + (int(alpha),), config.LINE_WIDTH)
        overlay.update_image(overlay_image)

    # 啟動主循環定時器（每 30ms 執行一次）
    timer = QTimer()
    timer.timeout.connect(main_loop_tick)
    timer.start(30)

    # 設定 Overlay 為滑鼠穿透（macOS 專用，讓滑鼠事件不被 overlay 攔截）
    winid = int(overlay.winId())
    ns_view = objc.objc_object(c_void_p=winid)
    ns_window = ns_view.window()
    ns_window.setIgnoresMouseEvents_(True)

    sys.exit(app.exec())

if __name__ == '__main__':
    main() 