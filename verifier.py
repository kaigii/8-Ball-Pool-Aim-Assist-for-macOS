# verifier.py
# 線段驗證模組：根據點雲支持度驗證 Hough 線段，篩選出最可靠的線段
# 用於 8BallPool_assist 的線段過濾與排序

import numpy as np

def verify_lines(candidate_lines, points, min_inliers=20):
    """
    用點雲支持度驗證 Hough 線段：
    1. 遍歷每條候選線段，計算點雲中有多少點「貼近」這條線段（距離 < 1.5 像素）
    2. 支持度高於 min_inliers 的線段才被視為有效
    3. 最後只取支持度最高的前三條線段
    :param candidate_lines: Hough 提案線段 (N,1,4)
    :param points: 邊緣點雲 (M,2)
    :param min_inliers: 最小支持點數
    :return: 最佳線段列表（每條格式同 Hough 輸出）
    """
    if candidate_lines is None or len(candidate_lines) == 0 or points is None or len(points) == 0:
        return []
    supported_lines = []
    for line in candidate_lines:
        x1, y1, x2, y2 = line[0]
        # 線段向量
        dx = x2 - x1
        dy = y2 - y1
        norm = np.hypot(dx, dy)
        if norm == 0:
            continue
        # 計算所有點到線段的最短距離
        px = points[:, 0]
        py = points[:, 1]
        # 投影參數 t (0<=t<=1在線段上)
        t = ((px - x1) * dx + (py - y1) * dy) / (norm ** 2)
        t = np.clip(t, 0, 1)
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        dists = np.hypot(px - proj_x, py - proj_y)
        inlier_count = np.sum(dists < 1.5)  # 支持點數
        if inlier_count > min_inliers:
            supported_lines.append((line, inlier_count))
    if not supported_lines:
        return []
    # 依支持度排序，取前三
    supported_lines.sort(key=lambda x: x[1], reverse=True)
    best_lines = [item[0] for item in supported_lines[:3]]
    return best_lines 