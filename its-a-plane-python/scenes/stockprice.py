from datetime import datetime, timedelta
try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics
from utilities.animator import Animator
from setup import colours, fonts, frames, screen
import requests

# Attempt to load config data
try:
    from config import STOCK_API_KEY
    from config import STOCK_SYMBOL
    from config import STOCK_REFRESH_SECONDS
    from config import STOCK_DISPLAY_SECONDS

except (ModuleNotFoundError, NameError, ImportError):
    STOCK_API_KEY = ""
    STOCK_SYMBOL = "MSFT"  # Change to your desired stock
    STOCK_REFRESH_SECONDS = 300  # Update every 5 minutes (API rate limits!)
    STOCK_DISPLAY_SECONDS = 10

# Scene Configuration
STOCK_FONT = fonts.small
STOCK_SYMBOL_POSITION = (1, 10) 
STOCK_PRICE_POSITION  = (1, 20)

class StockPriceScene(object):
    def __init__(self):
        super().__init__()
        self._stock_price = None
        self._stock_change = None
        self._last_stock_update = None
        self._stock_display_count = 0
        self._show_stock = False
        
    def fetch_stock_price(self):
        """
        Fetch stock price from Alpha Vantage or other free API
        You'll need to sign up for a free API key at:
        https://www.alphavantage.co/support/#api-key
        """
        try:
            # Using Alpha Vantage free API (replace YOUR_API_KEY)
            api_key = STOCK_API_KEY
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={STOCK_SYMBOL}&apikey={api_key}"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "Global Quote" in data:
                price = float(data["Global Quote"]["05. price"])
                change_percent = float(data["Global Quote"]["10. change percent"].rstrip('%'))
                return price, change_percent
            else:
                print(f"Stock API error: {data}")
                return None, None
                
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None, None
    
    @Animator.KeyFrame.add(frames.PER_SECOND * 1)
    def stock_price(self, count):
        """
        Display stock price when no planes are overhead.
        Alternates with other "no plane" scenes like weather forecast.
        """
        
        # Only show stock when there are NO planes
        if len(self._data):
            self._stock_display_count = 0
            return
        
        # only show if told to show
        if not(self._show_stock):
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
        seconds_since_update = (now - self._last_stock_update).total_seconds() if self._last_stock_update else STOCK_REFRESH_SECONDS
        
        if seconds_since_update >= STOCK_REFRESH_SECONDS or self._stock_price is None:
            # Fetch new stock data
            price, change = self.fetch_stock_price()
            if price is not None:
                self._stock_price = price
                self._stock_change = change
                self._last_stock_update = now
        
        # Show stock this cycle
        if self._stock_price is None:
            # Display error message
            display_text = f"ERR"
            colour = colours.RED
        else:
            # Format: "AAPL: $150.25"
            display_text = f"${self._stock_price:.2f}"
            
            # Color based on change: green if up, red if down, white if unchanged
            if self._stock_change > 0:
                colour = colours.GREEN
            elif self._stock_change < 0:
                colour = colours.RED
            else:
                colour = colours.WHITE
        
        # Draw stock price
        graphics.DrawText(
            self.canvas,
            STOCK_FONT,
            STOCK_SYMBOL_POSITION[0],
            STOCK_SYMBOL_POSITION[1],
            colour,
            STOCK_SYMBOL,
        )

        graphics.DrawText(
            self.canvas,
            STOCK_FONT,
            STOCK_PRICE_POSITION[0],
            STOCK_PRICE_POSITION[1],
            colour,
            display_text,
        )
        
        # Draw change percentage on second line if we have the data
        if self._stock_change is not None:
            change_text = f"{'+' if self._stock_change > 0 else ''}{self._stock_change:.2f}%"
            graphics.DrawText(
                self.canvas,
                fonts.small,
                STOCK_PRICE_POSITION[0] + 5,
                STOCK_PRICE_POSITION[1] + 10,
                colour,
                change_text,
            )
        
        self._show_stock = True