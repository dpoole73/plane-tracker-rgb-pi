from datetime import datetime, timedelta
try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics
from utilities.animator import Animator
from utilities.solar import grab_solar_data
from setup import colours, fonts, frames, screen
import requests

# Scene Configuration

# Scene Configuration
SOLAR_REFRESH_SECONDS = 3600  # Update every hour (API rate limits!)
SOLAR_FONT = fonts.regular
SOLAR_USE_LABEL = (1, 10)
SOLAR_GEN_LABEL = (32, 10)
SOLAR_USAGE_TOP_LEFT = (1, 11) 
SOLAR_GENERATION_TOP_LEFT = (32, 11) 

class SolarScene(object):
    def __init__(self):
        super().__init__()
        self._last_solar_update = None
        self._solar_display_count = 0
        self._show_solar = False
        
    def fetch_stats(self):
        """
        Fetch the stats for the last day from the solar panel system
        """
        try:
            self._power_usage, self._power_production = grab_solar_data()
                
        except Exception as e:
            print(f"Error fetching solar data: {e}")
            self._power_usage = None
            self._power_production = None
    
    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def solar_data(self, count):
        """
        Display solar info when no planes are overhead.
        Alternates with other "no plane" scenes like weather forecast.
        """
        
        # Only show stock when there are NO planes
        if len(self._data):
            self._solar_display_count = 0
            return
        
        # only show if told to show
        if not(self._show_solar):
            return
        
        # need to wipe the whole display
        self.draw_square(
            0,
            0,
            screen.WIDTH,
            screen.HEIGHT,
            colours.BLACK,
        )
        
        # Determine if we need to fetch new stock data
        now = datetime.now()
        seconds_since_update = (now - self._last_solar_update).total_seconds() if self._last_solar_update else SOLAR_REFRESH_SECONDS
        
        if seconds_since_update >= SOLAR_REFRESH_SECONDS or self._power_production is None:
            # Fetch new stock data
            self.fetch_stats()
            self._last_solar_update = now
        
        # Show solar from last hour
        if self._power_production is None:
            # Display error message
            display_text = f"ERR"
            colour = colours.RED
        else:
            colour = colours.GREEN

            # figure out the scale of the graph

            max_value = 0
            # read all the values and normalize scale to reasonable number of pixels
            for u in self._power_usage:
                if u > max_value:
                    max_value = u

            for p in self._power_production:
                if p > max_value:
                    max_value = p

            # set max bar height to sensible value
            max_bar_height = 20

            graphics.DrawText(
                    self.canvas,
                    SOLAR_FONT,
                    SOLAR_USE_LABEL[0],
                    SOLAR_USE_LABEL[1],
                    colours.RED,
                    "Used"
            )

            graphics.DrawText(
                    self.canvas,
                    SOLAR_FONT,
                    SOLAR_GEN_LABEL[0],
                    SOLAR_GEN_LABEL[1],
                    colours.GREEN,
                    "Gen"
            )


            # draw a vertical line for each value for usage
            for i, u in enumerate(self._power_usage):
                # get normalized height
                normalzied_height = (u / max_value) * max_bar_height
                # two lines for each bar
                graphics.DrawLine(
                    self.canvas,
                    SOLAR_USAGE_TOP_LEFT[0] + 2 * i , # X offset one pixel per line 
                    SOLAR_USAGE_TOP_LEFT[1] + max_bar_height - normalzied_height,  # y coordinate is normalized max_bar_height - normalized height
                    SOLAR_USAGE_TOP_LEFT[0] + 2 * i,
                    SOLAR_USAGE_TOP_LEFT[1] + max_bar_height,
                    colours.RED)
                graphics.DrawLine(
                    self.canvas,
                    SOLAR_USAGE_TOP_LEFT[0] + 2 * i + 1, # X offset one pixel per line 
                    SOLAR_USAGE_TOP_LEFT[1] + max_bar_height - normalzied_height,  # y coordinate is normalized max_bar_height - normalized height
                    SOLAR_USAGE_TOP_LEFT[0] + 2 * i + 1,
                    SOLAR_USAGE_TOP_LEFT[1] + max_bar_height,
                    colours.RED)
                
            # draw a vertical line for each value for usage
            for i, u in enumerate(self._power_production):
                # get normalized height
                normalzied_height = (u / max_value) * max_bar_height
                graphics.DrawLine(
                    self.canvas,
                    SOLAR_GENERATION_TOP_LEFT[0] + 2 * i, # X offset one pixel per line 
                    SOLAR_GENERATION_TOP_LEFT[1] + max_bar_height - normalzied_height,  # y coordinate is normalized max_bar_height - normalized height
                    SOLAR_GENERATION_TOP_LEFT[0] + 2 * i,
                    SOLAR_GENERATION_TOP_LEFT[1] + max_bar_height,
                    colours.GREEN)
                graphics.DrawLine(
                    self.canvas,
                    SOLAR_GENERATION_TOP_LEFT[0] + 2 * i + 1, # X offset one pixel per line 
                    SOLAR_GENERATION_TOP_LEFT[1] + max_bar_height - normalzied_height,  # y coordinate is normalized max_bar_height - normalized height
                    SOLAR_GENERATION_TOP_LEFT[0] + 2 * i + 1,
                    SOLAR_GENERATION_TOP_LEFT[1] + max_bar_height,
                    colours.GREEN)
                
        self._show_solar = True