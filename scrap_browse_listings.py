import selenium
import selenium.webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_listings(driver: selenium.webdriver, listings_url: str):
    driver.get(listings_url)
    search_results = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-pid]")))
    for result in search_results:

        pid = result.get_attribute("data-pid")

        title = result.find_element(By.XPATH, ".//a/span").text
        try: price = result.find_element(By.XPATH, './/span[@class="priceinfo"]').text
        except: price = "N/A"
        link = result.find_element(By.XPATH, ".//a").get_attribute("href")
        el = result.find_element(By.XPATH, ".//div[@class='meta-line']/div")
        time_posted = driver.execute_script("return arguments[0].childNodes[0].textContent", el)
        location = driver.execute_script("return arguments[0].childNodes[2].textContent", el)

        try:
            # HOVER OVER THE RESULT
            hover = ActionChains(driver).move_to_element(result)
            hover.perform()

            try:
                # CLICK ON THE ELEMENT BY CLASS NAME "slider-forward-arrow" IF FOUND IN THE RESULT
                # THIS WILL LOAD ALL THE THUMBNAILS FOR THAT LISTING
                next_arrow = result.find_element(By.CLASS_NAME, "slider-forward-arrow")
                if next_arrow:
                    next_arrow.click()

                driver.implicitly_wait(1)
            except:
                pass

            # EXTRACT IMAGE URLs
            image_elements = result.find_elements(By.XPATH, f".//img[contains(@src, '{pid}')]")
            image_url = [image.get_attribute("src") for image in image_elements]
        except:
            image_url = []

        print(f"Title: {title}\nPrice: {price}\nLink: {link}\nLocation: {location}\nTime Posted: {time_posted}\n\nThumbnails: {image_url}\n\n")
        yield {
            "Title": title,
            "Price": price,
            "Link": link,
            "Location": location,
            "Time Posted": time_posted,
            "thumbnails": image_url
        }


def main():
    listings_url = "https://honolulu.craigslist.org/search/mau/ela#search=2~gallery~0"
    driver = selenium.webdriver.Chrome()
    results = list(get_listings(driver, listings_url))
    print(results)
    driver.quit()



if __name__ == "__main__":
    main()