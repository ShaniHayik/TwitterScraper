
"""
Created by Shani Hayik

This code takes Google’s last 100 tweets from Twitter and provides the following output: 
1. Hashtag list  2. Mention list  3. Word statistics

Please note that 100 tweets might take longer time.
The output will appear in the console after you will start the program.

The task uses google chrome driver version 88.0.4324.96, so if you don't use this version,  
please replace the file of "chromedriver.exe" in the package to your google chrome version driver.
python interpreter: 3.8

thanks!
"""

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import os
import sys


base_dir = os.getcwd() #our current path

def Path(relative_path):
    return os.path.join(base_dir, relative_path)

#init username and password
class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path=Path("chromedriver.exe"))

    def login(self):
        bot = self.bot
        bot.get("https://twitter.com/")
        sleep(3)

        # Send name and password and press on login:
        bot.find_element_by_xpath( #login xpath
            '//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/a[2]/div/span/span'
        ).click()
        sleep(1.5)
        bot.find_element_by_name("session[username_or_email]").send_keys(self.username)
        bot.find_element_by_name("session[password]").send_keys(self.password)
        bot.find_element_by_xpath( #ok xpath
            "//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div/span/span"
        ).click()
        sleep(3)

    def getTop100Tweets(self):
        bot = self.bot
        bot.get("https://twitter.com/Google")
        tweets = []
        i = 200 #num pixels of tweet
        add = True
        while len(tweets) < 100:
            bot.execute_script(f"window.scrollTo(0, {i})")
            i += 600 #num pixels scroll
            sleep(0.17)
            # get tweets
            elems = bot.find_elements_by_css_selector('[data-testid="tweet"]') #find tweet
            for elem in elems:
                add = True
                text = elem.text
                for tweet in tweets:
                    if tweet[3:50] == text[3:50]: #if the tweet already exists in the array
                        add = False
                        break
                if add:
                    tweets.append(text)
                else:
                    pass
        return tweets



bot = TwitterBot("HayikShani", "shani12345")
bot.login()
tweets = bot.getTop100Tweets()


Hashtag_list = []
Mention_list = []

def add_mention(string): #mention list
    index = 0
    for ch in string[1:]:
        if not (ch.isalpha()): #alpha char
            Mention_list.append(string[1 : index + 1])
            return
        index += 1


def add_hashtag(string): #hashtag list
    index = 0
    for ch in string[1:]:
        if not (ch.isalpha()):
            Hashtag_list.append(string[1 : index + 1])
            return
        index += 1


for tweet in tweets:
    string = tweet.encode("utf-8")
    LineIndex = 0
    for line in iter(string.splitlines()):
        if LineIndex >= 4: #without the name and date
            line = str(line)
            for i, ch in enumerate(line):
                if ch == "@": #mention
                    add_mention(line[i:])
                elif ch == "#": #hashtag
                    add_hashtag(line[i:])
        LineIndex += 1


word_statistics = {}
for h in Hashtag_list:
    word_statistics[h] = word_statistics.setdefault(h, 0) + 1 #count num shows of hashtag

for m in Mention_list:
    word_statistics[m] = word_statistics.setdefault(m, 0) + 1

# remove duplicates
Hashtag_list = list(dict.fromkeys(Hashtag_list))
Mention_list = list(dict.fromkeys(Mention_list))

print("\nhashtag list: ", Hashtag_list)
print("\nmention list: ", Mention_list)
print("\nstatistics list: ", sorted(word_statistics.items(), key=lambda x: x[1], reverse=True),) #sort by value


