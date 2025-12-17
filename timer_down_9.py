import tkinter as tk
from datetime import datetime, timedelta
import pyttsx3
import os
import platform
#интерпретатор изменён на python 3.13.7
class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер обратного отсчета")
        
        # Устанавливаем размер окна (ширина x высота)
        self.root.geometry("600x400")
        
        # Инициализация движка для синтеза речи
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        
        # Установка голоса (если доступен русский)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'russian' in voice.languages:
                self.engine.setProperty('voice', voice.id)
                break
        
        # Установка начального времени
        self.time_left = timedelta(minutes=5)
        
        # Переменная для хранения состояния выключения
        self.shutdown_enabled = tk.BooleanVar(value=False)
        
        # Создание элементов интерфейса
        self.label = tk.Label(root, text=self.format_time(), font=('Helvetica', 36))
        self.label.pack(pady=20)
        
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=10)
        
        tk.Label(self.entry_frame, text="Часы:").pack(side=tk.LEFT)
        self.hours_entry = tk.Entry(self.entry_frame, width=5)
        self.hours_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.entry_frame, text="Минуты:").pack(side=tk.LEFT)
        self.minutes_entry = tk.Entry(self.entry_frame, width=5)
        self.minutes_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.entry_frame, text="Секунды:").pack(side=tk.LEFT)
        self.seconds_entry = tk.Entry(self.entry_frame, width=5)
        self.seconds_entry.pack(side=tk.LEFT, padx=5)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.button_frame, text="Старт", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.button_frame, text="Стоп", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(self.button_frame, text="Сброс", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Чекбокс для выключения компьютера
        self.shutdown_check = tk.Checkbutton(
            root, 
            text="Выключить компьютер после отсчёта",
            variable=self.shutdown_enabled,
            font=('Helvetica', 10)
        )
        self.shutdown_check.pack(pady=10)
        
        # Создаем отдельный стиль для сообщения о выключении
        self.shutdown_label = tk.Label(root, text="", font=('Helvetica', 14))
        self.shutdown_label.pack(pady=10)
        
        self.timer_running = False
    
    def format_time(self):
        """Форматирует время в формат HH:MM:SS"""
        total_seconds = int(self.time_left.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def speak(self, text):
        """Произносит переданный текст"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def shutdown_computer(self):
        """Выключает компьютер"""
        try:
            self.speak("Приятного вечера, Олег Васильевич! Выключаю компьютер.")
            # Используем отдельный label с меньшим шрифтом (16pt вместо 48pt)
            self.label.config(font=('Helvetica', 16))
            self.label.config(text="Приятного вечера, Олег Васильевич!\nВыключаю компьютер...")
            self.root.update()
            
            os_name = platform.system()
            
            if os_name == "Windows":
                os.system("shutdown /s /t 10")  # Выключение через 10 секунд
            elif os_name == "Linux" or os_name == "Darwin":
                os.system("shutdown -h +1")  # Выключение через 1 минуту
            else:
                self.speak("Неизвестная операционная система")
                self.shutdown_label.config(text="Ошибка: неизвестная ОС")
        except Exception as e:
            self.speak(f"Ошибка при выключении: {str(e)}")
            self.shutdown_label.config(text=f"Ошибка: {str(e)}")
    
    def update_timer(self):
        """Обновляет таймер каждую секунду"""
        if self.timer_running and self.time_left.total_seconds() > 0:
            self.time_left -= timedelta(seconds=1)
            self.label.config(text=self.format_time())
            self.root.after(1000, self.update_timer)
        elif self.time_left.total_seconds() <= 0:
            self.timer_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            # Произносим фразу
            self.speak("Заданное время таймера истекло. ")
            
            # Если включена опция выключения компьютера
            if self.shutdown_enabled.get():
                self.shutdown_computer()
            else:
                # Если выключение не требуется, просто показываем сообщение
                self.label.config(font=('Helvetica', 16))
                self.label.config(text="Завершено время обратного отсчёта.\n ....")
    
    def start_timer(self):
        """Запускает таймер"""
        try:
            # Восстанавливаем большой шрифт для таймера
            self.label.config(font=('Helvetica', 48))
            
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            seconds = int(self.seconds_entry.get() or 0)
            
            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError("Время не может быть отрицательным")
            
            self.time_left = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            self.label.config(text=self.format_time())
            
            if self.time_left.total_seconds() > 0:
                self.timer_running = True
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.update_timer()
        except ValueError as e:
            self.label.config(text=f"Ошибка: {str(e)}")
    
    def stop_timer(self):
        """Останавливает таймер"""
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        """Сбрасывает таймер"""
        self.stop_timer()
        self.time_left = timedelta(seconds=0)
        # Восстанавливаем большой шрифт для таймера
        self.label.config(font=('Helvetica', 48))
        self.label.config(text=self.format_time())
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.shutdown_label.config(text="")  # Очищаем сообщение о выключении
    
    def __del__(self):
        """Освобождает ресурсы движка синтеза речи"""
        self.engine.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()