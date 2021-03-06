#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_utils.android_tools.android_driver import *
from auto_utils.android_tools.weixin.command import *


def send_collect_info(driver, name):
    driver.click('ui=new UiSelector().text("发消息")')
    result = driver.is_displayed('aid=更多功能按钮，已折叠', 3)
    if result:
        time.sleep(1)
        driver.click('aid=更多功能按钮，已折叠')
        driver.click('ui=new UiSelector().text("我的收藏")')
        # driver.click('ui=new UiSelector().text("链接")')
        # driver.click('ui=new UiSelector().text("%s")' % name)
        driver.click('id=com.tencent.mm:id/b3')
        driver.click('ui=new UiSelector().text("发送")')
    else:
        driver.click('aid=更多功能按钮，已折叠')


def send_msg(driver, content='ॣ ॣ ॣ'):
    driver.click('ui=new UiSelector().text("发消息")')
    driver.type('id=com.tencent.mm:id/aie', content)
    driver.click('ui=new UiSelector().text("发送")')


def need_del(driver):
    driver.is_displayed('aid=聊天信息', 10)
    re_send = driver.is_displayed('aid=重发', 2)
    fr_add = driver.is_displayed('ui=new UiSelector().text("对方未添加你为好友")', 2)
    if re_send or fr_add:
        return True
    else:
        return False


def del_friend(driver, name):
    try:
        driver.click('aid=聊天信息')
        driver.click('id=com.tencent.mm:id/dnr')
        driver.click('aid=更多')
        driver.click('ui=new UiSelector().text("删除")')
        if driver.is_displayed('ui=new UiSelector().text("删除联系人")'):
            driver.click('ui=new UiSelector().text("删除")')
        else:
            pass
    except Exception as e:
        logging.error('%s 删除失败，错误信息：%s' % (name, e))


def move2user_display(driver, user_name):
    back_contacts_page(driver)
    while True:
        users = driver.find_type('id=com.tencent.mm:id/mc')
        for user in users:
            name = user.text
            name = name.replace(',', '')
            if name == user_name:
                logging.info('%s is display' % name)
                return user
        logging.info('%s is not display,swipe2down' % user_name)
        driver.swipe2down()
        if driver.is_displayed('ui=new UiSelector().text("确定")', 1):
            driver.click('ui=new UiSelector().text("确定")')


def contacts_read():
    path = os.path.dirname(__file__) + '/contacts.txt'
    with open(path, 'r', encoding='utf-8') as f:
        contracts = f.read().split(',')
    return contracts


def contacts_write(contacts):
    contacts = ','.join(contacts)
    path = os.path.dirname(__file__) + '/contacts.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contacts)
    logging.info('contacts writed!')


def chat_all_friend():
    driver = AndroidDriver()
    driver.open_app('weixin_1320.apk')
    driver.click('ui=new UiSelector().text("通讯录")')
    while True:
        contacts_name = contacts_read()
        try:
            contacts_page_flag = driver.is_displayed('id=com.tencent.mm:id/ll', 3)
            if contacts_page_flag:
                contacts = driver.find_type('id=com.tencent.mm:id/mc')
                names = []
                for c in contacts:
                    name = c.text
                    name = name.replace(',', '')
                    names.append(name)
                for name in names:
                    if name not in contacts_name:
                        element = move2user_display(driver, name)
                        contacts_name.append(name)
                        element.click()
                        send_collect_info(driver, '李茶的姑妈1')
                        result = need_del(driver)
                        if result:
                            del_friend(driver, name)
                        back_contacts_page(driver)
                driver.swipe2down()
            else:
                back_contacts_page(driver)
        except Exception as e:
            logging.error(e)
        finally:
            contacts_write(contacts_name)
            if driver.is_displayed('ui=new UiSelector().text("确定")', 5):
                driver.click('ui=new UiSelector().text("确定")')


def del_black_friend():
    driver = AndroidDriver()
    driver.open_app('weixin_1320.apk')
    contacts_name = contacts_read()
    driver.click('ui=new UiSelector().text("通讯录")')
    while True:
        try:
            contacts_page_flag = driver.is_displayed('id=com.tencent.mm:id/ll', 3)
            if contacts_page_flag:
                contacts = driver.find_type('id=com.tencent.mm:id/mc')
                names = []
                for c in contacts:
                    name = c.text
                    name = name.replace(',', '')
                    names.append(name)
                for name in names:
                    if name not in contacts_name:
                        element = move2user_display(driver, name)
                        contacts_name.append(name)
                        element.click()
                        send_msg(driver)
                        result = need_del(driver)
                        if result is True:
                            del_friend(driver, name)
                        back_contacts_page(driver)
                driver.swipe2down()
            else:
                back_contacts_page(driver)
        except Exception as e:
            logging.error(e)
        finally:
            contacts_write(contacts_name)
            if driver.is_displayed('ui=new UiSelector().text("确定")', 5):
                driver.click('ui=new UiSelector().text("确定")')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    chat_all_friend()
