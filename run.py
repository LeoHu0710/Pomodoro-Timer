import time
import tkinter as tk
from tkinter import messagebox
import threading

class PomodoroTimer:
    def __init__(self):
        self.is_running = False  # 記錄計時是否正在進行
        self.is_paused = False   # 記錄計時是否已暫停
        self.work_time = 0
        self.break_time = 0
        self.timer_thread = None
        self.current_mode = ""  # 記錄當前是工作還是休息模式
        self.remaining_time = 0  # 記錄剩餘時間

        # 建立視窗
        self.root = tk.Tk()
        self.root.title("番茄鐘")

        # 建立時間輸入區域
        self.label_work = tk.Label(self.root, text="請輸入工作時間（分鐘）：")
        self.label_work.pack(pady=5)
        
        self.work_time_entry = tk.Entry(self.root)
        self.work_time_entry.pack(pady=5)

        self.label_break = tk.Label(self.root, text="請輸入休息時間（分鐘）：")
        self.label_break.pack(pady=5)

        self.break_time_entry = tk.Entry(self.root)
        self.break_time_entry.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="開始", command=self.start)
        self.submit_button.pack(pady=10)

        # 增加暫停和繼續的按鈕
        self.pause_button = tk.Button(self.root, text="暫停", command=self.pause, state="disabled")
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(self.root, text="繼續", command=self.resume, state="disabled")
        self.resume_button.pack(pady=5)

        # 增加重製按鈕
        self.reset_button = tk.Button(self.root, text="重製", command=self.reset, state="disabled")
        self.reset_button.pack(pady=5)

        # 添加顯示當前狀態和倒數時間的標籤
        self.status_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, padx=20, pady=10)
        self.status_frame.pack(pady=10, fill=tk.X, padx=10)
        
        self.mode_label = tk.Label(self.status_frame, text="準備開始", font=("Arial", 12, "bold"))
        self.mode_label.pack()
        
        self.time_label = tk.Label(self.status_frame, text="00:00", font=("Arial", 36, "bold"))
        self.time_label.pack(pady=5)

        self.root.attributes("-topmost", True)  # 使視窗永遠在最上層

        # 處理視窗關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start(self):
        """啟動番茄鐘計時"""
        try:
            # 每次按下開始時都會讀取新的時間
            self.work_time = int(self.work_time_entry.get()) * 60  # 轉換為秒
            self.break_time = int(self.break_time_entry.get()) * 60  # 轉換為秒
            
            if self.work_time > 0 and self.break_time > 0:
                if self.is_running:
                    # 如果計時器已經在運行，則停止舊的計時
                    self.stop()

                self.is_running = True
                self.is_paused = False  # 確保當開始時不是暫停狀態

                # 鎖定輸入框，使其無法更改
                self.work_time_entry.config(state="disabled")
                self.break_time_entry.config(state="disabled")
                # 禁用開始按鈕，啟用暫停按鈕
                self.submit_button.config(state="disabled")
                self.pause_button.config(state="normal")
                self.reset_button.config(state="normal")  # 啟用重製按鈕
                
                self.timer_thread = threading.Thread(target=self.run_timer)
                self.timer_thread.daemon = True  # 設定為守護執行緒
                self.timer_thread.start()  # 啟動計時執行緒
            else:
                messagebox.showwarning("錯誤", "時間必須是正整數！")
        except ValueError:
            messagebox.showwarning("錯誤", "請輸入有效的數字！")

    def update_timer_display(self):
        """更新倒數計時顯示"""
        if self.is_running and not self.is_paused:
            minutes, seconds = divmod(self.remaining_time, 60)
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_string)
            
            # 更新模式顯示和背景顏色
            if self.current_mode == "work":
                self.mode_label.config(text="工作中", fg="red")
                self.status_frame.config(bg="#FFEEEE")  # 淡紅色背景
                self.time_label.config(bg="#FFEEEE")
                self.mode_label.config(bg="#FFEEEE")
            elif self.current_mode == "break":
                self.mode_label.config(text="休息中", fg="green")
                self.status_frame.config(bg="#EEFFEE")  # 淡綠色背景
                self.time_label.config(bg="#EEFFEE")
                self.mode_label.config(bg="#EEFFEE")
            
            # 每秒更新一次
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer_display)
            else:
                # 時間到，切換模式
                if self.current_mode == "work":
                    self.show_alert("時間到！休息一下吧！")
                    if self.is_running:
                        self.current_mode = "break"
                        self.remaining_time = self.break_time
                        self.update_timer_display()
                elif self.current_mode == "break":
                    self.show_alert("休息結束！繼續專注工作！")
                    if self.is_running:
                        self.current_mode = "work"
                        self.remaining_time = self.work_time
                        self.update_timer_display()

    def run_timer(self):
        """番茄鐘計時邏輯"""
        # 設定初始狀態
        self.current_mode = "work"
        self.remaining_time = self.work_time
        
        # 在主線程中更新UI
        self.root.after(0, self.update_timer_display)
        
        # 等待計時結束
        while self.is_running:
            time.sleep(0.5)  # 減少CPU使用率
            
        # 計時結束後啟用「開始」按鈕
        self.root.after(0, lambda: self.submit_button.config(state="normal"))

    def show_alert(self, message):
        """顯示提醒視窗，使用者按下確定後才繼續"""
        root = tk.Tk()
        root.withdraw()  # 隱藏主視窗
        messagebox.showinfo("番茄鐘提醒", message)
        root.destroy()  # 關閉視窗

    def pause(self):
        """暫停計時"""
        self.is_paused = True
        self.pause_button.config(state="disabled")  # 禁用暫停按鈕
        self.resume_button.config(state="normal")  # 啟用繼續按鈕
        self.mode_label.config(text="已暫停", fg="blue")
        self.status_frame.config(bg="#EEEEFF")  # 淡藍色背景
        self.time_label.config(bg="#EEEEFF")
        self.mode_label.config(bg="#EEEEFF")

    def resume(self):
        """繼續計時"""
        self.is_paused = False
        self.resume_button.config(state="disabled")  # 禁用繼續按鈕
        self.pause_button.config(state="normal")  # 啟用暫停按鈕
        
        # 恢復顯示當前模式
        if self.current_mode == "work":
            self.mode_label.config(text="工作中", fg="red")
        elif self.current_mode == "break":
            self.mode_label.config(text="休息中", fg="green")
            
        # 恢復計時器更新
        self.update_timer_display()

    def stop(self):
        """停止計時"""
        self.is_running = False  # 強制停止計時
        if self.timer_thread and self.timer_thread.is_alive():
            # 強制停止計時，避免 join() 時卡住
            self.timer_thread.join(timeout=0.1)  # 設置極短的超時時間，快速返回
        
        # 重置顯示
        self.mode_label.config(text="準備開始", fg="black")
        self.time_label.config(text="00:00")
        self.status_frame.config(bg="#F0F0F0")  # 預設背景色
        self.time_label.config(bg="#F0F0F0")
        self.mode_label.config(bg="#F0F0F0")
        
        # 禁用暫停和繼續按鈕
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="disabled")
        
        # 啟用輸入框
        self.work_time_entry.config(state="normal")
        self.break_time_entry.config(state="normal")

    def reset(self):
        """重製番茄鐘"""
        self.stop()
        self.work_time_entry.config(state="normal")
        self.break_time_entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.mode_label.config(text="準備開始", fg="black")
        self.time_label.config(text="00:00")
        self.status_frame.config(bg="#F0F0F0")
        self.time_label.config(bg="#F0F0F0")
        self.mode_label.config(bg="#F0F0F0")

    def on_close(self):
        """處理視窗關閉事件"""
        if messagebox.askokcancel("退出", "確定要退出嗎？"):
            self.is_running = False  # 強制停止計時
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=0.1)  # 設定極短的超時時間
            self.root.quit()  # 正確退出主循環
            self.root.destroy()  # 關閉視窗

    def run(self):
        """執行應用程式"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
