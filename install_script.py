import os
import re
import threading   #多线程
import time
import sys

#isdevice = False    #定义一个全局变量
# ======查找目录，找到最新app======https://app.appsflyer.com/scratch.spin.raffle.luckyone.win?pid=TestMediaSource&media_source=googleadwords_int&campaign=12345&advertising_id=20482b1f-0f2d-40f7-95bd-a126af0c53fd
def new_report(directory):
    lists = os.listdir(directory)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(directory + "\\" + fn))  # 按时间排序
    file_new = lists[-1]
    #file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    return file_new

#返回包名
def packageRe(directory):
    file_name = new_report(directory)
    backage = re.findall(r"(.+?)-", file_name)
    return backage[0]




#判读手机是否连接正常
def isnotdevices():
    try:
        command = "adb devices"
        d = os.popen(command)
        #global isdevice
        return True
    except:
        print("请链接好手机，重新尝试")
#返回所有devices
def get_dives():
    res = os.popen("adb devices")
    test = res.read()
    list = test.split('\n')
    del(list[0])
    devices_list = []
    for i in list:
        if i == '':
            continue
        if "device" in i:
            device_id = i.split('\t')[0]
        devices_list.append(device_id)

    return devices_list
#判断是否安装了该包，查询手机中所有安装的第三方包
def packages(devices):
    command = "adb -s {} shell pm list packages -3".format(devices)
    try:
        d = os.popen(command)
        # d = os.system(command)
        f = d.read()
        print(f)
        return f
    except:
        return False

#卸载安装包
def uninstall(directory,devices):
    backage = packageRe(directory)
    try:
        #backages = "com.xuanming.security.master"
        command = "adb -s {} uninstall ".format(devices) + backage
        d = os.popen(command)
        f = d.read()
        assert("Success" in f)
        print("卸载成功")
        print(time.asctime(time.localtime(time.time())))
    except:
        print("卸载失败")

#安装app
def install(directory,devices):
    file_name = new_report(directory)                       #调用获取最新文件名函数
    print(file_name)
    #packages_path = "D:\\install_rar\\com.xuanming.security.master-Toutiao_debug_testServer_v1.10.4-debug_vc10_svn44481.apk"
    command = "adb -s {} install ".format(devices) + "\"" + directory +file_name + "\""   #拼接adb命令
    print(command)
    try:
        d = os.popen(command)
        f = d.read()
        assert ("Success" in f)
        return True
    except:
        return False

def run_main(devices):
    directory = "D:\\install_rar\\"
    package = packageRe(directory)
    ele = isnotdevices()
    if ele == True:
        packages_list = packages(devices)
        if package in packages_list:
            uninstall(directory,devices)  # 先卸载
        bool_install = install(directory,devices)  # 安装
    if bool_install:
        print("成功安装：" + package)
    else:
        print("安装失败，请重试！")
    #print(time.asctime(time.localtime(time.time())))
    #sys.exit()
if __name__ == "__main__":
    '''
    r = threading.Thread(target=run_main)
    r.setDaemon(True)
    r.start()

    r.join(60)
    print("扑街了")
    print(time.asctime(time.localtime(time.time())))
    '''
    devices_list = get_dives()
    print(devices_list)
    for i in devices_list:
        run_main(i)