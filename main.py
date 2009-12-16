#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#


from google.appengine.ext import webapp, db
from google.appengine.ext.db import stats
from google.appengine.ext.webapp import util, template
import flickr
import os, datetime
from google.appengine.api import users

class PicRequest(db.Model):
    photo_id = db.StringProperty(required=True)
    furl = db.StringProperty(required=True)
    request_time = db.DateTimeProperty()
    

class ImageHandler(webapp.RequestHandler):
  

  sizes = {"m":"Medium", "s":"Small", "t":"Thumbnail", "b": "Large", "l":"Large"}

  def get(self, photo_id, size= None):
    p = flickr.photo_getInfo(photo_id)
    if((size is not None) and (size in self.sizes)):
      url =p.getURL(self.sizes[size], 'source')
    else:
      url =p.getURL('Medium', 'source')

    e = PicRequest(photo_id=photo_id,furl=url)
    e.request_time = datetime.datetime.now()
    e.put()

    self.redirect(url)
      

class UserHandler(webapp.RequestHandler):

  def get(self, username):

    self.response.out.write("Due to a weird bug with flickr, this is disabled right now. ");
    p = flickr.people_findByUsername(username)
    url = p.icon_url
    #url = "http://photos3.flickr.com/2/buddyicons/41134580@N00.jpg"
    self.response.out.write(url)
    #self.redirect(url)

class MainHandler(webapp.RequestHandler):

  def get(self):
    

    global_stat = stats.GlobalStat.all().get()

    if(global_stat is None):
      count = 1
    else:
      count =global_stat.count

    template_values = {
      'requestcount': count,
      'lasturl': 'ha',
      'requestcount24': 1
      }
    
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([(r'/i/(.*)\.(.*)\.jpg', ImageHandler),
                                        (r'/i/(.*)\.jpg', ImageHandler),
                                        (r'/u/(.*)\.jpg', UserHandler),
                                        ('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
