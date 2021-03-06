#! /usr/bin/env python
import rospy
import threading
from time import time, strftime, sleep
import subprocess

from flask import Flask, request, jsonify
from flask_cors import CORS

from std_msgs import msg
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image, CompressedImage

from check_create_folder_tool import FolderCheckCreate

class Main():
    def __init__(self):
        self.id = 'main'

        self.date_time = strftime("%Y%m%d-%H%M%S")

        self.topics = []

        self.run = False
        self.bag_name = 'No current or previous bag has been saved.'

        self.load_topics()

        self.activity = 'none'

        self.participant = 999

        print('Ready.')

    def load_topics(self):
        with open('/home/sandbox/config/topics_robot_2.txt') as f:
            lines = f.readlines()

            lines_clean = []
            for line in lines:
                lines_clean.append(line.rstrip('\n'))

            for line in lines_clean:
                self.topics.append(line)
            
            print('Will check for messages on these topics...')
            print(self.topics)
            
    def loop(self):
        while(True):
            if self.run:
                date_time = strftime("%Y%m%d-%H%M%S")

                if self.activity == 'none':
                    self.bag_name = '/home/sandbox/output/' + 'P' + str(self.participant) + '/ROSbag_' + date_time + '_secondary.bag'
                else:
                    self.bag_name = '/home/sandbox/output/' + 'P' + str(self.participant) + '/ROSbag_' + date_time + '_' + self.activity + '_secondary.bag'

                while(self.run):
                    cmd = ['rosbag', 'record', '-O', self.bag_name]
                    for topic in self.topics:
                        cmd.append(topic)
                    
                    self.p = subprocess.Popen(cmd)

                    while not rospy.core.is_shutdown() and self.run:
                        rospy.rostime.wallsleep(0.5)

                self.p.terminate()            

            sleep(1)

    def set_state(self, cmd):
        if cmd:
            self.run = True
        else:
            self.run = False

    def set_activity(self, activity):
        self.activity = activity

    def set_participant(self, participant):
        self.participant = participant
        fcc = FolderCheckCreate()
        fcc.run(self.participant)

if __name__ == '__main__':
    threading.Thread(target=lambda: rospy.init_node('ralt_signalman_secondary', disable_signals=True)).start()

    m = Main()

    app = Flask(__name__)
    CORS(app)

    threading.Thread(target=lambda: m.loop()).start()
    
    @app.route('/control', methods = ['POST'])
    def control_handler():
        data = request.get_json()
        
        command = data['command']
        activity = data['activity']

        print(command, activity)

        resp = "OK"

        m.set_activity(activity)

        if command == "True":
            m.set_state(True)
        elif command == "False":
            m.set_state(False)
        else:
            resp = "Invalid state. Send command to either 'True' or 'False'."

        return resp

    @app.route('/participant', methods = ['POST'])
    def participant_handler():
        data = request.get_json()

        participant = data['participant']

        participant = int(participant)

        m.set_participant(participant)

        resp = "OK"

        return resp

    @app.route('/status', methods = ['GET'])
    def status_handler():
        status = {}

        status["topics"] = m.topics
        status["running"] = m.run
        status["bagfile"] = m.bag_name

        return jsonify(status)

    app.run(host='0.0.0.0', port = 5004)
