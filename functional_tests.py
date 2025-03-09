from selenium import webdriver
import unittest 
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User hears about the online to-do list and decides to check out the home page  
        self.browser.get('http://localhost:8000')
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header.txt)

        # She is invited to enter a to-do item straight away 
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 
            'Enter a to-do item'
        )
        
        # She types "go to the store" into a text box
        inputbox.send_keys('go to the store')

        # She hits enter, the page updates, and now the page lists 
        ## "1: Go to the store" as the first item in a to-do list 
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertTrue(
                any(row.text == '1: go to the store' for row in rows)
        )

        # The text box still exists, so she uses it again. 
        ## She enters, "grab apples from the fruit section"
        self.fail('finish the test')

        # The page updates again and shows both items on her list 

        # User wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for her -- there is some explanatory text to that effect. 

        # she visits that URL - her to-do list is still there. 

        # She closes the website. 

        browser.quit() 
if __name__ == '__main__':
    unittest.main(warnings='ignore')


