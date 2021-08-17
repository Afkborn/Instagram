from logging import currentframe
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import time
from json import dumps, load
from urllib.request import urlretrieve
import datetime as dt
from time import sleep,time
import sqlite3  as sq
from os import getcwd, mkdir, path, system, remove,rmdir
from hashlib import md5
from shutil import rmtree

LOGINUSERNAMEXPATH = "//*[@id='loginForm']/div/div[1]/div/label/input"
LOGINPASSWORDXPATH = "//*[@id='loginForm']/div/div[2]/div/label/input"
LOGINBUTTONXPATH = "//*[@id='loginForm']/div/div[3]/button"
FOLLOWİNGXPATH = "//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span"
FOLLOWERSXPATH = "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span"
EDITUSERNAMEXPATH = "//*[@id='react-root']/section/main/div/article/div/div[2]/h1"
POSTCOUNTXPATH = "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span"
PPXPATH = "//*[@id='react-root']/section/main/div/header/div/div/div/button/img"
NAMEXPATH = "//*[@id='pepName']"
EMAILXPATH = "//*[@id='pepEmail']"
TELXPATH = "//*[@id='pepPhone Number']"

MAINURL  = "https://www.instagram.com/"
LOGINPAGEURL = "accounts/login/"
EDITURL = "accounts/edit/"


NOTIFICATIONTEXT= "Bildirimleri Aç"


FOLDERS = ["chromeProfile", "usersLog"]
USERSLOGFOLDER = ["myFollowing","myFollowers","pictures","unfollowers","didnotfollow"]
USERSLOGPICTURESFOLDER = ["myPP","myFollowingPP","myFollowersPP","myPost","otherPost"]


class Instagram:
    
    __isLogin = False
    isGetMyFollowers = False
    isGetMyFollowing = False
    isPasswordMatch = False
    isLoadOldFollowersTable = False
    isLoadOldFollowingTable = False
    isLoadLastFollowingDB = False
    isLoadLastFollowersDB = False
    EXECUTABLEPATH = r"driver\chromedriver.exe"
    
    def __init__(self,username,password,headless = False):
        self.username = username
        self.password = password
        self.passMd5 = md5(self.password.encode()).hexdigest()

        self.__checkJson()
        if self.isPasswordMatch: self.__checkOldData()


        for i in FOLDERS:
            if not path.exists(getcwd() + "\\" + i):
                mkdir(i)
        

        options = ChromeOptions()
        options.add_argument(f"user-data-dir={getcwd()}\chromeProfile")
        options.add_argument("--log-level=3")
        options.headless = headless
        self.browser = Chrome(executable_path=self.EXECUTABLEPATH,options=options)
        self.browser.set_window_position(0,0)
        self.browser.set_window_size(1024,768)


        self.browser.get(MAINURL + LOGINPAGEURL) 
        sleep(2)
        if self.browser.current_url != MAINURL + LOGINPAGEURL:
            self.__isLogin = True
        else:
            self.__login()

            sleep(4)
            self.browser.get(MAINURL + LOGINPAGEURL)
            sleep(2)
            if self.browser.current_url != MAINURL + LOGINPAGEURL:
                self.__isLogin = True
            else:
                print("username or password is incorrect")
                self.__isLogin = False
                self.browser.close()
        
        self.__getAccountDetail()

        print(f"Login: {self.__isLogin}\nUsername: {self.username}")
        if self.__isLogin:
            self.browser.get(MAINURL + self.username)
            sleep(2)
            self.followersCount = self.browser.find_element_by_xpath(FOLLOWERSXPATH).get_attribute('title')
            self.followingCount = self.browser.find_element_by_xpath(FOLLOWİNGXPATH).text
            self.postCount = self.browser.find_element_by_xpath(POSTCOUNTXPATH).text
            self.profilePictureUrl = self.browser.find_element_by_xpath(PPXPATH).get_attribute('src')

            if not path.exists(getcwd() + fr"\usersLog\\{self.username}"):
                mkdir(fr"usersLog\{self.username}")
            for i in USERSLOGFOLDER:
                if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\{i}"):
                    mkdir(fr"usersLog\{self.username}\\{i}")
            for i in USERSLOGPICTURESFOLDER:
                if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\{i}"):
                    mkdir(fr"usersLog\{self.username}\\pictures\\{i}")

            try:
                location = fr"\usersLog\{self.username}\pictures\myPP\pp-{self.__getTimeTimeInt()}.png"
                urlretrieve(self.profilePictureUrl, (getcwd() + location))
                self.profilePictureLocal = (getcwd() + location)
            except:
                print("Profile picture could not be downloaded, please try again later.")
                self.profilePictureLocal = None

            print(f"Followers Count: {self.followersCount}\nFollowing Count: {self.followingCount}\nPost Count: {self.postCount}\n")
            jsonDataSet = {
                "time" : time(),
                "username" : self.username,
                "password" : self.passMd5,
                "name" : self.name,
                "email" : self.email,
                "telephoneNumber" : self.telephoneNumber,
                "ppURL" : self.profilePictureUrl,
                "ppLocal" : self.profilePictureLocal,
                "followersCount" : self.followersCount,
                "followingCount" : self.followingCount,
                "postCount" : self.postCount
            }
            jsonDump = dumps(jsonDataSet)
            with open(getcwd() + fr"\usersLog\\{self.username}\\userlog.json","w") as json:
                json.write(jsonDump)

    def __login(self):
        self.browser.find_element_by_xpath(
            LOGINUSERNAMEXPATH).send_keys(self.username)
        self.browser.find_element_by_xpath(
            LOGINPASSWORDXPATH).send_keys(self.password)
        self.browser.find_element_by_xpath(
            LOGINBUTTONXPATH).send_keys(Keys.ENTER)       

    def __getAccountDetail(self):
        self.browser.get(MAINURL + EDITURL)
        sleep(2)
        if self.browser.find_element_by_xpath(EDITUSERNAMEXPATH).text == self.username:
            self.name = self.browser.find_element_by_xpath(NAMEXPATH).get_attribute("value")
            self.email = self.browser.find_element_by_xpath(EMAILXPATH).get_attribute("value")
            self.telephoneNumber = self.browser.find_element_by_xpath(TELXPATH).get_attribute("value")
        else:
            self.__isLogin = False
            print("Please try again")
            self.browser.close()
            rmtree(fr"{getcwd()}\chromeProfile")

    def __checkJson(self):
        if path.exists(getcwd() + fr"\usersLog\{self.username}\userlog.json"): 
            try:
                jsonUser = load(open(getcwd() + fr"\usersLog\{self.username}\userlog.json"))
                self.isPasswordMatch = True  if self.passMd5 == jsonUser["password"] else False
            except:
                self.isPasswordMatch = False

    def __checkOldData(self):
        if path.exists(getcwd() + fr"\usersLog\{self.username}\myFollowers\myFollowers.db"):
            vt=sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowers\myFollowers.db")
            im = vt.cursor()
            im.execute("SELECT name FROM sqlite_master WHERE type='table';")
            curr_table = im.fetchall()
            tableNames = curr_table[0]
            timeList = []
            for i in tableNames:
                timeList.append(i)
            self.lastFollowersTableName = max(timeList)     
            self.isLoadOldFollowersTable = True
            vt.close()      
        if path.exists(getcwd() + fr"\usersLog\{self.username}\myFollowing\myFollowing.db"):
            vt=sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowing\myFollowing.db")
            im = vt.cursor()
            im.execute("SELECT name FROM sqlite_master WHERE type='table';")
            curr_table = im.fetchall()
            tableNames = curr_table[0]
            timeList = []
            for i in tableNames:
                timeList.append(i)
            self.lastFollowingTableName = max(timeList)
            self.isLoadOldFollowingTable = True
            vt.close()

    def __getTimeTimeInt(self):
        return int(time() * 1e6)

    def __getTimeForSave(self):
        parser = dt.datetime.now()
        return parser.strftime("%d.%m.%Y.%H-%M-%S")

    def __checkNotification(self):
        isShow = False
        try:
            notificationText = self.browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/h2').text
            if notificationText == NOTIFICATIONTEXT:
                isShow = True
        except Exception as e:
            print(f"Check notification error detail: {e}")
        return isShow

    def __click(self,x,y):
        action = ActionChains(self.browser)
        action.move_by_offset(x,y)
        action.click()
        action.perform()
        action.reset_actions()

# TODO HATA VERİYOR ÇÖZ
    def downloadMyFollowingPP(self,useOldData = False):
        if useOldData:
            
            if not self.isLoadLastFollowingDB:
                print("You cant use old data!")
            else:
                self.getMyFollowingFromDB()
        else:
            self.getMyFollowing()
        
        for index,(_,src,_,username) in enumerate(self.followingList,start=1):
            if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\myFollowingPP\\{username}"):
                mkdir(( getcwd() + fr"\usersLog\\{self.username}\\pictures\\myFollowingPP\\{username}"))
            location = fr"\usersLog\{self.username}\pictures\myFollowingPP\{username}\pp-{self.__getTimeTimeInt()}.png"
            urlretrieve(src, (getcwd() + location))
            print(f"Downloading {username}'s photo. ({index} of {len(self.followersList)})")

# TODO HATA VERİYOR ÇÖZ
    def downloadMyFollowersPP(self,useOldData = False):
        if useOldData:

            if not self.isLoadLastFollowersDB:
                print("You cant use old data!")
            else:
                self.getMyFollowersFromDB()
        else:
            self.getMyFollowers()
        
        for index ,(_,src,_,username) in enumerate(self.followersList,start=1):
            if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\myFollowersPP\\{username}"):
                mkdir((getcwd() + fr"\usersLog\\{self.username}\\pictures\\myFollowersPP\\{username}"))
            location = fr"\usersLog\{self.username}\pictures\myFollowersPP\{username}\pp-{self.__getTimeTimeInt()}.png"
            urlretrieve(src, (getcwd() + location))
            print(f"Downloading {username}'s photo. ({index} of {len(self.followersList)})")

    def getMyFollowing(self,saveInFile = False):
        self.followingList = []
        if self.__isLogin:
            sleep(2)
            if self.browser.current_url == (MAINURL + self.username + "/"):
                self.browser.find_element_by_xpath(FOLLOWİNGXPATH).click()
            else:
                self.browser.get(MAINURL + self.username)
                sleep(2)
                self.browser.find_element_by_xpath(FOLLOWİNGXPATH).click()
            sleep(2)
            action = ActionChains(self.browser)
            dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
            control = True
            lastLastElement = ""
            count = 0
            while control:
                #dialog.click()
                self.__click(580,230)
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                allElement = dialog.find_elements_by_css_selector("li")
                lastElement = str(allElement[-1]).replace("<selenium.webdriver.remote.webelement.WebElement "," ").replace(">","").strip()[54:90]
                print(f"Login: {self.__isLogin}\nUsername: {self.username}")
                print(f"Followers Count: {self.followersCount}\nFollowing Count: {self.followingCount}\n")
                print(f"Getting Followers: {len(allElement)} of {self.followingCount}")
                if lastLastElement == lastElement:
                    if count == 5 :
                        control = False
                    elif len(allElement) == self.followersCount:
                        control = False
                    count += 1
                lastLastElement = lastElement
                sleep(1)
            allElement = dialog.find_elements_by_css_selector("li")
            liCount = 1
            for user in allElement:
                try:
                    name = self.browser.find_element_by_xpath(f'/html/body/div[5]/div/div/div[3]/ul/div/li[{liCount}]/div/div[1]/div[2]/div[2]').text
                    name = name.replace("'","")
                except:
                    name = "null"
                src = user.find_element_by_css_selector("img").get_attribute("src")
                link = user.find_element_by_css_selector("a").get_attribute("href")  
                username = link.replace("https://www.instagram.com/","").replace("/","")
                liCount+=1
                self.followingList.append((link,src,name,username))
            self.isGetMyFollowing=True
            if saveInFile:
                vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowing\myFollowing.db")
                im = vt.cursor()
                sqlTime = time()
                sql = f"CREATE TABLE IF NOT EXISTS '{sqlTime}' ('id', 'username','srcUrl','url','name')"
                im.execute(sql)
                id = 1
                for url,src,name,username in self.followingList:
                    degerGir = f"INSERT INTO '{sqlTime}' VALUES ('{id}', '{username}','{src}','{url}','{name}')"
                    im.execute(degerGir)
                    id+=1
                vt.commit()
                vt.close()
            else:
                return self.followingList
            
        else:
            print("you must login first")

    def getMyFollowingFromDB(self):
        if self.isLoadOldFollowingTable:
            self.followingList = []
            vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowing\myFollowing.db")
            im = vt.cursor()
            im.execute(f"SELECT * FROM '{self.lastFollowingTableName}'")
            veriler = im.fetchall()
            vt.close()
            for i in veriler:
                _ , username , srcUrl , url , name = i
                self.followingList.append((url,srcUrl,name,username))
            self.isLoadLastFollowingDB = True
            return self.followingList
        else:
            print("Error (is load old following table?)")

    def getMyFollowersFromDB(self):
        if self.isLoadOldFollowersTable:
            self.followersList = []
            vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowers\myFollowers.db")
            im = vt.cursor()
            im.execute(f"SELECT * FROM '{self.lastFollowersTableName}'")
            veriler = im.fetchall()
            vt.close()
            for i in veriler:
                _ , username , srcUrl , url , name = i
                self.followersList.append((url,srcUrl,name,username))
            self.isLoadLastFollowersDB = True
            return self.followersList
        else:
            print("Error (is load old followers table?)")
        
    def getMyPost(self):
        if self.__isLogin:
            sleep(2)
            if not self.browser.current_url == (MAINURL + self.username + "/"):
                self.browser.get(MAINURL + self.username)
                sleep(2)
            article = self.browser.find_elements_by_xpath('/html/body/div[1]/section/main/div/div[3]/article/div/div/div')
            hrefList = []
            for i in article:
                href = i.find_element_by_css_selector("a").get_attribute("href")
                hrefList.append(href)
            imgSrcList = []
            for i in hrefList:
                self.browser.get(i)
                sleep(2)
                imgSrc = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/div/div/div[1]/img').get_attribute("src")
                imgSrcList.append(imgSrc)
            saveTime = self.__getTimeForSave()
            if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\myPost\\{saveTime}"):
                mkdir((getcwd() + fr"\usersLog\\{self.username}\\pictures\\myPost\\{saveTime}"))
            postC = 1
            for i in imgSrcList:
                location = fr"\usersLog\{self.username}\pictures\myPost\{saveTime}\post{postC}.png"
                urlretrieve(i, (getcwd() + location))
                postC +=1
            exit()
        else:
            print("you must login first")

    def getPost(self,usernameOther):
        #post sayısını al eğer post sayısı fazla ise bu işleim uzun süreceğini söyle. 
        if self.__isLogin:
            sleep(2)
            if not self.browser.current_url == (MAINURL + usernameOther + "/"):
                self.browser.get(MAINURL + usernameOther)
                sleep(2)
            userPostCount = int(self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text)

            if userPostCount > 20:
                pass # sayfayı aşşağı kayddırmak gerekiyor. 
            else:
                article = self.browser.find_elements_by_xpath('/html/body/div[1]/section/main/div/div[3]/article/div/div/div')
                hrefList = []
                for i in article:
                    for j in i.find_elements_by_css_selector("a"):
                        href = j.get_attribute("href")
                        hrefList.append(href)
                imgSrcList = []
                for i in hrefList:
                    self.browser.get(i)
                    sleep(2)
                    imgSrc = self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/div/div/div[1]/img').get_attribute("src")
                    imgSrcList.append(imgSrc)
                saveTime = self.__getTimeForSave()
                if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\otherPost\\{usernameOther}"):
                    mkdir((getcwd() + fr"\usersLog\\{self.username}\\pictures\\otherPost\\{usernameOther}"))
                if not path.exists(getcwd() + fr"\usersLog\\{self.username}\\pictures\\otherPost\\{usernameOther}\\{saveTime}"):
                    mkdir((getcwd() + fr"\usersLog\\{self.username}\\pictures\\otherPost\\{usernameOther}\\{saveTime}"))
                postC = 1
                for i in imgSrcList:
                    location = fr"\usersLog\{self.username}\pictures\otherPost\{usernameOther}\{saveTime}\post{postC}.png"
                    urlretrieve(i, (getcwd() + location))
                    postC +=1
        else:
            print("you must login first")

    def getDifference(self, useOldData = False, saveInFile = False):
        if self.__isLogin:
            myFollowingUsername = []
            myFollowersUsername = []
            if useOldData:
                if not self.isLoadLastFollowersDB: self.getMyFollowersFromDB()
                if not self.isLoadLastFollowingDB: self.getMyFollowingFromDB()
            else:
                if not self.isGetMyFollowers:
                    self.getMyFollowers(True)
                if not self.isGetMyFollowing:
                    self.getMyFollowing(True)

            for _,_,_,username in self.followingList:
                myFollowingUsername.append(username)
            for _,_,_,username in self.followersList:
                myFollowersUsername.append(username)
                
            self.unfollowers = list(set(myFollowingUsername) - set(myFollowersUsername))
            self.didnotfollow = list(set(myFollowersUsername) - set(myFollowingUsername))
            
            print(f"My Following: {myFollowingUsername}\n\n\n")
            print(f"My Followers: {myFollowersUsername}\n\n\n")
            print(f"Unfollowers: {self.unfollowers}\n\n\n") #takip etmeyenler
            print(f"Didnot follow: {self.didnotfollow}\n\n\n") #takip etmediklerim

            if saveInFile:
                vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\unfollowers\unfollowers.db")
                im = vt.cursor()
                sqlTime = time()
                sql = f"CREATE TABLE IF NOT EXISTS '{sqlTime}' ('id', 'username','srcUrl','url','name')"
                im.execute(sql)
                id = 1
                for i in self.unfollowers:
                    # sadece bir tane username geldi yazilimturk
                    for url,src,name,username in self.followingList:
                        if username == i:
                            degerGir = f"INSERT INTO '{sqlTime}' VALUES ('{id}', '{username}','{src}','{url}','{name}')"
                            im.execute(degerGir)
                            id+=1
                            vt.commit()
                vt.close()
                vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\didnotfollow\didnotfollow.db")
                im = vt.cursor()
                sqlTime = time()
                sql = f"CREATE TABLE IF NOT EXISTS '{sqlTime}' ('id', 'username','srcUrl','url','name')"
                im.execute(sql)
                id = 1
                for i in self.didnotfollow:
                    # sadece bir tane username geldi yazilimturk
                    for url,src,name,username in self.followersList:
                        if username == i:
                            degerGir = f"INSERT INTO '{sqlTime}' VALUES ('{id}', '{username}','{src}','{url}','{name}')"
                            im.execute(degerGir)
                            id+=1
                            vt.commit()
                vt.close()
                
            
        else:
            print("you must login first")

    def getMyFollowers(self,saveInFile = False):
        self.followersList = []
        if self.__isLogin:
            sleep(2)
            if self.browser.current_url == (MAINURL + self.username + "/"):
                self.browser.find_element_by_xpath(FOLLOWERSXPATH).click()
            else:
                self.browser.get(MAINURL + self.username)
                sleep(2)
                self.browser.find_element_by_xpath(FOLLOWERSXPATH).click()
            sleep(2)
            action = ActionChains(self.browser)
            dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")

            control = True
            lastLastElement = ""
            count = 0
            while control:
                #dialog.click()
                self.__click(611,183)
                action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                allElement = dialog.find_elements_by_css_selector("li")
                lastElement = str(allElement[-1]).replace("<selenium.webdriver.remote.webelement.WebElement "," ").replace(">","").strip()[54:90]
                print(f"Login: {self.__isLogin}\nUsername: {self.username}")
                print(f"Followers Count: {self.followersCount}\nFollowing Count: {self.followingCount}\n")
                print(f"Getting Followers: {len(allElement)} of {self.followersCount}")
                if lastLastElement == lastElement:
                    if count == 5 :
                        control = False
                    elif len(allElement) == self.followersCount:
                        control = False
                    count += 1
                lastLastElement = lastElement
                sleep(1)
            allElement = dialog.find_elements_by_css_selector("li")
            liCount = 1
            for user in allElement:
                try:
                    name = self.browser.find_element_by_xpath(f'/html/body/div[6]/div/div/div[2]/ul/div/li[{liCount}]/div/div[1]/div[2]/div[2]').text
                    name = name.replace("'","")
                except:
                    name = "null"
                link = user.find_element_by_css_selector("a").get_attribute("href")  
                src = user.find_element_by_css_selector("img").get_attribute("src")
                username = link.replace("https://www.instagram.com/","").replace("/","")
                self.followersList.append((link,src,name,username))
                liCount+=1
            self.isGetMyFollowers=True
            if saveInFile:
                vt = sq.connect(getcwd() + fr"\usersLog\{self.username}\myFollowers\myFollowers.db")
                im = vt.cursor()
                sqlTime = time()
                sql = f"CREATE TABLE IF NOT EXISTS '{sqlTime}' ('id', 'username','srcUrl','url','name')"
                im.execute(sql)
                id = 1
                for url,src,name,username in self.followersList:
                    degerGir = f"INSERT INTO '{sqlTime}' VALUES ('{id}', '{username}','{src}','{url}','{name}')"
                    im.execute(degerGir)
                    id+=1
                vt.commit()
                vt.close()
                return self.followersList
            else:
                return self.followersList
        else:
            print("you must login first")

    def changeDriverPath(self,path):

        self.EXECUTABLEPATH = path

    def getLoginStatus(self):
        """Return login status as boolean"""
        return self.__isLogin

    def logOut(self):
        """Logs out of the current account"""
        if self.__checkNotification():
            self.__click(504,460)
        self.__click(950,27)
        sleep(0.1)
        self.__click(806,226)
        sleep(2)
        self.browser.get(MAINURL + LOGINPAGEURL) 
        if self.browser.current_url != MAINURL + LOGINPAGEURL:
            self.__isLogin = True
        else:
            self.__isLogin = False
        return not self.__isLogin
        
    def closeBrowser(self):
        """Closes the browser"""
        self.browser.close()



    
if __name__ == "__main__":
    pass