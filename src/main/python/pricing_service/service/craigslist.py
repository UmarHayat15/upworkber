from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pricing_service.service.base import BaseWebDriverService


class CraigslistService(BaseWebDriverService):
    def __init__(self):
        pass

    def browse_craigslist(self, category: str, primary_location: str, secondary_location: str):
        try:
            driver = self.setup_driver()
            driver.implicitly_wait(3)

            listings_url = f"https://{primary_location}.craigslist.org/search/{secondary_location}/{category}#search=2~gallery~0"

            print(f"listings_url: {listings_url}")

            driver.get(listings_url)

            search_results = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@data-pid]"))
            )
            data = []
            for result in search_results:

                pid = result.get_attribute("data-pid")

                title = result.find_element(By.XPATH, ".//a/span").text
                try:
                    price = result.find_element(By.XPATH, './/span[@class="priceinfo"]').text
                except:
                    price = "N/A"

                link = result.find_element(By.XPATH, ".//a").get_attribute("href")
                el = result.find_element(By.XPATH, ".//div[@class='meta-line']/div")
                time_posted = driver.execute_script("return arguments[0].childNodes[0].textContent", el)
                location = driver.execute_script("return arguments[0].childNodes[2].textContent", el)

                #image_url = result.find_elements(By.XPATH, f"//img[contains(@src, '{pid}')]")
                image_url = "N/A"

                #print(f"Title: {title}\nPrice: {price}\nLink: {link}\nLocation: {location}\nTime Posted: {time_posted}\nSrc: {img_src}\n")
                data.append({
                    "Title": title,
                    "Price": price,
                    "Link": link,
                    "Location": location,
                    "Time Posted": time_posted,
                    "thumbnail": image_url
                })

            return data
        finally:
            driver.quit()

    def craigslist_detail(self, url: str):
        driver = self.setup_driver()
        driver.get(url)
        driver.implicitly_wait(3)
        try:
            description = driver.find_element(By.XPATH, '//section[@id="postingbody"]').text
        except:
            description = None
        try:
            elements = driver.find_elements(By.XPATH, '//div[@id="thumbs"]/a')
            image_urls = [element.get_attribute('href') for element in elements]
        except:
            image_urls = []

        if len(image_urls) == 0:
            try:
                image_urls = [driver.find_element(By.XPATH, '//div[@class="gallery"]//img').get_attribute('src')]
            except:
                image_urls = []

        try:
            pass
        finally:
            driver.quit()

        data = {
            'Description': description,
            'Image URLs': image_urls
        }
        return data