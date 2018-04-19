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
import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity

def get(self):
  bucket_name = os.environ.get('BUCKET_NAME',
                               app_identity.get_default_gcs_bucket_name())

  self.response.headers['Content-Type'] = 'text/plain'
  self.response.write('Demo GCS Application running from Version: '
                      + os.environ['CURRENT_VERSION_ID'] + '\n')
  self.response.write('Using bucket name: ' + bucket_name + '\n\n')

def create_file(self, filename):
  """Create a file.

  The retry_params specified in the open call will override the default
  retry params for this particular file handle.

  Args:
    filename: filename.
  """
  self.response.write('Creating file %s\n' % filename)

  write_retry_params = gcs.RetryParams(backoff_factor=1.1)
  gcs_file = gcs.open(filename,
                      'w',
                      content_type='text/plain',
                      options={'x-goog-meta-foo': 'foo',
                               'x-goog-meta-bar': 'bar'},
                      retry_params=write_retry_params)
  gcs_file.write('abcde\n')
  gcs_file.write('f'*1024*4 + '\n')
  gcs_file.close()
  self.tmp_filenames_to_clean_up.append(filename)

class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Type'] = 'application/json;charset=utf-8'   
        api = "RGAPI-61e2a1c6-837c-44ad-b828-59ea4a29d7e5"
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

        page_size = 1
        stats = gcs.listbucket(bucket + '/foo', max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')

            if count != page_size or count == 0:
              break
            stats = gcs.listbucket(bucket + '/foo', max_keys=page_size, marker=stat.filename)




app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
