# -*- coding: utf-8 -*-
#################################################################################
#
#    zencli.py - A Zenoss JSON API Commandline Client
#    Copyright 2012 Stephan Adig <stephan.adig@citrix.com>
#       Licensed under the Apache License, Version 2.0 (the "License");
#       you may not use this file except in compliance with the License.
#       You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#       Unless required by applicable law or agreed to in writing, software
#       distributed under the License is distributed on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#       See the License for the specific language governing permissions and
#       limitations under the License.
#################################################################################

import sys
import json
import urllib
import urllib2

ROUTERS = { 'MessagingRouter': 'messaging',
            'EventsRouter': 'evconsole',
            'ProcessRouter': 'process',
            'ServiceRouter': 'service',
            'DeviceRouter': 'device',
            'NetworkRouter': 'network',
            'TemplateRouter': 'template',
            'DetailNavRouter': 'detailnav',
            'ReportRouter': 'report',
            'MibRouter': 'mib',
            'ZenPackRouter': 'zenpack' }


class ZenossAPI(object):
    def __init__(self,url,username,password, debug=False):
        self._conn=urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if debug:
            self._conn.add_handler(urllib2.HTTPHandler(debuglevel=1))
        self._reqCount=1
        self._url=url
        self._username=username
        self._password=password
        loginParams=urllib.urlencode(dict(
            __ac_name=username,
            __ac_password=password,
            submitted = 'true',
            came_from='%s/zport/dmd' % url
        ))
        self._conn.open('%s/zport/acl_users/cookieAuthHelper/login' % url ,loginParams)
    
    def _router_request(self,router,method,data=[]):
        if router not in ROUTERS:
            raise Exception('Router "%s" not available' % router)
        req=urllib2.Request('%s/zport/dmd/%s_router' % (self._url,ROUTERS[router]))
        req.add_header('Content-type','application/json; charset=utf-8')
        reqData=json.dumps([dict(
            action=router,
            method=method,
            data=data,
            type='rpc',
            tid=self._reqCount)])
        self._reqCount+=1
        return json.loads(self._conn.open(req,reqData).read())

    
    def get_device_classes(self):
        return self._router_request('DeviceRouter','getDeviceClasses')['result']

    def get_device_by_name(self,name):
        return self._router_request('DeviceRouter','getDevices',
                data=[{
                    'uid':'/zport/dmd/Devices',
                    'params':{
                        'name':name
                    }
                    }])['result']
    def get_devices(self,deviceClass='/zport/dmd/Devices'):
        return self._router_request('DeviceRouter','getDevices',
                data=[{
                    'uid':deviceClass,
                    'params':{}

                    }]
                )
    def get_production_states(self):
        return self._router_request('DeviceRouter','getProductionStates')['result']

    def set_production_state(self,device_uids,prodstate,hashcheck,uid=None,ranges=None,params=None,sort='name',dir='ASC'):
        return self._router_request('DeviceRouter','setProductionState',
                data=[{
                    'uids':device_uids,
                    'prodState':prodstate,
                    'hashcheck':hashcheck,
                    'uid':uid,
                    'ranges':ranges,
                    'params':params,
                    'sort':sort,
                    'dir':dir}])['result']


