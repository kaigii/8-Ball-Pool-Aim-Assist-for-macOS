# overlay_window.py
# 透明疊加視窗模組：負責將 OpenCV 影像以透明方式疊加在桌面上
# 用於 8BallPool_assist 的輔助線顯示

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap, QImage
import numpy as np
import cv2

class OverlayWindow(QWidget):
    """
    透明疊加視窗：
    1. 接收 OpenCV 影像（BGR 或 BGRA），轉為 QPixmap。
    2. 以透明方式繪製在桌面上方。
    """
    def __init__(self):
        super().__init__()
        self.pixmap_to_draw = None  # 當前要顯示的 QPixmap

    def paintEvent(self, event):
        """
        Qt paint 事件：將 pixmap 畫到視窗上。
        """
        painter = QPainter(self)
        if self.pixmap_to_draw is not None:
            painter.drawPixmap(self.rect(), self.pixmap_to_draw)

    def update_geometry(self, rect):
        """
        設定視窗位置與大小。
        :param rect: {'left', 'top', 'width', 'height'}
        """
        self.setGeometry(rect['left'], rect['top'], rect['width'], rect['height'])

    def update_image(self, frame):
        """
        接收 OpenCV 影像（BGR 或 BGRA），轉為 QPixmap 並觸發重繪。
        :param frame: numpy.ndarray (H, W, 3/4)
        """
        if frame is None:
            self.pixmap_to_draw = None
            self.update()
            return
        height, width, channel = frame.shape
        if channel == 4:
            # BGRA 轉 RGBA
            rgba_image = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            bytesPerLine = 4 * width
            q_image = QImage(rgba_image.data, width, height, bytesPerLine, QImage.Format_RGBA8888)
        elif channel == 3:
            # BGR 轉 RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bytesPerLine = 3 * width
            q_image = QImage(rgb_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        else:
            raise ValueError('Unsupported channel number for overlay image')
        pixmap = QPixmap.fromImage(q_image)
        self.pixmap_to_draw = pixmap
        self.update() 