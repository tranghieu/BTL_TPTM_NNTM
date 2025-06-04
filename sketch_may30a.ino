void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("📡 Hệ thống giám sát bắt đầu...");
}

void loop() {
  String timestamp = currentTime();

  float bpm = random(650, 1150) / 10.0;  // Giảm xác suất vượt ngưỡng
  float acc = random(10, 35) / 10.0;     // Gia tốc chỉ tối đa 3.4

  String status;
  if (bpm < 45 || bpm > 125) {
    status = "⚠️ Nhịp tim bất thường";
  } else if (acc > 3.3 && random(0, 100) < 30) {  // 30% khả năng cảnh báo nếu acc cao
    status = "⚠️ Té ngã nghi ngờ";
  } else if (random(0, 500) == 0) {
    status = "🔋 Pin yếu (giả lập)";
  } else {
    status = "✅ Ổn định";
  }

  Serial.println(timestamp + "," + String(bpm, 1) + "," + String(acc, 2) + "," + status);
  delay(1000);
}

String currentTime() {
  static int fake_second = 0;
  static int fake_minute = 0;

  fake_second++;
  if (fake_second >= 60) {
    fake_second = 0;
    fake_minute++;
    if (fake_minute >= 60) {
      fake_minute = 0;
    }
  }

  String mm = String(fake_minute);
  String ss = String(fake_second);
  if (mm.length() < 2) mm = "0" + mm;
  if (ss.length() < 2) ss = "0" + ss;

  return "2025-06-03 00:" + mm + ":" + ss;
}
