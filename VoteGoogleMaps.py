import logging
import os
import random
import shutil
import tempfile
from random import randint
import filetype
import undetected_chromedriver.v2 as uc
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread,pyqtSignal
from PyQt6 import uic
from selenium import webdriver
from time import sleep
import requests
import json
import uuid
import requests
from selenium.webdriver import Keys
import pyperclip
_count = -1

class UI(QMainWindow):
    def __init__(self,hsd = ''):
        super(UI, self).__init__()
        uic.loadUi("DATA/untitled.ui", self)
        self.pushButton = self.findChild(QPushButton,'pushButton')
        self.pushButton.clicked.connect(self.letStart)
        self.pushButton_2 = self.findChild(QPushButton,'pushButton_2')
        self.pushButton_2.clicked.connect(self.stop)
        self.tableWidget = self.findChild(QTableWidget,'tableWidget')
        self.label_3 = self.findChild(QLabel,'label_3')
        self.label_3.setText(f'Tool Bản Quyền Thuộc Về Hữu Chris . Ngày hết hạn : {hsd}')
        self.spinBox = self.findChild(QSpinBox,'spinBox')
        self.checkBox = self.findChild(QCheckBox,'checkBox')
        self.checkBox_2 = self.findChild(QCheckBox,'checkBox_2')
        self.checkBox_3 = self.findChild(QCheckBox,'checkBox_3')
        self.checkBox_4 = self.findChild(QCheckBox,'checkBox_4')
        self.childStartThread = {}
        self.setTableWidget()
        self.show()

    # Start Thread
    def letStart(self):
        for i in range(0,self.spinBox.value()):
            self.childStartThread[i] = StartThread(index=i)
            self.childStartThread[i].checkBox = self.checkBox
            self.childStartThread[i].checkBox_2 = self.checkBox_2
            self.childStartThread[i].checkBox_3 = self.checkBox_3
            self.childStartThread[i].checkBox_4 = self.checkBox_4
            self.childStartThread[i].start()
            self.childStartThread[i].showStatus.connect(self.showStatus)

    def setTableWidget(self):
        # Open File and get Account Gmail
        with open('DATA/account.txt','r') as rA:rA=rA.readlines()

        # Handhand Set Row of Tablewidget
        rowCount = len(rA)
        self.tableWidget.setRowCount(rowCount)
        self.tableWidget.setColumnCount(2)

        # Show Account to Tablewidget
        count = 0
        for item in rA:
            name = item.split('|')[0]
            self.tableWidget.setItem(count, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(count, 1, QTableWidgetItem('Ready'))
            count += 1


    def showStatus(self,index,text):
        self.tableWidget.setItem(index, 1, QTableWidgetItem(text))


    def stop(self):
        for i in range(0, self.spinBox.value()):
            self.childStartThread[i].terminate()
            self.tableWidget.setItem(i, 1, QTableWidgetItem('Stop !!!'))

class StartThread(QThread):
    showStatus = pyqtSignal(int,str)
    def __init__(self,index = 0):
        super(StartThread, self).__init__()
        self.index = index
        self.is_running = True
    def run(self):
        with open('DATA/account.txt','r',encoding='utf8') as rA:rA=rA.readlines()
        global _count
        while True:
            _count += 1
            self.count = _count
            if _count > len(rA)-1:break
            self.handle()
        # images = self.getimages()
        # for image in images:
        #     print(image)



    #Create Browser
    def setBrowser(self):
        self.showStatus.emit(self.count, 'Đang khởi tạo hệ thống !')
        self.temp = os.path.normpath(tempfile.mkdtemp())
        opts = uc.ChromeOptions()
        # If spinBox use proxy checked,handle get proxy to api and use it !
        if self.checkBox.isChecked():
            proxy = self.getProxy()
            opts.add_argument('--proxy-server=%s' % proxy)
        opts.add_argument(f"--window-position={self.index * 200},0")
        #opts.add_argument("--window-size=800,880")
        args = ["hide_console", ]
        opts.add_argument('--deny-permission-prompts')
        opts.add_argument(f'--user-data-dir={self.temp}')
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--disable-gpu")
        self.browser = uc.Chrome(executable_path=os.getcwd()+'/chromedriver',options=opts,service_args=args)
        with self.browser:self.browser.get('https://gmail.com')

    # Get proxy
    def getProxy(self):
        with open('DATA/apiproxy.txt', 'r') as rProxy:
            rProxy = rProxy.readlines()
        while True:
            proxy = requests.get(
                f'http://proxy.tinsoftsv.com/api/changeProxy.php?key=[{rProxy[self.index]}]&location=[0]')
            proxy_data = json.loads(proxy.text)
            try:
                proxy = proxy_data['proxy']
                self.showStatus.emit(self.count,f'Lấy Thành Công Proxy : {proxy}')
                return proxy
            except:
                timedelay = proxy_data['next_change']
                for i in range(int(timedelay), 0, -1):
                    self.showStatus.emit(self.count,f'Hệ Thống Sẽ Khởi Động Sau {i}s')
                    sleep(1)


    #Handle

    def handle(self):
        try:

            self.setBrowser()
            self.showStatus.emit(self.count, 'Đang xử lý !!!')
            # Open Account Files and get User and Password
            with open('DATA/account.txt','r') as rA:rA=rA.readlines()
            nickname = rA[self.count].split("|")[0]
            password = rA[self.count].split("|")[1]
            # Send email
            self.browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(nickname)
            sleep(1)

            # Click Continue
            self.browser.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
            sleep(5)

            # Send Keypassword
            self.check(self.browser,'input[type="password"]')

            self.browser.find_element_by_css_selector('input[type="password"]').send_keys(password)
            sleep(1)

            # Click Continue
            self.browser.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
            sleep(5)


            self.browser.get('https://google.com/maps')
            sleep(1)
            # Check Account Google login
            check = self.check(self.browser,'a[class="gb_A gb_La gb_f"]',timeout=8)
            if not check:return

            # Search Keyword
            count = 0
            lenRK = 1
            while True:
                if count > lenRK-1: break
                keyword,lenRK = self.handleKeyword(count)
                count += 1
                self.browser.find_element_by_css_selector('#searchboxinput').clear()
                self.browser.find_element_by_css_selector('#searchboxinput').send_keys(keyword)
                sleep(randint(3,5))
                # Select Key The Fisrt
                try:
                    self.browser.find_element_by_css_selector('#searchboxinput').send_keys(Keys.ENTER)
                except:pass

                sleep(5)
            # handle Another
            #     check = self.handleBackdoor()
            #     if check == False:
                for i in range(0, 50):
                    self.browser.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]').send_keys(Keys.DOWN)
                    sleep(0.1)
                # Handle Review
                if self.checkBox_2.isChecked():
                    self.handleReview()


                self.browser.switch_to.default_content()

                # Handle Add Picture
                if self.checkBox_3.isChecked():
                    self.handleAddPicture()

                self.showStatus.emit(self.count, 'Thành công . Đang dọn dẹp hệ thống !')
                sleep(randint(5,8))
                self.showStatus.emit(self.count, 'Thành công !!!')
            self.close()
            self.showStatus.emit(self.count, 'Thành công !!!')
        except ZeroDivisionError:
            logging.exception("message")
            self.close()
            self.showStatus.emit(self.count, 'Thất bại !!!')
            sleep(randint(2,3))






    def check(self,browser,css,timeout=15):
        count = 0
        while count < int(timeout):
            try:
                browser.find_element_by_css_selector(css)
                return True
            except:
                sleep(1)
                count += 1
        return False

    def handleReview(self):
        try:
            # Click Danh Gia
            self.browser.execute_script(
                """document.querySelector('button[jsaction="pane.reviewsummary.writeReview;keydown:pane.reviewsummary.writeReview"]').click()""")
            sleep(3)

            # Switch To Iframe Of Vote
            iframe = self.browser.find_element_by_css_selector('iframe[name="goog-reviews-write-widget"]')
            self.browser.switch_to.frame(iframe)
            sleep(1)
        # Vote Sao
            star = randint(4, 5)
            self.browser.execute_script(
                f"""document.querySelector('div[data-rating="{star}"]').click()""")
            sleep(3)
            # Review
            message = self.getMessage()
            self.browser.find_element_by_css_selector('textarea').send_keys(message)
            sleep(2)
            # self.browser.find_elements_by_css_selector('button')[2].click()
            # sleep(randint(3, 5))
            self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')[2].click()
            # Check Review
            checkReview = self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')
            if len(checkReview) > 3:
                checkReview[0].click()
                sleep(3)
                self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')[2].click()
            sleep(randint(3, 5))
            self.browser.find_element_by_css_selector('button[jscontroller="soHxf"]').click()
        except:
            return
    def getimages(self):
        while True:
            path = os.getcwd()
            folderimg = path + '/DATA/Images' if self.checkBox_4.isChecked() else path + '/DATA/Image'
            listimg = os.listdir(folderimg)
            images = []
            for image in listimg:
                if filetype.is_image(folderimg + '/' + image):
                    images.append(os.path.join(folderimg,image))
            return images

    # Get Message
    def getMessage(self):
        with open('DATA/message.txt', encoding='utf8') as rM: rM = rM.readlines()
        messages = random.choice(rM)
        return messages


    def close(self):
        if self.browser:
            self.browser.close()
            sleep(0.25)
            self.browser.quit()
            try:
                shutil.rmtree(r'{}'.format(self.temp))
            except:
                pass


    def handleAddPicture(self):
        try:
            # Click Add Picture
            self.browser.execute_script(
                """document.querySelector('button[jsaction="pane.imagery.addPhoto;keydown:pane.imagery.addPhoto"]').click()""")
            sleep(3)
            iframe = self.browser.find_element_by_css_selector('iframe[class="picker-frame"]')
            self.browser.switch_to.frame(iframe)
            sleep(2)
            # Find Input Files and send Picture to input
            if self.checkBox_4.isChecked():
                images = self.getimages()
                for image in images:
                    self.browser.find_element_by_css_selector('input[type="file"]').send_keys(image)
            else:
                images = self.getimages()
                rdImage = random.randint(0,len(images)-1)
                self.browser.find_element_by_css_selector('input[type="file"]').send_keys(images[rdImage])
            # self.browser.find_element_by_css_selector('input[type="file"]').send_keys('/Users/nguyenanh/PycharmProjects/VoteGoogleMaps/DATA/Images/img_1.png','/Users/nguyenanh/PycharmProjects/VoteGoogleMaps/DATA/Images/img_2.png','/Users/nguyenanh/PycharmProjects/VoteGoogleMaps/DATA/Images/img.png')

            sleep(randint(6, 10))
            self.browser.switch_to.default_content()
            for i in range(0,10):
                try:
                    self.browser.find_element_by_css_selector('button[jsaction="modal.close"]').click()
                    break
                except:
                    sleep(1)
            sleep(3)


            #self.browser.find_element_by_xpath('//*[@id="last-focusable-in-modal"]').click()
            #self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')[2].click()
        except:
            return


    def handleBackdoor(self):
        #try:
        countA = 0
        div = self.browser.find_element_by_css_selector('div[class="w6VYqd"]')
        aDiv = div.find_elements_by_css_selector('a')
        sleep(3)
        for i in range(0,len(aDiv)):
            self.showStatus.emit(self.count, 'Đang xử lý !!!')
            div.find_elements_by_css_selector('a')[i].click()
            sleep(3)
            # Handle Review

            if self.checkBox_2.isChecked():
                self.handleReview()

            self.browser.switch_to.default_content()

            # Handle Add Picture
            if self.checkBox_3.isChecked():
                self.handleAddPicture()

            self.showStatus.emit(self.index, 'Thành công . Đang dọn dẹp hệ thống !')
            sleep(randint(5,8))
            self.showStatus.emit(self.index, 'Thành công !!!')
            break
        # except:
        #     print('Loi')
        #     return False


    def handleKeyword(self,index):
        with open('DATA/keyword.txt' ,'r',encoding='utf8') as rK:rK = rK.readlines()
        return rK[index],len(rK)

class HandleKey(QMainWindow):
    def __init__(self):
        super(HandleKey, self).__init__()
        uic.loadUi("DATA/untitled1.ui", self)
        self.label = self.findChild(QLabel,'label')
        self.label_2 = self.findChild(QLabel,'label_2')
        self.pushButton = self.findChild(QPushButton,'pushButton')
        self.pushButton.clicked.connect(self.btnCLicked)
        keyID = str(uuid.uuid1())
        self.keyID = keyID.replace('-', '')
        self.label_2.setText(f'Mã máy kích hoạt của bạn : {self.keyID}')


        self.show()

    def btnCLicked(self):
        pyperclip.copy(self.keyID)
        #self.label_2.setText('Copy Key Thành Công')




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    keyID = str(uuid.uuid1())
    keyID = keyID.replace('-', '')

    url = 'http://echipauto.com/config_keycomputer.php'

    payloads = {
        'mail': 'votegooglemaps',
        'pass': '123456',
        'mamay': keyID[-9:],
        'id': '9995119',
        'submit': 'submit'
    }
    response = requests.post(url,data=payloads)
    response = json.loads(response.text)
    if response.get('status','') == 'success':
        hsd = response.get('hsd','')
        UiWindow = UI(hsd)
    else:
        UiKey = HandleKey()


    app.exec()