import serial
import time
import csv

# Твои настройки
COM_PORT = 'COM5'      # Твой порт
BAUD_RATE = 115200     # Скорость из Arduino
RECORD_TIME = 15       # Запишем 15 секунд для первого теста

print(f"Подключаюсь к {COM_PORT}...")

try:
    # Открываем порт
    ser = serial.Serial(COM_PORT, BAUD_RATE)
    print("Отлично, связь есть! Пишем кардиограмму...")
    
    # Создаем файл для сохранения
    with open('my_first_ecg.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "ECG_Value"]) # Заголовки столбцов
        
        start_time = time.time()
        
        # Собираем данные 15 секунд
        while (time.time() - start_time) < RECORD_TIME:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line.isdigit():
                    writer.writerow([time.time(), line])
                    
    print("Запись завершена! Файл my_first_ecg.csv сохранен рядом со скриптом.")
    
except Exception as e:
    print(f"Что-то пошло не так: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()