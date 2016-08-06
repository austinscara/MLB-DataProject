from selenium import webdriver
import time

chrome_profile = webdriver.ChromeOptions()
profile = {"download.default_directory" : r"C:\Users\Austi\Documents\MLB DataProject\MLB_Data_CSV_Files"}
chrome_profile.add_experimental_option("prefs", profile)


driver = webdriver.Chrome(r"C:\Users\Austi\Documents\MLB DataProject\chromedriver\chromedriver.exe", chrome_options=chrome_profile)
driver.implicitly_wait(10)
driver.get("http://www.baseball-reference.com/players/j/jeterde01-bat.shtml")

x = driver.find_element_by_xpath('//*[@id="all_standard_batting"]')
x.click()
time.sleep(5)
driver.quit()



# link = driver.find_element_by_link_text("Export")click()