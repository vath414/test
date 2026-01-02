from seleniumbase import Driver
import json
import time
import random
import os

# ===== Settings =====
SCROLL_SPEED = 10   # pixels per step (lower = slower & smoother)
RUN_TIME = 100      # total scroll duration
LOOPS = 5   
Gif="gif"        # number of processing cycles per account


# ===== Setup Browser =====
def setup():
    """Create a browser and load cookies for the given account"""
    driver = Driver(uc=True)
    driver.get("https://youtu.be/qI5mTOD-or0?si=n-9fzNKvLdTYJgAG")
    time.sleep(2)
    return driver
def test(driver):
    watch=[720,876,902,945,978,1020,1050,1110,1200,1230,1300,1400,1500,1600]
    watch_time=random.choice(watch)
    print(f"⏱️ Watching video for {watch_time} seconds...")
    time.sleep(watch_time)

# ===== Smooth Scrolling =====
def smooth_scroll(driver, duration=RUN_TIME, step=SCROLL_SPEED):
    print("🌀 Scrolling...")
    start = time.time()
    y = 0
    while time.time() - start < duration:
        y += step
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(random.uniform(0.05, 0.1))
    print("🎯 Done scrolling.")


# ===== Like Post =====
def like(driver):
    try:
        like_buttons = driver.find_elements('[data-testid="like"]')
        if like_buttons:
            like_buttons[0].click()
            print("❤️ Liked")
        else:
            print("⚠️ No like buttons found")
    except Exception as e:
        print("❌ Like failed:", e)


# ===== Retweet Post =====
def retweet(driver):
    try:
        retweet_buttons = driver.find_elements('[data-testid="retweet"]')
        if retweet_buttons:
            retweet_buttons[0].click()
            time.sleep(2)
            driver.click_if_visible('//*[text()="Repost"]')
            print("🔁 Retweeted")
        else:
            print("⚠️ No retweet buttons found")
    except Exception as e:
        print("❌ Retweet failed:", e)
def Getstart(driver):
    with open("start.txt","r") as f:
        url=f.readlines()
    for i in url:
        smooth_scroll(driver)
        driver.get(i.strip())
        time.sleep(5)
        try:
            follow_button = driver.find_element('[data-testid$="-follow"]')
            follow_button.click()
            print("✅ Follow button clicked!")
        except Exception as e:
            print("❌ Could not click Follow:", e)
        driver.go_back()
        time.sleep(3)
    print("✅ Done following")
def check():
    videos = sorted(os.listdir(Gif))
    videos = [v for v in videos if v.endswith(".mp4")]
    video=random.choice(videos)
    return video
def post(driver):
    video=check()
    if video is None:
        driver.quit()
        return
    file_path = os.path.abspath(os.path.join(Gif, video))
    time.sleep(3)
    try:
            # 1️⃣ Open compose window
        driver.get("https://x.com/compose/tweet")
        time.sleep(5)
        # try:
        #     driver.click("//button[@aria-label='Choose audience']")
        #     driver.click("(//div[@role='menu']//span)[1]")
        #     time.sleep(1)
        #     # Wait for dropdown options to appea
        # except Exception as e: 
        #     print(e)
            # 2️⃣ Type caption
        driver.type('[aria-label="Post text"]', "Chudai..\n #nsfw #sex #porn #naked #nudes #hentai #squirt #pussy #goon")
        time.sleep(1)
        print("tittle completed")
            # 2️⃣ Type caption
            # 3️⃣ Upload video
        driver.send_keys('input[type="file"]', file_path)
        print("Uploading video...")
        time.sleep(100)  # wait for upload to finish

            # Click Post button
        try:
    # Try normal click first
            driver.click("//span[text()='Post' or text()='Tweet']")
        except Exception:
    # Fallback: use JS click if overlay still intercepts it
            driver.js_click("//span[text()='Post' or text()='Tweet']")
        print("✅ Posted successfully!")
        time.sleep(10)
    except Exception as e:
        print("❌ Error while posting:", e)
    driver.quit()
# ===== Full Process =====
def process(driver, loops=LOOPS):
    """Performs like, retweet, scroll, and refresh repeatedly"""
    for i in range(loops):
        print(f"\n--- Cycle {i + 1}/{loops} ---")
        time.sleep(10)
        driver.execute_script("window.scrollBy(0, 270);")
        time.sleep(2)
        like(driver)
        time.sleep(1)
        retweet(driver)
        time.sleep(2)
        smooth_scroll(driver)
        time.sleep(4)
        driver.refresh()
    print("✅ Done processing")
    time.sleep(5)
    driver.quit()
