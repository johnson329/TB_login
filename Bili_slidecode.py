from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image,ImageChops
from lxml import etree
from urllib.request import urlretrieve
import re


class CrackGeetest(object):
    def __init__(self,url,username,password):
        self.url=url
        self.username=username
        self.password=password
        self.browser=webdriver.Chrome()
        self.wait=WebDriverWait(self.browser,10)
        self.bg_filename = 'bg.jpg'
        self.fullbg_filename = 'fulllbg.jpg'
        self.bg_xpath = '//div[@class="gt_cut_fullbg gt_show"]/div'
        self.fullbg_xpath = '//div[@class="gt_cut_bg gt_show"]/div'
    def open(self):
        self.browser.get(self.url)

        userinput=self.wait.until(ec.presence_of_element_located((By.ID,'login-username')))
        userinput.send_keys(self.username)
        userinput = self.wait.until(ec.presence_of_element_located((By.ID, 'login-passwd')))
        userinput.send_keys(self.password)
    def get_image(self,filename,xpath):
        import time
        time.sleep(1)
        bg_location_list = []
        html=etree.HTML(self.browser.page_source)
        bg_obj=html.xpath(xpath)
        bg_url_pattern=re.compile('url\("(.*?)"\)',re.S)
        bg_url=re.search(bg_url_pattern,bg_obj[0].get("style")).group(1)
        for i in bg_obj:
            location={}
            location['x'],location['y']=re.search('background-position: (.*?)px (.*?)px',i.get("style")).groups()
            bg_location_list.append(location)

        urlretrieve(bg_url.replace('webp','jpg'),filename=filename)
        return bg_location_list
    def get_merge_image(self,filename,location_list):
        im=Image.open(filename)
        im_list_upper=[]
        im_list_down = []
        for location in location_list:
            if location['y']=='-58':
                im_list_upper.append(im.crop((abs(int(location['x'])),58,abs(int(location['x']))+10,166)))
            if location['y']=='0':
                im_list_down.append(im.crop((abs(int(location['x'])), 0, abs(int(location['x'])) + 10, 58)))
        new_im=Image.new('RGB',(260,116))
        x_offset=0
        for im in im_list_upper:
            new_im.paste(im,(x_offset,0))
            x_offset+=im.size[0]
        x_offset=0
        for im in im_list_down:
            new_im.paste(im,(x_offset,58))
            x_offset += im.size[0]
        new_im.save(filename)
        return new_im
    def down_merge(self):
        location_list=self.get_image(self.bg_filename,self.bg_xpath)
        img1=self.get_merge_image(self.bg_filename,location_list)
        location_list = self.get_image(self.fullbg_filename, self.fullbg_xpath)
        img2=self.get_merge_image(self.fullbg_filename, location_list)
        return img1,img2
    def is_px_equal(self,img1,img2,x,y):
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 11
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False
    def get_gap_location(self,img1,img2):
        for x in range(img1.size[0]):
            for y in range(img2.size[1]):
                if not self.is_px_equal(img1,img2,x,y):
                    return x

    def get_slider(self):
        slider=self.browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
        return slider
    def move2gap(self,slider,offset):
        import time
        print(offset)
        ActionChains(self.browser).click_and_hold(slider).perform()
        time.sleep(1)
        ActionChains(self.browser).move_by_offset(xoffset=offset,yoffset=0).perform()
        time.sleep(1)
        ActionChains(self.browser).release().perform()
        time.sleep(5)


    def crack(self):
        self.open()
        try:
            img1,img2=self.down_merge()
            diff_location=self.get_gap_location(img1,img2)
            print(diff_location)
            slider=self.get_slider()
            self.move2gap(slider,diff_location)
        finally:
            self.browser.quit()



if __name__ == '__main__':
    cg=CrackGeetest("https://passport.bilibili.com/login","123","123")
    cg.crack()
