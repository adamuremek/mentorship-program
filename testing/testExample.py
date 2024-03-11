from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
import pyautogui
from testSuite import Test, TestSuite

'''
THE ENV FILE

Create an ENV file with the following values

URL={The URL you are testing}
TESTER={Your Name}
'''

load_dotenv()

'''Make sure to create your driver with whatever web browser'''
driver = webdriver.Firefox()

'''
TEST METHODS

This is a Test Method. This is where we put our actual testing logic.

In each test method, we must grab and return 3 things (in this order):
- test_passed - Boolean - Did the test pass?
- pre_test_screenshot - pyautogui screenshot - What happened before the test
- post_test_screenshot - pyautogui screenshot - What happened after the test

You don't have to worry about saving the screenshots or doing anything to document
the tests. The TestSuite class will take care of all of it.

This particular test method tests whether or not the site loads.

This test automatically is added to all TestSuites and is run first. 
'''

def testSiteLoad():
    #Navigate to the landing Page
    driver.get(os.getenv("URL"))

    #Grab the pretest screenshot
    pre_test_screenshot = pyautogui.screenshot()

    #Look for the logo and assess whether or not it's there
    logo = None
    try:
        logo = driver.find_element(By.CLASS_NAME, "logo")
    except:
        logo = None
    
    test_passed = logo != None

    #Grab the posttest screenshot
    post_test_screenshot = pyautogui.screenshot()

    #Return the tuple of all three in this order
    return test_passed, pre_test_screenshot, post_test_screenshot

if __name__ == "__main__":
    #Create Test Suite with name and driver object.
    suite = TestSuite("Test Test Suite", driver)
    #Load the tests into the testSuite({TestID}{Test Name}{Function Name})
    suite.addTest(Test("Load1", "Site Load Test", testSiteLoad))
    suite.addTest(Test("Load2", "Site Load Test", testSiteLoad))
    suite.addTest(Test("Load3", "Site Load Test", testSiteLoad))

    #Run the test suite by calling this method
    suite.runTestSuite()

    #All testing metrics are stored within the suite.
    #So, when you're ready to output a CSV, call this method.
    suite.generateResultReport('./testresults')

    