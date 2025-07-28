<div align="center">

# 8-Ball-Pool-Aim-Assist-for-macOS

[English](README.md)


![alt text](https://img.shields.io/badge/macOS-12.0%2B-blue)
![alt text](https://img.shields.io/badge/Python-3.9%2B-green)
![alt text](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

**這是一個專為在 macOS 上遊玩 8 Ball Pool 設計的輔助瞄準工具。它透過電腦視覺技術，即時分析遊戲畫面中的白色輔助線，並繪製一條延伸的、穩定的預測路徑，幫助玩家更精準地判斷球的走向。**

</div>

## 📸 運作預覽

<div align="center">

**遊戲畫面與輔助線疊加效果：**
<img width="700" alt="遊戲畫面與輔助線疊加效果" src="https://github.com/user-attachments/assets/235f035f-c62a-4296-b3be-0e59e63aa2ff" />

**即時參數調整器 (Tuner)：**
<img width="700" alt="即時參數調整器" src="https://github.com/user-attachments/assets/2466d522-b804-441a-806f-cc8960a21d72" />

</div>
透過直觀的 GUI 介面，您可以即時調整所有影像處理參數，找到在您螢幕上的最佳設定。

## ✨ 功能特色

- **即時畫面分析**：擷取指定的遊戲區域，毫秒級處理。
- **進階影像處理**：採用雙邊濾波、Canny 邊緣偵測等演算法，精準提取線條特徵。
- **雙重霍夫變換 (Dual Hough Transform)**：分別針對長、短線段進行偵測，提高在不同視角下的偵測率。
- **點雲驗證機制**：利用 RANSAC 思想，透過邊緣點雲的支持度來驗證和篩選最可靠的線段，排除雜訊干擾。
- **平滑線段追蹤**：獨家的 LineTracker 模組，能消除線條的短暫閃爍，並提供優雅的淡出 (Fade-out) 效果。
- **無干擾懸浮視窗**：使用 PySide6 建立的透明懸浮視窗，可疊加在遊戲之上，且完全穿透滑鼠事件，不影響遊戲操作。
- **即時參數調整器**：內建一個強大的 GUI 調參工具 (tuner.py)，讓你可以即時微調所有視覺處理參數，並立即看到效果。

## 🚀 開始使用

### 安裝需求 (Prerequisites)
請確保您的 Mac 上已安裝 Python 3.9 或更高版本。

### 安裝步驟

#### 1. 複製專案
```bash
git clone https://github.com/kaigii/8-Ball-Pool-Aim-Assist-for-macOS.git
cd 8-Ball-Pool-Aim-Assist-for-macOS
```

#### 2. 安裝依賴套件
建議在虛擬環境中進行安裝：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🎮 使用方法

### 1. 將遊戲畫面投射到 Mac
使用 macOS 內建的「iPhone 鏡像輸出」功能，或任何其他螢幕鏡像 App，將您的手機遊戲畫面完整投射到 Mac 桌面上。

### 2. 設定撞球桌擷取範圍
這是最關鍵的步驟！您需要手動指定程式要分析的區域。

1. 在 Mac 上按下 `Command + Shift + 4`，此時游標會變成一個十字，並顯示當前座標。
2. 將滑鼠移動到遊戲視窗中撞球桌範圍的左上角，記下 x 和 y 座標。
3. 拖曳滑鼠到右下角，計算出矩形的 **寬度** 和 **高度**。
4. 打開專案中的 `config.py` 檔案，修改 `GAME_WINDOW_RECT` 字典中的值。

### 3. 執行主程式
一切就緒後，在終端機中執行：
```bash
python3 main.py
```

程式會啟動一個透明的懸浮視窗，並自動打開參數調整器 Tuner。此時，您應該能在遊戲畫面上看到偵測到的輔助線。

## 🛠️ 參數設定與微調

本專案的核心設定分為兩部分：`config.py` 檔案用於設定基礎行為與外觀，Tuner 介面則用於微調影像辨識的精確度。

### config.py 檔案設定
這個檔案控制著程式的核心行為和輔助線的視覺樣式。

- **GAME_WINDOW_RECT**:
  - 用途：定義螢幕擷取的範圍。
  - 調整方式：如「使用方法」所述，利用 Command+Shift+4 測量並填入遊戲中撞球桌的實際像素座標和大小。

- **HSV_WHITE_LOWER / HSV_WHITE_UPPER**:
  - 用途：定義程式要辨識的「白色」範圍。這對過濾出遊戲的輔助線至關重要。
  - 調整方式：如果線條辨識不佳，可以微調這些值。通常 `[0, 0, 200]` 到 `[180, 30, 255]` 的範圍適用於大多數情況。

- **USE_DUAL_HOUGH**:
  - 用途：切換線條偵測模式。True 表示同時使用長、短兩種線段偵測器，能適應更多情況；False 則只使用單一偵測器。
  - 調整方式：保持 True 通常效果最好。

- **LINE_ALPHA_DEFAULT**:
  - 用途：新偵測到的輔助線的初始不透明度 (0-255)。
  - 調整方式：數值越高，線條越實。40 是一個比較柔和的初始值。

- **LINE_FADE_STEP**:
  - 用途：當線條消失時，每幀減少的不透明度。
  - 調整方式：數值越大，線條消失得越快。8 能提供一個平滑的淡出效果。

- **LINE_WIDTH / LINE_COLOR**:
  - 用途：控制輔助線的寬度（像素）和顏色（RGB）。
  - 調整方式：依個人喜好調整。

- **ENABLE_TUNER**:
  - 用途：決定是否在啟動主程式時自動打開 Tuner 調整視窗。
  - 調整方式：當您找到滿意的參數後，可將此設為 False，這樣執行時會更簡潔。

### Tuner 即時參數調整
執行 `main.py` 時，Tuner 視窗會自動打開，讓您透過滑桿即時調整影像處理參數，並立刻在預覽視窗中看到結果。您的所有調整都會自動儲存到 `params_ransac.json` 檔案中。

**預覽視窗的目標：**
- **左側 (邊緣偵測)**：理想的結果是，這個視窗應該是全黑的，只剩下清晰、乾淨的白色輔助線條。桌面上的其他圖案（如小鹿）應該被完全過濾掉。
- **右側 (偵測結果)**：綠色的「點雲」應該密集地分佈在白色輔助線上，而藍色的「霍夫線段」應該與輔助線完美重合。

**滑桿功能：**
- **Bilateral Filter**：影像平滑濾鏡。通常保持較小值即可，用於去除輕微的影像雜訊。
- **Canny Edge**：邊緣偵測的關鍵。
  - **T1 和 T2**：控制敏感度。調整這兩個值，直到左側預覽視窗中的雜訊最少，線條最清晰。
- **min_inliers**：一條線需要多少個綠色點雲支持才能被認定為有效。適當提高此值可以過濾掉錯誤的短線條。
- **Hough Long / Hough Short**：控制線段偵測的演算法。
  - **Threshold**：偵測閾值，越高要求越嚴格。
  - **MinLineLen**：最短被接受的線段長度。
  - **MaxLineGap**：線段上點與點之間允許的最大間隙。

## 📄 授權條款 (License)

本專案採用 **創用 CC 姓名標示-非商業性-相同方式分享 4.0 國際 (CC BY-NC-SA 4.0)** 授權條款。

這意味著您可以自由地：
- **分享** — 以任何媒介或格式重製及散布本專案。
- **修改** — 重混、變更、及依本專案建立新作品。

惟需遵守下列條件：
- **姓名標示 (Attribution)** — 您必須給予適當的姓名標示，提供指向本授權條款的連結，以及指出是否（對原始作品）進行了變更。
- **非商業性 (NonCommercial)** — 您不得將本專案用於商業目的。
- **相同方式分享 (ShareAlike)** — 如果您重混、轉換、或依本專案建立新作品，您必須基於與原先完全相同的授權條款來散布您的貢獻。

詳細的授權條款全文，請參閱 [Creative Commons 網站](https://creativecommons.org/licenses/by-nc-sa/4.0/)。

## ❤️ 貢獻 (Contributing)

歡迎貢獻！無論是回報錯誤、建議功能，還是提交 Pull Request，您的幫助都受到歡迎。

1. Fork 這個專案
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

 