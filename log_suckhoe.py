import serial
import csv
import time
import smtplib
from email.message import EmailMessage

# Thông tin serial
COM_PORT = 'COM3'
BAUD_RATE = 115200
CSV_FILE = r'G:\My Drive\suckhoe.csv'
WRITE_INTERVAL = 180  # mỗi 3 phút

# Thông tin email
EMAIL_SEND = 'hieuta2606@gmail.com'  # Gmail gửi đi
EMAIL_PASSWORD = 'evbt mczq vzow ckbd'  # App password
EMAIL_TO = 'tranghieu0626@gmail.com'  # Người nhận

def gui_email(thongbao):
    msg = EmailMessage()
    msg.set_content(thongbao)
    msg['Subject'] = '⚠️ Cảnh báo sức khỏe từ hệ thống'
    msg['From'] = EMAIL_SEND
    msg['To'] = EMAIL_TO

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SEND, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("📧 Đã gửi email cảnh báo!")

def parse_data(line):
    try:
        parts = line.strip().split(',')
        if len(parts) == 4:
            return parts  # [timestamp, bpm, acc, status]
    except:
        return None
    return None

def main():
    print("🔌 Đang kết nối với Arduino...")
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=10)
    print("✅ Đã kết nối với", COM_PORT)

    # Ghi tiêu đề nếu file mới
    try:
        with open(CSV_FILE, mode='x', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Thời gian', 'Nhịp tim', 'Gia tốc', 'Trạng thái'])
            print("📄 Đã tạo file CSV và thêm tiêu đề.")
    except FileExistsError:
        print("📄 File CSV đã tồn tại.")

    last_write_time = time.time()
    latest_data = None

    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            data = parse_data(line)

            if data:
                latest_data = data
                print("📥 Nhận:", data)

                # Nếu phát hiện trạng thái bất thường
                if '⚠️' in data[3]:
                    gui_email(
                        f"Cảnh báo lúc {data[0]}:\n→ Trạng thái: {data[3]}\n→ Nhịp tim: {data[1]}\n→ Gia tốc: {data[2]}"
                    )

        # Ghi file mỗi 3 phút
        current_time = time.time()
        if latest_data and (current_time - last_write_time) >= WRITE_INTERVAL:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(latest_data)
                print(f"📝 Ghi vào CSV lúc {latest_data[0]}")
            last_write_time = current_time

        time.sleep(0.5)

if __name__ == '__main__':
    main()
