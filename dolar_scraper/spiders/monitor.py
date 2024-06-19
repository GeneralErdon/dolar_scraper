from decimal import Decimal
from typing import Any
import scrapy
from scrapy.responsetypes import Response
from scrapy.selector import Selector

class BcvSpider(scrapy.Spider):
    name = "MONITOR"
    start_urls = [
        "https://monitordolarvenezuela.com/monitor-dolar-hoy",
        ]
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        
        pass