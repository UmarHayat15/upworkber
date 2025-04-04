from pricing_service.db import ModelBase, PostgresDB, Conn
from sqlalchemy import create_engine
from pricing_service.db import BaseDao

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class BaseService:
    def __init__(self, dao: BaseDao):
        engine = create_engine(Conn().get_db_url())
        # Create tables in the test database
        ModelBase.metadata.create_all(engine)
        self.dao = dao(engine)

    def get(self, query=None):
        return [self.dao.as_dict(x) for x in self.dao.fetch_all()]

    def insert(self, items: list):
        self.dao.insert(items)

    def insert_many(self, items: list):
        self.dao.insert_many(items)


class BaseWebDriverService:
    def __init__(self):
        pass

    def chrome_options(self, docker_mode=False, proxy_settings="0.0.0.0:3128"):
        options = Options()

        if docker_mode:
            options.add_argument("--headless=new")  # Run Chrome in the new headless mode
            options.add_argument("--no-sandbox")  # required when running as root in Docker
            options.add_argument("--disable-dev-shm-usage")  # avoids issues with limited space
            options.add_argument("--disable-gpu")  # necessary for headless mode
            options.add_argument("--window-size=1920,1080") # Optional: Specify window size for layout consistency

        if proxy_settings:
            options.add_argument(f"--proxy-server={proxy_settings}")

        return options


    def setup_driver(self):
        service = Service()
        driver = webdriver.Chrome(service=service, options=self.chrome_options())
        return driver