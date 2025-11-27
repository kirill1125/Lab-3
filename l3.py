import tkinter as tk
from tkinter import messagebox
import random
import string
import winsound
import threading
import time

class KeyGenerator:
    def __init__(self):
        self.charset = string.ascii_uppercase + string.digits
        
    def shift_right(self, text, shift):
        result = []
        for char in text:
            if char in self.charset:
                idx = self.charset.index(char)
                new_idx = (idx + shift) % len(self.charset)
                result.append(self.charset[new_idx])
            else:
                result.append(char)
        return ''.join(result)
    
    def shift_left(self, text, shift):
        result = []
        for char in text:
            if char in self.charset:
                idx = self.charset.index(char)
                new_idx = (idx - shift) % len(self.charset)
                result.append(self.charset[new_idx])
            else:
                result.append(char)
        return ''.join(result)
    
    def generate_key(self, first_block):
        if len(first_block) != 5:
            raise ValueError("Нужно 5 символов")
        if not all(c in self.charset for c in first_block):
            raise ValueError("Только A-Z и 0-9")
        
        second_block = self.shift_right(first_block, 3)
        third_block = self.shift_left(first_block, 5)
        
        return f"{first_block}-{second_block}-{third_block}"

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        
    def play_music(self):
        def music_loop():
            notes = [440, 523, 659, 784]
            while self.is_playing:
                for freq in notes:
                    if not self.is_playing:
                        break
                    try:
                        winsound.Beep(freq, 300)
                    except:
                        pass
                    time.sleep(0.1)
                time.sleep(0.3)
        
        self.is_playing = True
        thread = threading.Thread(target=music_loop)
        thread.daemon = True
        thread.start()
    
    def stop_music(self):
        self.is_playing = False
    
    def toggle_music(self):
        if self.is_playing:
            self.stop_music()
            return False
        else:
            self.play_music()
            return True

# Создаем окно
window = tk.Tk()
window.title('Key Generator')
window.geometry('500x400')

# Загружаем GIF фон
try:
    bg_image = tk.PhotoImage(file='gradient.gif')
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    print("GIF фон загружен!")
except Exception as e:
    print(f"GIF не загружена: {e}")
    window.configure(bg='#2C3E50')

# Создаем генератор и проигрыватель
generator = KeyGenerator()
music_player = MusicPlayer()

# Функции
def generate_key():
    text = entry.get().upper()
    if len(text) != 5:
        messagebox.showwarning('Ошибка', 'Введите 5 символов A-Z, 0-9')
        return
    
    try:
        key = generator.generate_key(text)
        result_label.config(text=key)
        status_label.config(text='Ключ создан!')
        flash_animation()
        play_sound_effect()
        show_hex_info(text)
    except Exception as e:
        messagebox.showerror('Ошибка', str(e))

def random_input():
    chars = string.ascii_uppercase + string.digits
    random_text = ''.join(random.choice(chars) for _ in range(5))
    entry.delete(0, tk.END)
    entry.insert(0, random_text)
    status_label.config(text='Случайный блок создан')
    play_random_sound()

def validate_input(event=None):
    text = entry.get().upper()
    filtered = ''.join(c for c in text if c in generator.charset)
    if len(filtered) > 5:
        filtered = filtered[:5]
    
    if entry.get() != filtered:
        entry.delete(0, tk.END)
        entry.insert(0, filtered)
    
    if len(filtered) == 5:
        status_label.config(text='Готов к генерации')
    else:
        status_label.config(text=f'Символов: {len(filtered)}/5')

def flash_animation():
    colors = ['red', 'yellow', 'green', 'yellow', 'red', 'orange']
    for i, color in enumerate(colors):
        window.after(i * 100, lambda c=color: result_label.config(fg=c))
    window.after(600, lambda: result_label.config(fg='orange'))

def play_sound_effect():
    def play():
        try:
            winsound.Beep(800, 100)
            winsound.Beep(1000, 100)
            winsound.Beep(1200, 150)
        except:
            pass
    threading.Thread(target=play, daemon=True).start()

def play_random_sound():
    def play():
        try:
            winsound.Beep(600, 50)
            winsound.Beep(800, 100)
        except:
            pass
    threading.Thread(target=play, daemon=True).start()

def show_hex_info(text):
    hex_vals = []
    dec_vals = []
    for char in text:
        if char in '0123456789':
            hex_val = hex(int(char))[2:].upper()
            dec_val = str(int(char))
        else:
            hex_val = hex(ord(char))[2:].upper()
            dec_val = str(ord(char))
        hex_vals.append(hex_val)
        dec_vals.append(dec_val)
    
    info = f"HEX: {' '.join(hex_vals)} | DEC: {' '.join(dec_vals)}"
    hex_label.config(text=info)

def toggle_music():
    if music_player.toggle_music():
        music_btn.config(text='🔊 Выкл звук', bg='#006600')
    else:
        music_btn.config(text='🔇 Вкл звук', bg='#330033')

def cancel():
    music_player.stop_music()
    window.destroy()

# Основной интерфейс
main_frame = tk.Frame(window, bg='#1A1A1A', bd=3, relief='raised')
main_frame.place(relx=0.5, rely=0.5, anchor='center', width=450, height=300)

# Заголовок
title_label = tk.Label(main_frame, text='ГЕНЕРАТОР КЛЮЧЕЙ', 
                      font=('Arial', 16, 'bold'), 
                      bg='#1A1A1A', fg='white')
title_label.pack(pady=10)

# Поле ввода
input_frame = tk.Frame(main_frame, bg='#1A1A1A')
input_frame.pack(pady=10)

tk.Label(input_frame, text='Первый блок (5 символов A-Z, 0-9):', 
         font=('Arial', 10), bg='#1A1A1A', fg='white').pack()

entry_frame = tk.Frame(input_frame, bg='#1A1A1A')
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, width=10, font=('Consolas', 14), 
                justify='center', bg='#2A2A2A', fg='white')
entry.insert(0, 'JINOS')
entry.pack(side='left', padx=5)
entry.bind('<KeyRelease>', validate_input)

tk.Button(entry_frame, text='Случайный', command=random_input,
          bg='#003366', fg='white', font=('Arial', 8)).pack(side='left', padx=5)

# Кнопки управления
buttons_frame = tk.Frame(main_frame, bg='#1A1A1A')
buttons_frame.pack(pady=15)

tk.Button(buttons_frame, text='СГЕНЕРИРОВАТЬ', command=generate_key,
          bg='#006600', fg='white', font=('Arial', 10, 'bold'),
          width=15).pack(side='left', padx=5)

music_btn = tk.Button(buttons_frame, text='Вкл звук', command=toggle_music,
                     bg='#330033', fg='white', font=('Arial', 10, 'bold'),
                     width=10)
music_btn.pack(side='left', padx=5)

tk.Button(buttons_frame, text='ВЫХОД', command=cancel,
          bg='#660000', fg='white', font=('Arial', 10, 'bold'),
          width=10).pack(side='left', padx=5)

# Результат
result_frame = tk.Frame(main_frame, bg='#1A1A1A')
result_frame.pack(pady=10)

result_label = tk.Label(result_frame, text='XXXXX-XXXXX-XXXXX', 
                       font=('Consolas', 12, 'bold'), 
                       bg='#1A1A1A', fg='orange')
result_label.pack()

hex_label = tk.Label(result_frame, text='HEX: - | DEC: -', 
                    font=('Courier', 8), bg='#1A1A1A', fg='#888888')
hex_label.pack()

# Статус
status_label = tk.Label(window, text='Введите 5 символов A-Z, 0-9', 
                       font=('Arial', 9), bg='#1A1A1A', fg='#CCCCCC')
status_label.place(relx=0.5, rely=0.95, anchor='center')

# Запускаем окно
window.mainloop()