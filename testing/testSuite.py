from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import time
import os

console_line = '=' * 100

class Test:
    def __str__(self) -> str:
        '''
        Description
        -----------
        Converts the object into a human readable string ready for a CSV File.

        Returns
        -------
        Delimited string with all the information for a CSV File.
        
        Authors
        -------
        Garrett Mai,
        Cody Syring
        '''
                
        return f"{self.test_id},{self.test_name},{self.passed},{self.time_taken},{self.timestamp},{self.tester}"
        
    def __init__(self, test_id : str, test_name : str, test_function) -> None:
        '''
        Description
        -----------
        Initialize the Test object with all it's default values.

        Parameters
        ----------
        - test_id (string): The identifier for the test
        - test_name (string): A short description of the test
        - test_function (reference to function): The method that should be run as part of the function

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''

        self.test_id = test_id
        self.test_name = test_name
        self.test_function = test_function
        self.time_taken = 0
        self.timestamp = None
        self.passed = False
        self.tester = os.getenv('TESTER')

    def runTest(self):
        '''
        Description
        -----------
        Run the test and collect testing metrics

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''

        #Run the test and grab the result tuple
        print(f'Running {self.test_id}...')
        start = time.time()
        result = self.test_function()
        end = time.time()

        self.passed = result[0]

        #If it didn't pass, we need to save the screenshots
        if not self.passed:
            #Check for the screenshots subdirectory
            if not os.path.isdir("./Screenshots"):
                os.mkdir("./Screenshots") #Create it if it doesn't exist

            #Save the screenshots
            result[1].save(f"./Screenshots/test{self.test_id}pretest.png")
            result[2].save(f"./Screenshots/test{self.test_id}posttest.png")

        #Calculate the time taken and document when the test was done
        self.time_taken = float(f"{end - start:.2f}")
        self.timestamp = datetime.now()

class TestSuite:
    def _private_add_load_site(self) -> None:
        '''
        Description
        -----------
        A private method that creates a test to spin up the browser and test loading.

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''

        #The Function should load the site, thus getting the browser up,
        #and should return whether or not it loaded
        def load_site():
            self.driver.get(os.getenv("URL"))

            logo = None
            try:
                logo = self.driver.find_element(By.CLASS_NAME, "logo")
            except:
                logo = None
            
            test_passed = logo != None

            print('SITE LOADED.')

            return test_passed, 0, 0 #Must pass back a tuple
        
        #Finally, create the test and add it to the list
        self._private_tests.append(Test("LOAD SITE", "I Am Loading the site", load_site))

    def __init__(self, test_suite_name : str, driver : webdriver):
        '''
        Description
        -----------
        Create the test suite with the specified information. 

        Parameters
        ----------
        - test_suite_name (string): The name of the test suite.
        - driver (webdriver onject): The web driver used to interact with the browser.

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''
        
        #Set the object's values to the given values
        self.name = test_suite_name
        self._private_tests = []
        self.driver = driver

        #Add the loader function
        self._private_add_load_site()

    def addTest(self, new_test : Test) -> None:
        '''
        Description
        -----------
        Add a test to the suite.

        Parameters
        ----------
        - new_test (Test): The test that we want to add to the suite. 

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''

        #add the test to the list
        self._private_tests.append(new_test)

    def runTestSuite(self) -> None:
        '''
        Description
        -----------
        Run each test in the test suite.

        Authors
        -------
        Garrett Mai
        Cody Syring
        '''

        print(f'\n{console_line}')

        print(f'Running Suite: {self.name}')
        for i in range(len(self._private_tests)):
            self._private_tests[i].runTest()

        print(f'{console_line}\n')

    def generateResultReport(self, directory : str):
        

        print(f'\n{console_line}')
        print('Generating File...')
        file = None
        timestamp = datetime.now()

        #Either create the file, or create the directory and the file
        try:
            file = open(f"{directory}\{self.name}{timestamp.year}{timestamp.month:02d}{timestamp.day:02d}.csv", "w")
        except:
            os.mkdir(directory)
            try:
                file = open(f"{directory}\{self.name}{timestamp.year}{timestamp.month:02d}{timestamp.day:02d}.csv", "w")
            except:
                raise FileNotFoundError()

        #Write each line into the file
        for i in range(len(self._private_tests)):
            file.write(f"{self._private_tests[i]}\n")

        #close up and let the people know what's up
        file.close()

        print(f"File Saved at {directory}\{self.name}{timestamp.year}{timestamp.month:02d}{timestamp.day:02d}.csv")
        print(f'{console_line}\n')
