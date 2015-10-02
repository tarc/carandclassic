import cgi
import webapp2

from google.appengine.api import urlfetch

from lxml import html
from lxml.html import parse


def prune (text):
  return ''.join(c for c in text if not c in ('\n' , '\r' , '\t'))

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.write('<html><body>List:<pre>')

    result = urlfetch.fetch("http://www.carandclassic.co.uk/")
    result_stripped = unicode ( result.content , errors = 'ignore' )

    page = html.fromstring(result_stripped)

    latest = page.xpath (
        '//div[@class="item alt"]/div[@class="titleAndText"]/p/text()' )

    self.response.write ( '<ul>' )
    for desc in latest:
      self.response.write ( '<li>' )
      self.response.write ( cgi.escape ( prune ( desc ) ) )
      self.response.write ( '</li>' )

    self.response.write ( '</ul>' )

    self.response.write ( '</pre></body></html>' )



app = webapp2.WSGIApplication ( [
  ('/', MainPage) ,
  ] ,
  debug = True )
