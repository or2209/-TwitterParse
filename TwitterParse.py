from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv



class TwitterParse:

    count_tweets = 0
    def __init__(self):
        self.hashtag_list =[]
        self.mention_list = []
        self.avg_length = 0
        self.smallest_length = 1000000
        self.biggest_length = 0
        self.tweet_data = []
        self.count=0

    def extract_mention_list(self, text):
        # initializing hashtag_list variable

        # splitting the text into words
        for word in text.split():

            # checking the first character of every word
            if word[0] == '#':
                # adding the word to the hashtag_list
                self.mention_list.append(word[1:])

    def calculate_length(self, tweet):
        length_tweet = len(tweet)
        self.avg_length += length_tweet
        self.count += 1
        if length_tweet < self.smallest_length:
            self.smallest_length = length_tweet
        if length_tweet > self.biggest_length:
            self.biggest_length = length_tweet

    def get_tweet_data(self, tweet):
        nami = tweet.find_element_by_xpath('.//span').text
        handle = tweet.find_element_by_xpath('.//span[contains(text(),"@")]').text
        try:
            time = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        comment = tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = tweet.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        self.extract_hashtags(responding)
        self.extract_mention_list(responding)

        self.calculate_length(responding)
        replay = tweet.find_element_by_xpath('//div[@data-testid="reply"]').text
        retweet = tweet.find_element_by_xpath('//div[@data-testid="retweet"]').text
        likes = tweet.find_element_by_xpath('//div[@data-testid="like"]').text

        twetts = (nami, handle, time, responding, replay, retweet, likes)
        return twetts

        # function to print all the hashtags in a text

    def extract_hashtags(self, text):
        # initializing hashtag_list variable

        # splitting the text into words
        for word in text.split():

            # checking the first character of every word
            if word[0] == '@':
                # adding the word to the hashtag_list
                self.hashtag_list.append(word[1:])

    def create_output(self):
        print("The hashtags are :")

        for hashtag in self.hashtag_list:
            print('@' + hashtag, end=', ')
        print()

        print("mensions List:")
        for mention in self.mention_list:
            print('#' + mention, end=', ')

        print()
        print("the largest tweet length is:" + str(self.biggest_length))
        print()
        print("the smallest tweet length is:" + str(self.smallest_length))
        print()
        print("the average tweet of length:" + str(self.avg_length))

    def get_data(self,num_of_tweets,driver):
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True

        while scrolling:
            if self.count_tweets == num_of_tweets:
                self.create_output()
                return
            tweets = driver.find_elements_by_css_selector("[data-testid=\"tweet\"]")
            for card in tweets:
                if self.count_tweets == num_of_tweets:
                    self.create_output()
                    return
                data = self.get_tweet_data(card)
                if data:
                    self.tweet_data.append(data)
                    self.count_tweets=self.count_tweets +1


            scroll_attempt = 0

            while True:
                if self.count_tweets == num_of_tweets:
                    self.create_output()
                    return
                # check scroll position
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                sleep(1)
                curr_position = driver.execute_script("return window.pageYOffset")
                if last_position == curr_position:
                    scroll_attempt += 1

                # end of scroll region
                    if scroll_attempt >= 3:
                        if self.count_tweets == num_of_tweets:
                            self.create_output()
                            return
                        scrolling = False
                        break
                    else:
                        sleep(2)  # attempt to scroll again

                else:
                    last_position = curr_position
                    if self.count_tweets == num_of_tweets:
                        self.create_output()
                        return
                    break
            self.create_output()



    def login(self,driver,email_user,username,password,search_term):
        driver.maximize_window()  # For maximizing window
        driver.implicitly_wait(20)  # gives an implicit wait for 20 seconds
        driver.get("https://twitter.com/i/flow/login")
        email = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input')
        email.send_keys(email_user)
        email.click()
        button_next = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div')
        button_next.click()

        # enter user_name
        user_name = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        user_name.send_keys(username)
        btn_user_name = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
        btn_user_name.click()

        # enter the password
        search_password = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')
        search_password.send_keys(password)
        button_password = driver.find_element_by_xpath(
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div')
        button_password.click()

        # # find search input and search for term
        search_input = driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/label/div[2]/div/input')
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)


    def write_csv(self):
        with open('polynote_tweets.csv', 'w', newline='', encoding='utf-8') as f:
             header = ['UserName', 'Handle', 'Timestamp', 'Comments', 'Likes', 'Retweets', 'Text']
             writer = csv.writer(f)
             writer.writerow(header)
             writer.writerows(self.tweet_data)




num_of_tweets = int(input("enter number of tweets"))
driver_path="C:\chrome_driver\chromedriver"
username="or_laharty"
password="or220995"
email_user="orlaharty1@gmail.com"
search_term="@YouTube"
t=TwitterParse()
driver = webdriver.Chrome(executable_path=driver_path)
t.login(driver,email_user,username,password,search_term)
t.get_data(num_of_tweets,driver)
# t.write_csv()

