#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background thread

if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
import paho.mqtt.client as mqtt
from threading import Thread
from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!' #Seems to be needed for using session: http://flask.pocoo.org/docs/0.10/api/#sessions
socketio = SocketIO(app, async_mode=async_mode)
thread = None

#Tank Monitor:
#   - Basic concept: Webpage to display all tank related data. Works off of mqtt status messages
#       - First step: implement tank monitor and filler
#           - Flask (flask-socketio):
#               - Listen for MQTT messages
#               - Display 
#           - Client (javascript / socketio):
#               - display current tank level
#               - work with user to dose and fill tank
#               - display list of most recent messages
#           - Python on Raspberry Pi
#               - have app running as service to constantly monitor water level
#               
#   - Todo: 
#       - move received log to window like in emonhub example
#       - review imports and delete unused
#       - install gevent and check for websockets activity
#       - limit to one user at a time (probably need to have a login page)
#       - Consider copying layout from here: 
#           - https://github.com/emoncms/development/tree/master/Tutorials/Python/socketiowebconsole
#               - Especially the log window - might be cool to have a window that displays all mqtt activity
#               - also like sidebar menu
#               - use of MQTT_Thread class for background thread looks useful
#   - Progress:
#       - copied over from alarm_monitor
#       - updated page to show tank level at top
#   - Next steps:
#       1. implement controls for filling tank
#       2. create interactive filling and dosing protocol
#           - webpage will prompt user: add x millileters. have you added treatment? yes. shall I fill? yes. 
#   - By the way ...
#       - consider experimenting with vitamin C for chloramine removal - https://sites.google.com/site/brunwater/water-knowledge
#       - (activated filter probably not worth considering as it is less effective for chloramine)

    

@app.route("/test")
def test():
    # see :
    # http://flask.pocoo.org/docs/0.10/reqcontext/
    # http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    # http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.MultiDict
    if 'reload' in request.args.values()[0]: #for testing 
        print('issuing reload signal')
        socketio.emit('reload_page')
    print "query_string: ", request.query_string
    print "args: ", request.args.items()
    print "keys: ", request.args.keys()
    print "values: ", request.args.listvalues() # there is also a values() method
    print "args as a dict: ", request.args.to_dict()
    print "remote address: ", request.remote_addr 
    #print "request.event", request.event.keys()
    return jsonify({'ip': request.remote_addr, "args: ": request.args.items()}), 200

'''
def mqtt_receiver():
    count=0;
    while True:
        time.sleep(5)
        count += 1
        print "emitting..."
        socketio.emit('tank_level',{'data': 'tank level', 'count': count}, namespace='/tank') 
'''
def mqtt_receiver():
    
    print "launching mqtt_receiver ..."
    while True: # probably don't need  'while True' loop when using client.loop_forever()
        def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
        
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("#")
        
        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload))
            socketio.emit('mqtt_event',{'topic': msg.topic, 'data': msg.payload}, namespace='/tank') 
        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        client.connect("localhost", 1883, 60) #connect blocks until socket connection made, then asynchronous
        
        client.loop_forever()

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=mqtt_receiver)
        thread.start()
    return render_template('level_control.html')
    
@app.route('/mqtt_monitor')
def mqtt_monitor():
    global thread
    if thread is None:
        thread = Thread(target=mqtt_receiver)
        thread.start()
    return render_template('mqtt_monitor.html')


@socketio.on('connection event')
def handleConnectionEvent(message):
    print "connection event: ", message

@app.route("/debug") 
def debug():
    raise Exception('Nothing to see here. Move along') #used for debugging in browser - click on little console logo at the right
    '''Then you can do cool stuff like:
        >>> cur = g.db.execute('select device_ID, sensor_ID, sensor_type, sensor_value, units, timestamp from entries order by id desc')
        >>> entry = cur.fetchone()
        also: dump(g), dump(session), dir(), globals(), locals(), dir(g), dir(session), 
    '''
    return

@socketio.on('message')
def handle_message(message):
    # handle control messages from pages here - like start or stop tank filler
    print 'received message: ', message['data']


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',debug=True)


#Snippets:
"""
    


"""
