# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2, json, urllib2
from riotwatcher import RiotWatcher

api = "RGAPI-39baa1e6-4f95-4875-9d97-c5ff7ff7e89b"

class ReqPage(webapp2.RequestHandler):
    def get(self):
        try:
            query = self.request.GET['summoner']
            print(query)
            request = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+ query +"?api_key=" + api
            self.response.headers['Content-Type'] = 'application/json;charset=utf-8'
            contents = urllib2.urlopen(request).read()
            self.response.write(contents)
        except Exception as err:
            print(err)
            self.response.write("Oops something went wrong </br>" + str(err))


class MainPage(webapp2.RequestHandler):
    def get(self):
        '''
        watcher = RiotWatcher('RGAPI-39baa1e6-4f95-4875-9d97-c5ff7ff7e89b')
        my_region = 'NA1'
        me = watcher.summoner.by_name(my_region, 'Forrest the Fast')
        my_ranked_stats = watcher.league.positions_by_summoner(my_region, me['id'])
        '''
        request = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/Forrest%20the%20Fast?api_key=" + api
        print(request)
        try:
            self.response.headers['Content-Type'] = 'application/json;charset=utf-8'   
            contents = urllib2.urlopen(request).read()
            self.response.write(contents)
        except Exception as err:
            print(err)
            self.response.write("Oops something went wrong </br>" + str(err))

class DataPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Type'] = 'application/json;charset=utf-8'   
        '''
        request = "https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/Forrest%20the%20Fast?api_key=" + api
        request = "https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches1.json"
        try:
            # Opens the API request, then writes it to the page to view
            contents = urllib2.urlopen(request).read()
            print(urllib2.urlopen(request).info())
            self.response.write(contents)
            print("finished")
        except Exception as err:
            self.response.write(err)
            print("error")

        self.response.write('Listbucket result:\n')
        '''
        with open('matchdata1.json') as file:
            self.response.write(file.read())


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/data', DataPage),
    ('/request', ReqPage)
], debug=True)
