import cgi
import webapp2

from google.appengine.api import urlfetch

from lxml import html
from lxml.html import parse

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/zoar" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Zoa ae os irmaum"></div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.write(MAIN_PAGE_HTML)

class Zoeira(webapp2.RequestHandler):
  def post(self):
    self.response.write('<html><body>Muita treta:<pre>')
    self.response.write(cgi.escape(self.request.get('content')))
    self.response.write('<br><br>')

    result = urlfetch.fetch("http://www.carandclassic.co.uk/")
    result_stripped = unicode ( result.content , errors = 'ignore' )

    page = html.fromstring(result_stripped)

    #page = parse("http://www.carandclassic.co.uk/").getroot()
    #page.make_links_absolute()
    latest = page.xpath (
        '//div[@class="item alt"]/div[@class="titleAndText"]/p/text()' )

    self.response.write ( latest )

    self.response.write ( '</pre></body></html>' )



app = webapp2.WSGIApplication ( [
  ('/', MainPage) ,
  ('/zoar', Zoeira) , ] ,
  debug = True )
