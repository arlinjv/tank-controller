## tank-controller
### Python and Python-Flask apps for controlling aquaculture tank at Robot Garden

#### tank-controller is a Flask / Flask-socketio app that creates a website where one can observe various tank parameters like temperature, water level, etc. The web interface also features some control options like automated dosing and refilling. Messaging between apps is done via MQTT.
- To install Flask:
  - $ sudo pip install Flask
- To install Flask-Socketio:
  - $ pip install flask-socketio
- To install Mosquitto MQTT broker (from http://hackaday.com/2016/05/09/minimal-mqtt-building-a-broker/):
  - $ curl -O http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
  - $ sudo apt-key add mosquitto-repo.gpg.key
  - $ rm mosquitto-repo.gpg.key
  - $ cd /etc/apt/sources.list.d/
  - $ sudo curl -O http://repo.mosquitto.org/debian/mosquitto-jessie.list
  - $ sudo apt-get update
  - $ sudo apt-get install mosquitto mosquitto-clients
- To install MQTT python library: 
  - $ pip install paho-mqtt

#### The apps in the component_controllers folder are intended to work in conjunction with tank-controller and must be running in the background in order for tank-controller to work.

- To ...
