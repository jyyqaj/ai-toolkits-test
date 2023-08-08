import os

from driver_preparation.download import web_driver_path, driver_name

basic_input_path = os.getcwd()
basic_input_path = basic_input_path.replace("\\", "/")
face = 'face'
draw = 'drawing'
music = 'music'
history = 'getHistory'
square = 'getSquare'
driver_path = web_driver_path + driver_name
