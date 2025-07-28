# line_tracker.py
# 線段追蹤與淡出模組：平滑線段偵測結果，消除閃爍，支援淡出效果
# 用於 8BallPool_assist 的輔助線穩定顯示

import numpy as np
from config import config

class LineTracker:
    """
    線段追蹤器（支援淡出）：
    1. 記憶最近一次有效的線段列表及其 alpha（透明度）
    2. 若短暫失去偵測，會繼續輸出上一次結果，並讓 alpha 每幀遞減
    3. alpha<=0 時才真正消失
    """
    def __init__(self):
        self.tracked_lines = []  # 每項為 {'line': 線段, 'alpha': 透明度, 'lost': 失聯幀數}
        self.DEFAULT_ALPHA = config.LINE_ALPHA_DEFAULT  # 初始透明度
        self.FADE_STEP = config.LINE_FADE_STEP         # 每幀淡出速度

    def update(self, current_lines):
        """
        更新追蹤器：
        - 若本幀有有效線段，則刷新記憶，否則進行淡出
        - 新線段 alpha=預設值，舊線段失聯時 alpha 遞減
        :param current_lines: 本幀偵測到的線段列表
        """
        new_tracked = []
        if current_lines is not None and len(current_lines) > 0:
            # 用簡單的線段相等（可進階用相似度）
            for line in current_lines:
                found = False
                for tracked in self.tracked_lines:
                    if np.array_equal(line, tracked['line']):
                        # 線段還在，重設 alpha
                        new_tracked.append({'line': line, 'alpha': self.DEFAULT_ALPHA, 'lost': 0})
                        found = True
                        break
                if not found:
                    # 新線段
                    new_tracked.append({'line': line, 'alpha': self.DEFAULT_ALPHA, 'lost': 0})
            # 對於舊線段沒被偵測到的，進行淡出
            for tracked in self.tracked_lines:
                if not any(np.array_equal(tracked['line'], l) for l in current_lines):
                    alpha = tracked['alpha'] - self.FADE_STEP
                    if alpha > 0:
                        new_tracked.append({'line': tracked['line'], 'alpha': alpha, 'lost': tracked['lost']+1})
            self.tracked_lines = new_tracked
        else:
            # 沒有新線段，全部淡出
            for tracked in self.tracked_lines:
                alpha = tracked['alpha'] - self.FADE_STEP
                if alpha > 0:
                    new_tracked.append({'line': tracked['line'], 'alpha': alpha, 'lost': tracked['lost']+1})
            self.tracked_lines = new_tracked

    def get_stable_results(self):
        """
        取得平滑後的線段結果（含 alpha）：
        :return: [(線段, alpha)]
        """
        return [(t['line'], t['alpha']) for t in self.tracked_lines if t['alpha'] > 0] 