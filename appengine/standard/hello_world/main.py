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

import base64

from apiclient.discovery import build
from google.appengine.api import urlfetch
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        url = 'https://hsreplay.net/api/v1/live/replay_feed/'
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                service = build('pubsub', 'v1')
                publish_client = service.projects().topics()
                topic = 'projects/hsreplay-feed/topics/replay-feed'
                message = base64.b64encode(result.content)
                body = {'messages': [{'data': message}]}
                publish_client.publish(topic=topic, body=body).execute()
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
