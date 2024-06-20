from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/livingroom/curtains')
def livingroom_curtains():
    print("Living Room Curtains Function")
    return redirect(url_for('index'))

@app.route('/livingroom/light')
def livingroom_light():
    return "Living Room Light Function"

@app.route('/livingroom/radiator')
def livingroom_radiator():
    return "Living Room Radiator Function"

@app.route('/greenhouse/watering')
def greenhouse_watering():
    return "Greenhouse Watering Function"

@app.route('/balcony/light')
def balcony_light():
    return "Balcony Light Function"

@app.route('/bedroom/light')
def bedroom_light():
    return "Bedroom Light Function"

@app.route('/bedroom/lightmusic')
def bedroom_lightmusic():
    return "Bedroom Light Music Function"

@app.route('/room/light')
def room_light():
    return "Room Light Function"

@app.route('/room/kettle')
def room_kettle():
    return "Room Kettle Function"

if __name__ == '__main__':
    app.run(debug=True)
