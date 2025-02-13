import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify, render_template

# Inisialisasi Flask
app = Flask(__name__)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
TRIG = 23    # [pin GPIO 23] Sesuaikan dengan koneksi Anda
ECHO = 24    # [pin GPIO 24] Pastikan ECHO melalui pembagi tegangan ke GPIO

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def ambil_data_jarak():
    # Pastikan trigger dalam keadaan LOW
    GPIO.output(TRIG, False)
    time.sleep(0.05)  # Delay untuk stabilisasi sensor

    # Kirim pulsa trigger HIGH selama 10 mikrodetik
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10μs
    GPIO.output(TRIG, False)

    # Catat waktu mulai
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Catat waktu tiba echo
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Hitung durasi pulsa
    pulse_duration = pulse_end - pulse_start

    # Hitung jarak (kecepatan suara = 34300 cm/s)
    distance = pulse_duration * 17150  # (34300/2)
    distance = round(distance, 2)
    return distance

@app.route('/')
def index():
    distance = ambil_data_jarak()
    return render_template('index.html', distance=distance)

@app.route('/api/distance')
def api_distance():
    distance = ambil_data_jarak()
    return jsonify({'distance': distance})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()

# https://bit.ly/hcsr04-code