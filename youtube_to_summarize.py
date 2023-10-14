from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(executable_path=r'C:\Users\samlb\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe')
actions = ActionChains(driver)

number_of_videos = 10
search_queries = ['software-as-a-service', 'SaaS', 'ITSG-33']

for counter in search_queries:
    driver.get("https://www.youtube.com/results?search_query="+counter)

    videos = []
    while(len(videos) < number_of_videos):
        videos = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer.style-scope.ytd-item-section-renderer[bigger-thumbs-style="DEFAULT"]')))
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    videos = videos[0:number_of_videos]
    print(videos)
    print(len(videos))

    for video in videos:

        video_link = WebDriverWait(video, 20).until(EC.presence_of_element_located((By.ID, 'thumbnail'))).get_attribute('href')

        driver.execute_script(f"window.open('{video_link}', '_blank');")

        time.sleep(2)
        
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(10)


    time.sleep(10)
    exit()

# # Wait for the website to load
# time.sleep(3)

# # Locate the search bar
# search_box = driver.find_element_by_name("search_query")

# # Type the search query
# search_term = "Python programming"
# search_box.send_keys(search_term)

# # Submit the search query
# search_box.send_keys(Keys.RETURN)

# # Wait for search results to load
# time.sleep(5)

# # Fetch video titles
# videos = driver.find_elements_by_id("video-title")

# # Print video titles
# for video in videos:
#     print(video.text)

# # Close the browser
# driver.close()
