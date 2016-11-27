## tank-controller
### Python and Python-Flask apps for controlling aquaculture tank at Robot Garden

#### tank-controller is a Flask / Flask-socketio app that creates a website where one can observe various tank parameters like temperature, water level, etc. The web interface also features some control options like automated dosing and refilling. Messaging between apps is done via MQTT
- To install Flask:
- To install Flask-Socketio:
- To install Mosquitto MQTT broker:
- To install MQTT python library:

#### The apps in the component_controllers folder are intended to work in conjunction with tank-controller and must be running in the background in order for tank-controller to work.

- To ...
