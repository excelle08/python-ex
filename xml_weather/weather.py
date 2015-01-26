__author__ = 'Excelle'
from xml.parsers.expat import ParserCreate
import urllib2


class WeatherModel(object):
    # Basic information
    CityName = ""
    Region = ""
    Country = ""
    # Units
    uniTemperature = "C"
    uniPressure = "mb"
    uniDistance = "km"
    uniSpeed = "km/h"
    # Current condition
    nowTemp = "0.0"
    nowHumidity = "0"
    nowVisibility = "0.0"
    nowWindGrade = "0"
    nowPressure = "0.0"
    nowWeather = 'Sunny'
    SunRise = "0:00 am"
    SunSet = "0:00 pm"
    # Forecasts
    ForeCastTable = []
    Row = {}

    def setBasicInf(self, city, country, region=""):
        self.CityName = city
        self.Country = country
        self.Region = region

    def setUnits(self, uT, uP, uD, uS):
        self.uniTemperature = uT
        self.uniPressure = uP
        self.uniDistance = uD
        self.uniSpeed = uS

    def addForeCast(self, row):
        self.ForeCastTable.append(row)


class XmlSaxHandler(object):
    def __init__(self, weatherobject):
        self.weatherobj = weatherobject

    def start_element(self, name, attrs):
        try:
            if name == 'yweather:location':
                self.weatherobj.setBasicInf(attrs['city'], attrs['country'], region=attrs['region'])
            elif name == 'yweather:units':
                self.weatherobj.setUnits(attrs['temperature'], attrs['pressure'], attrs['distance'], attrs['speed'])
            elif name == 'yweather:wind':
                self.weatherobj.nowWindGrade = attrs['chill']
            elif name == 'yweather:atmosphere':
                self.weatherobj.nowHumidity = attrs['humidity']
                self.weatherobj.nowVisibility = attrs['visibility']
                self.weatherobj.nowPressure = attrs['pressure']
            elif name == 'yweather:astronomy':
                self.weatherobj.SunRise = attrs['sunrise']
                self.weatherobj.SunSet = attrs['sunset']
            elif name == 'yweather:condition':
                self.weatherobj.nowTemp = attrs['temp']
                self.weatherobj.nowWeather = attrs['text']
            elif name == 'yweather:forecast':
                self.weatherobj.addForeCast(attrs)
            else:
                pass
        except ValueError:
            pass


    def end_element(self, name):
        pass

    def char_data(self, text):
        pass

# Retrieve data from Yahoo
url = "http://weather.yahooapis.com/forecastrss?u=c&w=2168396"
f = urllib2.urlopen(url)
data = f.read()
print 'Successfully retrieved online data.'
# Parse XML file
w = WeatherModel()
handler = XmlSaxHandler(w)
parser = ParserCreate()
parser.returns_unicode = True
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(data)
# Get Weather object and print
w = handler.weatherobj
print "%s, %s" % (w.CityName, w.Country)
print "Temperature: %s %s, Wind: %s" % (w.nowTemp, w.uniTemperature, w.nowWindGrade)
print w.nowWeather
print "Pressure: %s %s, Humidity: %s %%, Visibility: %s %s " % (w.nowPressure, w.uniPressure, w.nowHumidity,
                                                               w.nowVisibility, w.uniDistance)
print "Sunrise: %s, Sunset: %s" % (w.SunRise, w.SunSet)
print "Forecasts:"

for dict in w.ForeCastTable:
    print "%s,%s %s~%s %s, %s" % (dict['day'], dict['date'], dict['low'], dict['high'], w.uniTemperature, dict['text'])

