import re
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from pricing_service.service.base import BaseWebDriverService


class FacebookService(BaseWebDriverService):
    def __init__(self):
        pass

    facebook_marketplace_cities = [
        "albuquerque", "anchorage", "annarbor", "appleton", "arlington",
        "atlanta", "augusta", "austin", "bakersfield", "baltimore",
        "batonrouge", "birmingham", "boise", "boston", "buffalo",
        "charleston", "charlotte", "chattanooga", "chicago", "cincinnati",
        "cleveland", "coloradosprings", "columbia", "columbus", "dallas",
        "dayton", "denver", "desmoines", "detroit", "elpaso",
        "erie", "eugene", "evansville", "fargo", "fayetteville",
        "flint", "fortlauderdale", "fortmyers", "fortwayne", "fortworth",
        "fresno", "grandrapids", "greensboro", "greenville", "honolulu",
        "houston", "huntsville", "indianapolis", "jackson", "jacksonville",
        "kansascity", "knoxville", "lansing", "lasvegas", "lexington",
        "lincoln", "little-rock", "losangeles", "louisville", "lubbock",
        "madison", "memphis", "miami", "milwaukee", "minneapolis",
        "modesto", "mobile", "nashville", "newhaven", "neworleans",
        "newyork", "norfolk", "oakland", "oklahomacity", "omaha",
        "orlando", "philadelphia", "phoenix", "pittsburgh", "portland",
        "provo", "raleigh", "reno", "richmond", "rochester",
        "sacramento", "saltlakecity", "sanantonio", "sandiego", "sanfrancisco",
        "sanjuan", "sanjose", "santarosa", "savannah", "seattle",
        "shreveport", "siouxfalls", "spokane", "springfield", "stlouis",
        "stpaul", "stockton", "syracuse", "tallahassee", "tampa",
        "toledo", "tucson", "tulsa", "virginiabeach", "washington",
        "108028339219415", ### paia, hawaii
        "106288819402892", ### kahului
    ]

    def fb_urlgen(base_url, city, query, queryItems):
        return f"{base_url}/{city}/search?query={query}" + "".join({f"&{x}={queryItems.get(x)}" for x in queryItems})

    def selenium_find_all_text_fields(self, driver):
        spans = driver.find_elements(By.XPATH, "//span[string-length(normalize-space(text())) > 0]")
        all_texts = [span.text for span in spans if span.text.strip()]
        for i in range(0, len(all_texts)):
            print(f"{i} {all_texts[i]}")

    def close_fb_popup(self, driver: webdriver.Chrome):
        try:
            close_button = driver.find_element(
                By.XPATH,
                "//div[@aria-label='Close' and @role='button']")
            close_button.click()
        except:
            print("No close button found")

    def class_elements(self, el):
        return el.get_attribute("class").split(" ")

    def search_fb(self, days_back=10, query="fender american_vintage", city="la"):
        driver = self.setup_driver()
        days_old = f"{days_back}"
        base_url = f"https://www.facebook.com/marketplace"
        queryItems = {
            "daysSinceListed": days_old,
        }

        url = self.fb_urlgen(base_url, city, query, queryItems)

        driver.get(url)
        print(url)

        self.close_fb_popup(driver)

        links = driver.find_elements(By.TAG_NAME, "a")

        valid_links = [i for i in links if len(i.text.split('\n')) == 3]
        all_entries = []
        for i in valid_links:
            price, title, location = i.text.split('\n')
            href = i.get_attribute("href")
            marketplace_id = href.split('/')[5]
            print(price, title, location, href)
            all_entries.append(dict(price=price, title=title, location=location, href=href, mp_id=marketplace_id))
        try:
            return all_entries
        finally:
            driver.quit()

    def browse_fb(self, category, city):
        driver = self.setup_driver()

        base_url = f"https://www.facebook.com/marketplace"

        url = f"{base_url}/{city}/{category}"

        driver.get(url)

        self.close_fb_popup(driver)

        # Scroll to load more listings
        for _ in range(1):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)

        # Extract listings
        listing_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/marketplace/item/')]")

        seen_ids = set()
        listings_data = []

        for listing in listing_elements:
            try:
                href = listing.get_attribute("href")
                if not href:
                    continue

                # Extract marketplace ID from URL
                match = re.search(r'/marketplace/item/(\d+)', href)
                marketplace_id = match.group(1) if match else None
                if marketplace_id in seen_ids:
                    continue  # skip duplicates
                seen_ids.add(marketplace_id)

                text = listing.text.split('\n')
                price = text[0] if len(text) > 0 else ""
                title = text[1] if len(text) > 1 else ""
                location = text[2] if len(text) > 2 else ""

                listings_data.append({
                    "price": price,
                    "title": title,
                    "location": location,
                    "href": href,
                    "marketplace_id": marketplace_id
                })
            except Exception as e:
                print("Error parsing listing:", e)

        return listings_data

    def fbm_listing_detail(self, url):
        driver = self.setup_driver()

        driver.get(url)
        time.sleep(5)

        title = description = location = seller_link = ""
        images = []
        #response = Selector(text=driver.page_source)
        try:
            title = driver.find_element(By.XPATH, '//h1/span').text
        except:
            pass
            #title = response.xpath('//h1/span::text').get('')

        try:
            description = driver.find_element(By.CSS_SELECTOR,
                                              'div.x126k92a span.x193iq5w').text
        except:
            #description = response.css('div.x126k92a span.x193iq5w::text').get('')
            pass

        try:
            seller_element = driver.find_element(By.CSS_SELECTOR, 'span.xjp7ctv a.x1i10hfl')
            seller_link = seller_element.get_attribute("href")
        except:
            #seller_link = response.css('span.xjp7ctv a.x1i10hfl::text').get('')
            pass

        try:
            location_element = driver.find_element(By.CSS_SELECTOR, 'div[class="x14vqqas x11i5rnm xod5an3 x1mh8g0r"] span.xzsf02u span')
            location = location_element.text
        except:
            #location = response.css('div[class="x14vqqas x11i5rnm xod5an3 x1mh8g0r"] span.xzsf02u span::text').get('')
            pass

        try:
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.x1o1ewxj')
            images = list({img.get_attribute("src") for img in image_elements})
        except:
            #images = response.css('img.x1o1ewxj::attr(src)').getall()
            pass

        try:
            pass
        finally:
            driver.quit()

        return {
            "URL": url,
            "Title": title,
            "Description": description,
            "Seller Profile": seller_link,
            "Location": location,
            "Images": ", ".join(images)
    }