'''
Created on 2015

@author: aadebuger
'''

from flask import Flask
from flask import abort,jsonify
from flask_restful import Resource, Api,request
import json
from mongoengine import * 
from pymongo import read_preferences
from passlib.apps import custom_app_context as pwd_context
app = Flask(__name__)
api = Api(app)
import payresource

    
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class Charges(payresource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="charges"
class ChargesList(payresource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="charges"
class Events(payresource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="events"
class EventsList(payresource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="events"

@app.route('/v2/charges', methods=['POST'])
def new_user():
    print 'request=',request
    form = request.form
    
    print form
    return "hello"
    
    
api.add_resource(ChargesList, '/v1/charges')
api.add_resource(Charges, '/v1/charges<string:story_id>')
api.add_resource(EventsList, '/v1/events')
api.add_resource(Events, '/v1/events<string:todo_id>')


if __name__ == '__main__':
#    connect('stylemaster',host=util.getMydbip())
#    connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
            
    app.run(debug=True)