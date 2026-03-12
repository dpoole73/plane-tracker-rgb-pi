ZONE_HOME = {
    "tl_y": xx.xxxxxx, # Top-Left Latitude (deg) https://www.latlong.net/ or google maps. The bigger the zone, the more planes you'll get. My zone is ~3.5 miles in each direction or 10mi corner to corner. 
    "tl_x": xx.xxxxxx, # Top-Left Longitude (deg)
    "br_y": xx.xxxxxx, # Bottom-Right Latitude (deg)
    "br_x": xx.xxxxxx # Bottom-Right Longitude (deg)
}
LOCATION_HOME = [
    xx.xxxxxx, # Latitude (deg)
    xx.xxxxxx # Longitude (deg)
]
TEMPERATURE_LOCATION = "xx.xxxxxx,xx.xxxxxx" #same as location home
TOMORROW_API_KEY = "xxxxxxx" # Get an API key from https://tomorrow.io they only allows 25 pulls an hour, if you reach the limit you'll need to wait until the next hour 
TEMPERATURE_UNITS = "imperial" #can use "metric" if you want, same for distance 
DISTANCE_UNITS = "imperial"
CLOCK_FORMAT = "12hr" #use 12hr or 24hr
MIN_ALTITUDE = 2000 #feet above sea level. If you live at 1000ft then you'd want to make yours ~3000 etc. I use 2000 to weed out some of the smaller general aviation traffic. 
BRIGHTNESS = 100
BRIGHTNESS_NIGHT = 50
NIGHT_BRIGHTNESS = False #True for on False for off
NIGHT_START = "22:00" #dims screen between these hours
NIGHT_END = "06:00"
GPIO_SLOWDOWN = 2 #depends what Pi you have I use 2 for Pi 3 and 1 for Pi Zero
JOURNEY_CODE_SELECTED = "XXX" #your home airport code ALL CAPS ie ORD
JOURNEY_BLANK_FILLER = " ? " #what to display if theres no airport code
HAT_PWM_ENABLED = False #only if you haven't soldered the PWM bridge use True if you did
FORECAST_DAYS = 3 #today plus the next two days
EMAIL = "" #insert your email address between the " ie "example@example.com" to recieve emails when there is a new top 3 flight. Leave "" to recieve no emails. It will log/local webpage regardless
MAX_FARTHEST = 3 #the amount of furthest flights you want in your log
MAX_CLOSEST = 3 #the amount of closest flights to your house you want in your log

SOLAR_API_KEY = "XXX" # api key for this app
SOLAR_AUTH_CODE = "XXX" # code based on user authentication allowing access to our account
SOLAR_REDIRECT_URI = "https://api.enphaseenergy.com/oauth/redirect_uri"
SOLAR_SYSTEM_ID = "XXXXX" # your system id
SOLAR_ENDPOINT = "https://api.enphaseenergy.com/api/v4/systems"
SOLAR_CLIENT_ID= "XXXX"
SOLAR_CLIENT_SECRET = "XXXX"
# can't use the auth code above more than once so we will stire this for now instead
SOLAR_REFRESH_TOKEN = "XXXX"

# sign up for an API key here https://www.alphavantage.co/support/#api-key
STOCK_API_KEY = "XXXXX"
STOCK_SYMBOL = "XXXXX"
STOCK_REFRESH_SECONDS = 300
STOCK_DISPLAY_SECONDS = 10