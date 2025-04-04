import time
from pricing_service.service.base import BaseWebDriverService


class SystemService(BaseWebDriverService):
    def __init__(self):
        pass

    def get_geo_location(self, url="https://whatismyipaddress.com/"):
        try:
            driver = self.setup_driver()

            driver.get(url)

            time.sleep(10)

        finally:
            driver.quit()