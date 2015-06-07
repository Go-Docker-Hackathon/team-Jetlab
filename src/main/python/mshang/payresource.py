# -*- coding: utf-8 -*-
'''
Created on 2015

@author: aadebuger
'''
# -*- coding: utf-8 -*-
'''
Created on 2015年5月30日

@author: aadebuger
'''

import json
from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
from pymongo import collection
#from pymongo import ReturnDocument


from pymongo import collection

from bson import json_util
from bson.objectid import ObjectId
import util
import time
from datetime import datetime
from time import time

#import MongodbOperation
from mongoengine import Document, EmailField, StringField, BooleanField, queryset_manager
from passlib.apps import custom_app_context as pwd_context
#from passlib.hash import pbkdf2_sha256
#from passlib.utils import consteq
from pymongo import read_preferences


def getNextSequence(documentname):
        print 'getNextSequence'
        client = MongoClient(util.getMydbip())
        db = client.test_database    
#        ret = db[documentname].find_one_and_update(   {'_id': 'userid'}, {'$inc': {'seq': 1}},  projection={'seq': True, '_id': False}, upsert=True, return_document=ReturnDocument.AFTER)
        ret = db[documentname].find_and_modify(   {'_id': 'orderid1'}, {'$inc': {'seq': 1}},  projection={'seq': True, '_id': False}, upsert=True,new=True)

        print ret
        return  ret['seq'];
def newOrderno(document):
            updatedAt= time.strftime('%Y%m%d%H%M%S')
            incnumber = getNextSequence("incnumber")
            order_no = "%s%03d"%(updatedAt,int(incnumber)%1000)
            return order_no
def newUpload(documentname):
        try:
            client = MongoClient(util.getMydbip())
            db = client.test_database
            ret = db[documentname].insert({})      
            print str(ret)
            return str(ret)
        except Exception,e:
            print e
        return None      
def newBucketUpload(documentname,size,bucket,url,name):
        try:
            client = MongoClient(util.getMydbip())
            db = client.test_database
            print 'datetime=',datetime.utcnow()
            print 'datetime=',time.strftime('%Y-%m-%dT%H:%M:%S')
            
            datadict = {"size":size,"bucket":bucket,"url":url,"name":name, "createdAt": time.strftime('%Y-%m-%dT%H:%M:%S')}
            ret = db[documentname].insert(datadict)      
            print str(ret)
            del datadict["_id"]
            datadict['objectId']= str(ret)
            return datadict      
        except Exception,e:
            print e
        return None  
class MResourceList(Resource):
    def __init__(self,documentname):
        '''
        Constructor
        '''
        self.documentname =documentname
        
    def before_save(self):
        return True;
    def after_save(self):
        print 'after_save1'
    def get(self):
        print 'get'
 #       args = parser.parse_args()
 #       print 'args=',args        
        client = MongoClient(util.getMydbip())
        db = client.test_database
        print "list get=",request
        searchword = request.args.get('where', '')
        offset = int(request.args.get('offset', '0'))
        limit = int(request.args.get('limit', '0'))
        
        
        print 'searchword=',searchword
        print 'offset=',offset
        print 'limit=',limit
        
        
#        ret = db.news.find_one()
        if searchword=='':
            print 'searchword=null'
#sort({"createdAt":-1})            
            try: 
                    if limit==0:
                        if offset ==0:
                            ret = db[self.documentname].find().sort([('_id', -1)])
                        else:
                            ret = db[self.documentname].find().sort([('_id', -1)]).offset(offset);
                    else:
                        if offset == 0 :
                            ret = db[self.documentname].find().sort([('_id', -1)]).limit(limit)
                        else:
                            ret = db[self.documentname].find().sort([('_id', -1)]).skip(offset).limit(limit)
            except Exception,e:
                    print e
        else:
             dict = json.loads(searchword)
             ret = db[self.documentname].find(dict)
        newsv = [];
        for news in ret:
            print 'news=',news
            print 'news get id',news.get("id")
            if news.get("id")==None:
                oid =  str(news["_id"])
                del news["_id"]
                news['id']=oid
            newsv.append(news)
        print 'newsv=',newsv
#        return json.dumps(newsv,default=json_util.default)        
        retstr= json.dumps(newsv,default=json_util.default)  
        newdict = json.loads(retstr)  
        return newdict
    def post(self):
        print "post=",request
        print request.url
        print 'request=',request
        form = request.form       
        if not self.before_save():
             return "111",404
        
        try:
            print "post request=",request.form
            client = MongoClient(util.getMydbip())
            db = client.test_database
 #           timestr= time.strftime('%Y-%m-%d %H:%M:%S')
##            request.form['createdAt']=timestr
            data = dict((key, request.form.getlist(key)) for key in request.form.keys())
            print 'data=',data
 #           data['createdAt']=timestr
            data['created']=int( time())
            data['refunded']=False
            data['pay']=False
            data['time_expire']=int( time())+3600*2
            ret = db[self.documentname].insert(data)      
            print str(ret)
 #           retdict = {"objectId":str(ret),'createdAt':timestr}
            self.after_save();
            print 'data=',data
            if data.get("id")==None:
                oid =  str(data["_id"])
                del data["_id"]
                data['id']=oid
            return json.dumps(data),201
        except Exception,e:
            print e
            
        return "111"
class MResource(Resource):
    '''
    classdocs
    '''


    def __init__(self,documentname):
        '''
        Constructor
        '''
        self.documentname =documentname
    def get(self, todo_id):
        print 'MResource  get todo_id',todo_id
        client = MongoClient(util.getMydbip())
        db = client.test_database
#        abort_if_todo_doesnt_exist(todo_id)

#        return TODOS[todo_id]
        document = db[self.documentname].find_one({'_id': ObjectId(todo_id)})
        print 'document=',document
        if document==None:
                abort(404, message="{} doesn't exist".format(todo_id))
                    
#        return json.dumps(document,default=json_util.default)  
        oid =  str(document["_id"])
        del document["_id"]
        document['id']=oid
        document['objectId']=oid
            
        retstr = json.dumps(document,default=json_util.default)      
        print 'retstr=',retstr  
        newdict = json.loads(retstr)  
        return newdict
    def delete(self, todo_id):
        print 'todo_id',todo_id
#        abort_if_todo_doesnt_exist(todo_id)
        client = MongoClient(util.getMydbip())
        db = client.test_database
        ret  = db[self.documentname].remove({'_id': ObjectId(todo_id)})   
        print 'ret=',ret     
        return '', 204

    def put(self, todo_id):
        print "put=",request
        print 'todo_id',todo_id
        try:
            print "put request=",request.json
#            newtodo_id = request.json['id'];
#            print "newtodo_id=",newtodo_id;
            client = MongoClient(util.getMydbip())
            try:
                del request.json["id"];
            except Exception,e:
                    print e
            db = client.test_database
            opword = request.args.get('op', '')
            print 'opword=',opword;
            updatedAt= time.strftime('%Y-%m-%d %H:%M:%S')
            request.json['updatedAt']=time.strftime('%Y-%m-%d %H:%M:%S')
            if opword=='':
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{"$set":request.json})      
            else:
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{opword:request.json}) 
            print 'ret=',ret
            retdict = {"id":todo_id,"updatedAt":updatedAt}
            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201

if __name__ == '__main__':
    pass