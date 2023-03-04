from flask import Flask, render_template, request, redirect
import threading
import time
import winsound

app = Flask(__name__)

class TimerThread(threading.Thread):
    def __init__(self, timer_length):
        super().__init__()
        self.timer_length = timer_length
        self.stop_event = threading.Event()

    def run(self):
        start_time = time.time()
        end_time = start_time + self.timer_length
        while time.time() < end_time and not self.stop_event.is_set():
            winsound.Beep(440, 1000) # plays a beep sound for 1 second at 440 Hz
            time.sleep(3) # sleep for 10 seconds // change for every human is detected
        if not self.stop_event.is_set():
            winsound.Beep(440, 1000) # plays a final beep sound
        self.stop_event.set()

    def stop(self):
        self.stop_event.set()

timer_thread = None

@app.route('/', methods=['GET', 'POST'])
def timer():
    global timer_thread
    if request.method == 'POST':
        timer_length = int(request.form['timer'])
        timer_thread = TimerThread(timer_length)
        timer_thread.start()
    return render_template('beep.html', timer_thread=timer_thread)

@app.route('/stop', methods=['POST'])
def stop_timer():
    global timer_thread
    if timer_thread and timer_thread.is_alive():
        timer_thread.stop()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
