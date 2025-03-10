# Pomodoro-Timer

這是一個簡單的番茄鐘應用程式，設計用來幫助使用者專注於工作或學習，並且遵循番茄工作法（Pomodoro Technique）。它會定時提醒使用者休息與繼續工作，提升工作效率。

### 功能

- 設定番茄鐘時間（默認 25 分鐘工作，5 分鐘休息）
- 顯示倒數計時
- 當番茄鐘結束時發出通知提醒

### 使用方式
1. 安裝所需的 Python 套件

2. 執行番茄鐘程式：
    ```
    python run.py
    ```

### 打包成執行檔 (可選)

若你希望將此番茄鐘應用打包成可執行檔（.exe 或其他格式），可以使用 `PyInstaller` 來完成這個過程。以下是簡單的打包教學：

#### 安裝 PyInstaller

首先，確保你已經安裝了 `PyInstaller`，如果還沒有，請執行以下指令來安裝：
```
pip install pyinstaller
```

執行以下指令來打包你的程式：
```
pyinstaller --onefile run.py
```
