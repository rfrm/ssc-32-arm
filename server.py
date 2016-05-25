import serial
from robot import Robot
from bottle import request, get, post, route, static_file, run

ser = serial.Serial('COM5', 115200)
r = Robot(ser, l1=6.3, l2=4, l3=20, l4=30.5, l5=9)

@get('/')
def root():
    return static_file('index.html', '.')

@get('/assets/<filename:path>')
def assets(filename):
    return static_file(filename, root='assets')

@post('/move')
def move():
    move_from = request.forms['from']
    move_to =   request.forms['to']
    piece = request.forms['piece']
    r.move_piece(piece, move_from, move_to)

@post('/capture')
def capture():
    move_from = request.forms['from']
    move_to =   request.forms['to']
    return "Hi"

run(debug=True)
