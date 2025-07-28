# tuner.py
# 參數調整器 GUI：即時調整影像處理參數，預覽效果並儲存到 params_ransac.json
# 用於 8BallPool_assist 的參數微調與除錯

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import json
from capture import capture_screen
from config import config
from vision_core import VisionProcessor
from PIL import Image, ImageTk

PARAMS_FILE = 'params_ransac.json'

# === 預設參數（與 config.py 保持一致，僅供初始值） ===
def default_params():
    """
    回傳預設參數 dict，供參數檔缺漏時補齊
    """
    return {
        'bilateral_d': config.BILATERAL_D,
        'bilateral_sigmaColor': config.BILATERAL_SIGMA_COLOR,
        'bilateral_sigmaSpace': config.BILATERAL_SIGMA_SPACE,
        'canny_threshold1': config.CANNY_THRESHOLD1,
        'canny_threshold2': config.CANNY_THRESHOLD2,
        'hough_threshold': config.HOUGH_THRESHOLD,
        'hough_minLineLength': config.HOUGH_MIN_LINE_LENGTH,
        'hough_maxLineGap': config.HOUGH_MAX_LINE_GAP,
        'min_inliers': config.MIN_INLIERS,
        # 長線段 Hough 參數
        'hough_threshold_long': config.HOUGH_THRESHOLD_LONG,
        'hough_minLineLength_long': config.HOUGH_MIN_LINE_LENGTH_LONG,
        'hough_maxLineGap_long': config.HOUGH_MAX_LINE_GAP_LONG,
        # 短線段 Hough 參數
        'hough_threshold_short': config.HOUGH_THRESHOLD_SHORT,
        'hough_minLineLength_short': config.HOUGH_MIN_LINE_LENGTH_SHORT,
        'hough_maxLineGap_short': config.HOUGH_MAX_LINE_GAP_SHORT,
    }

# === 參數檔案存取 ===
def load_params():
    """
    讀取參數檔，若缺漏則補齊預設值
    """
    try:
        with open(PARAMS_FILE, 'r') as f:
            params = json.load(f)
            # 補齊新參數
            for k, v in default_params().items():
                if k not in params:
                    params[k] = v
            # 移除舊的顏色/粗細參數
            for k in list(params.keys()):
                if k.startswith('point_') or k.startswith('hough_line_'):
                    del params[k]
            return params
    except Exception:
        return default_params()

def save_params(params):
    """
    儲存參數到檔案
    """
    with open(PARAMS_FILE, 'w') as f:
        json.dump(params, f)

class TunerGUI:
    def __init__(self):
        self.params = load_params()
        self.vision_processor = VisionProcessor(config)
        self.PREVIEW_WIDTH = 350
        
        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("Tuner")
        self.root.geometry("800x430")
        
        # 建立變數
        self.vars = {}
        self.sliders = {}
        
        # 建立介面
        self.create_widgets()
        
        # 開始更新循環
        self.update_preview()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 參數框架（上半部分）
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=(0, 3))
        
        # 左側參數框架
        left_frame = ttk.Frame(param_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 右側參數框架
        right_frame = ttk.Frame(param_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 建立左側參數（Bilateral + Canny）
        self.create_left_params(left_frame)
        
        # 建立右側參數（Hough）
        self.create_right_params(right_frame)
        
        # 預覽框架（下半部分）
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(3, 0))
        
        # 預覽標籤（均分寬度，置中對齊）
        self.edges_label = ttk.Label(preview_frame, text="邊緣偵測", anchor="center")
        self.edges_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        
        self.debug_label = ttk.Label(preview_frame, text="偵測結果", anchor="center")
        self.debug_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
    def create_left_params(self, parent):
        # Bilateral 參數（左上）
        bilateral_frame = ttk.LabelFrame(parent, text="Bilateral Filter")
        bilateral_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 2))
        
        self.create_slider(bilateral_frame, "d", "bilateral_d", 1, 40)
        self.create_slider(bilateral_frame, "SigmaColor", "bilateral_sigmaColor", 1, 400)
        self.create_slider(bilateral_frame, "SigmaSpace", "bilateral_sigmaSpace", 1, 200)
        
        # Canny 參數（左下）
        canny_frame = ttk.LabelFrame(parent, text="Canny Edge")
        canny_frame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        
        self.create_slider(canny_frame, "T1", "canny_threshold1", 0, 1500)
        self.create_slider(canny_frame, "T2", "canny_threshold2", 0, 1500)
        self.create_slider(canny_frame, "min_inliers", "min_inliers", 1, 100)
    
    def create_right_params(self, parent):
        if not config.USE_DUAL_HOUGH:
            # 單一 Hough 參數
            hough_frame = ttk.LabelFrame(parent, text="Hough Transform")
            hough_frame.pack(fill=tk.BOTH, expand=True)
            
            self.create_slider(hough_frame, "Threshold", "hough_threshold", 1, 200)
            self.create_slider(hough_frame, "MinLineLength", "hough_minLineLength", 1, 200)
            self.create_slider(hough_frame, "MaxLineGap", "hough_maxLineGap", 1, 100)
        else:
            # 長線段 Hough 參數（右上）
            hough_long_frame = ttk.LabelFrame(parent, text="Hough Long")
            hough_long_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 2))
            
            self.create_slider(hough_long_frame, "Threshold", "hough_threshold_long", 1, 200)
            self.create_slider(hough_long_frame, "MinLineLen", "hough_minLineLength_long", 1, 200)
            self.create_slider(hough_long_frame, "MaxLineGap", "hough_maxLineGap_long", 1, 100)
            
            # 短線段 Hough 參數（右下）
            hough_short_frame = ttk.LabelFrame(parent, text="Hough Short")
            hough_short_frame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
            
            self.create_slider(hough_short_frame, "Threshold", "hough_threshold_short", 1, 200)
            self.create_slider(hough_short_frame, "MinLineLen", "hough_minLineLength_short", 1, 50)
            self.create_slider(hough_short_frame, "MaxLineGap", "hough_maxLineGap_short", 1, 100)
    
    def create_slider(self, parent, label, key, min_val, max_val):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=0)
        
        # 標籤（增加寬度避免文字被截斷）
        ttk.Label(frame, text=label, width=10).pack(side=tk.LEFT)
        
        # 變數
        var = tk.IntVar(value=self.params.get(key, min_val))
        self.vars[key] = var
        
        # 滑桿（適中長度）
        slider = ttk.Scale(frame, from_=min_val, to=max_val, variable=var, orient=tk.HORIZONTAL, length=200)
        slider.pack(side=tk.LEFT, padx=(5, 5))
        
        # 數值標籤（增加寬度）
        value_label = ttk.Label(frame, text=str(var.get()), width=5)
        value_label.pack(side=tk.RIGHT)
        
        # 綁定更新事件
        def update_value(*args):
            value_label.config(text=str(var.get()))
            self.update_params()
        
        var.trace('w', update_value)
        self.sliders[key] = slider
    
    def update_params(self):
        # 收集所有參數
        params = {}
        for key, var in self.vars.items():
            params[key] = var.get()
        
        # 儲存參數
        save_params(params)
        self.params = params
    
    def update_preview(self):
        try:
            # 擷取畫面
            frame = capture_screen(config.GAME_WINDOW_RECT)
            
            # 取得參數
            params = self.params.copy()
            
            # 影像處理
            if config.USE_DUAL_HOUGH:
                candidate_lines, points = self.vision_processor.get_features_dual_hough(frame, params)
            else:
                candidate_lines, points = self.vision_processor.get_features(frame, params)
            
            # 邊緣圖像重建
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            filtered = cv2.bilateralFilter(gray, params['bilateral_d'], params['bilateral_sigmaColor'], params['bilateral_sigmaSpace'])
            edges = cv2.Canny(filtered, params['canny_threshold1'], params['canny_threshold2'])
            
            # 偵測結果圖
            debug_view = frame.copy()
            
            # 畫點雲（綠色）
            for x, y in points:
                cv2.circle(debug_view, (int(x), int(y)), 1, (0,255,0), -1)
            
            # 畫 Hough 線段（藍色）
            if candidate_lines is not None:
                for line in candidate_lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(debug_view, (x1, y1), (x2, y2), (255,0,0), 1)
            
            # 縮小預覽（讓預覽圖填滿可用空間）
            h, w = debug_view.shape[:2]
            # 計算預覽區域的可用寬度（視窗寬度減去邊距）
            available_width = 800 - 20  # 視窗寬度減去左右邊距
            preview_width = available_width // 2 - 5  # 均分寬度，減去間距
            scale = preview_width / w
            new_size = (preview_width, int(h * scale))
            debug_view_small = cv2.resize(debug_view, new_size)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            edges_small = cv2.resize(edges_rgb, new_size)
            
            # 轉換為 PIL Image
            edges_pil = Image.fromarray(edges_small)
            debug_pil = Image.fromarray(cv2.cvtColor(debug_view_small, cv2.COLOR_BGR2RGB))
            
            # 轉換為 PhotoImage
            edges_photo = ImageTk.PhotoImage(edges_pil)
            debug_photo = ImageTk.PhotoImage(debug_pil)
            
            # 更新標籤
            self.edges_label.configure(image=edges_photo, text="")
            self.edges_label.image = edges_photo
            
            self.debug_label.configure(image=debug_photo, text="")
            self.debug_label.image = debug_photo
            
        except Exception as e:
            print(f"預覽更新錯誤: {e}")
        
        # 30ms 後再次更新
        self.root.after(30, self.update_preview)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TunerGUI()
    app.run() 