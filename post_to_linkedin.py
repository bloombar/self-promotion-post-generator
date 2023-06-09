#! /usr/bin/env python3

import os, time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
  '''
  This script will post a message and image to LinkedIn
  '''
  load_dotenv() # load environment variables from .env file... see README.md for details

  # post content... update this with your own files generated by the `generate_post.py` script.
  image_path = os.path.abspath('./posts/20230325-012748-image.png') # absolute path to one of the images you've generated
  message = "Hey everyone, I'm excited to announce that our environmentally-friendly product has won an award at the EcoLaunch Expo in Seattle on June 1st - I am humbled and grateful for the recognition! #innovativeeducation #codingpower #ecofriendly #productlaunch"

  # create untraceable headless browser
  options = webdriver.ChromeOptions()
  # remove traceable features
  options.add_argument('--disable-gpu')
  options.add_argument('--no-sandbox')
  # options.add_argument('--headless')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--disable-extensions')
  options.add_argument('--disable-infobars')
  options.add_argument('--window-size=1920x1080')
  options.add_argument('--disable-notifications')
  options.add_argument('--disable-browser-side-navigation')

  # delete caching
  options.add_argument('--disable-cache')
  options.add_argument('--disable-application-cache')
  options.add_argument('--disable-offline-load-stale-cache')
  options.add_argument('--disk-cache-size=0')
  options.add_argument('--disable-background-networking')
  options.add_argument('--disable-default-apps')
  options.add_argument('--disable-extensions')
  options.add_argument('--disable-sync')
  options.add_argument('--disable-translate')
  options.add_argument('--hide-scrollbars')
  options.add_argument('--metrics-recording-only')
  options.add_argument('--mute-audio')
  options.add_argument('--no-first-run')
  options.add_argument('--safebrowsing-disable-auto-update')

  # create browser
  browser = webdriver.Chrome(options=options)
  browser.implicitly_wait(10) # timeout in seconds

  #linkedin credentials
  email = os.getenv('LINKEDIN_EMAIL_ADDRESS')
  password =os.getenv('LINKEDIN_PASSWORD')

  # login to linkedin
  browser.get('https://www.linkedin.com/login')
  time.sleep(random.randint(1, 3))
  browser.find_element(by=By.NAME, value='session_key').send_keys(email)
  #sleep a few seconds
  time.sleep(random.randint(1, 5))
  browser.find_element(by=By.NAME, value='session_password').send_keys(password)
  time.sleep(random.randint(1, 5))
  browser.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Sign in').click()

  # pause
  time.sleep(random.randint(3, 5))

  # fill in post form
  browser.find_element(by=By.CLASS_NAME, value='share-box-feed-entry__trigger').click() # click to open post overlay
  time.sleep(random.randint(1, 3))
  browser.find_element(by=By.CLASS_NAME, value='ql-editor').send_keys(message) # add message
  time.sleep(random.randint(3, 5))
  # not sure why, but sometimes the image upload button is not found, so we need to try a few different ways to find it
  # seems that LinkedIn is trying to make this hard to hack... ha!  silly battle to pick.
  try:
    browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/span[1]/button').click() # click image upload button
    print('1 1')
  except:
    try:
      browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/span[1]').click() # click image upload button
      print('1 2')
    except:
      try:
        browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[1]').click() # click image upload button
        print('1 3')
      except:
        print("No image upload button found... bailing out!")
        return # failure!  exit
        pass
  time.sleep(random.randint(1, 3))

  # upload image... this seems to generally work, but sometimes fails probably related to the problem above... still figuring it out
  try:
    browser.find_element(by=By.CSS_SELECTOR, value='input[type="file"]').send_keys(image_path) # select image
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(random.randint(1, 3))
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    print('2 1')
  except:
    print('Error uploading image.... bailing out!')
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    # return # failure!  exit
    pass
  time.sleep(random.randint(1, 3))

  # submit the form... this fails sometimes also probably in relation to the image upload problem bove... still figure it out
  try:
    browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[4]/button').click() # submit!
    print('3 1')
  except:
    try:
      browser.find_element(by=By.XPATH, value='/html/body/div[3]/div/div/div/div[2]/div/div[2]/div[2]/div[4]').click() # submit!
      print('3 2')
    except:
      print('Error submitting post... bailing out!')
      pass
  time.sleep(random.randint(1, 3))

  # close selenium browser
  browser.close()
  exit()

if __name__ == '__main__':
  main()
