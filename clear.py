import os
import re
import subprocess
import time
#isdevice = False    #定义一个全局变量
# ======查找目录，找到最新app======https://app.appsflyer.com/scratch.spin.raffle.luckyone.win?pid=TestMediaSource&media_source=googleadwords_int&campaign=12345&advertising_id=20482b1f-0f2d-40f7-95bd-a126af0c53fd
def new_report(directory):
    lists = os.listdir(directory)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(directory + "\\" + fn))  # 按时间排序
    file_new = lists[-1]
    #file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    return file_new

#获取文件包名-activity（使用sdk---tool：aapt通过apk文件获取包名/activity name）
class aaptUse:
	def __init__(self, file_path):
		self.file_path = file_path
		self.aapt_path = self.aapt_path()
	#获取aapt路径（视具体的sdk中tool的aapt的存放路径修改）
	def aapt_path(self):
		if 'ANDROID_HOME' in os.environ:							#通过os.environ获取环境变量，并判断是否含有“ANDROID_HOME”
			build_tools = os.path.join(os.environ['ANDROID_HOME'],'build-tools')		#拼接出build_tools的路径
			if "aapt.exe" in os.listdir(build_tools):
				aapt_path = os.path.join(build_tools, "aapt.exe")
				return aapt_path
			elif "version" in os.listdir(build_tools):
				version_path = os.path.join(build_tools, "version")
				if "aapt.exe" in os.listdir(version_path):
					aapt_path = os.path.join(version_path, "aapt.exe")
					return aapt_path
				else:
					print("没有找到aapt,请检查后再重试。")
					time.sleep(3)
					sys.exit()
			else:
				print("没有找到aapt,请检查后再重试。")
				time.sleep(3)
				sys.exit()
		else:
			print("没有找到路径'ANDROID_HOME',请检查后再重试。")
			time.sleep(3)
			sys.exit()
	#执行aapt命令获取包名
	def get_apk_backagename_activity(self):
		#print(self.aapt_path,self.file_path)
		p = subprocess.Popen("{} dump badging {}".format(self.aapt_path, self.file_path),
			 stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)			#通过subprocess.Popen
		(output, err) = p.communicate()
		#package_name = re.compile("package: name='(.+?)' versionCode").match(output.decode())
		#print(output.decode())
		package_name = re.findall("package: name='(.+?)' versionCode", output.decode())
		apk_activity = re.findall("launchable-activity: name='(.+?)'", output.decode())
		print(package_name,apk_activity)
		return package_name[0],apk_activity[0]
	#单独获取activity
	'''
	def get_apk_activity(self):
		p = subprocess.Popen("{} dump badging {}".format(self.aapt_path, self.file_path), stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		#package_name = re.compile("package: name='(.+?)' versionCode").match(output.decode())
		apk_activity = re.findall("launchable-activity: name='(.+?)'", output.decode())
		return apk_activity[0]
	'''

#返回包名
def packageRe(directory):
    file_name = new_report(directory)
    backage = re.findall(r"(.+?)-", file_name)
    return backage[0]
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
#清楚数据
def cleardata(devices, package):
	res = os.popen("adb -s {} shell pm clear {}".format(devices, package))
#启动app
#启动app：com.doutu.coolkeyboard/com.coconut.demo.MainActivity
def start_app(devices,package_name,main_activity):
	start_re = os.popen("adb -s {} shell am start -n {}/{}".format(devices,package_name, main_activity))
	if "Starting" in start_re.read():
		print("启动成功")
	else:
		print("启动失败")

if __name__ == "__main__":
	directory = "D:\\install_rar\\"
	path = os.path.join(directory,new_report(directory))
	get_name = aaptUse(path)
	backage_name,activity_name = get_name.get_apk_backagename_activity()

	packagename = packageRe(directory)
	list = get_dives()
	print(list)
	for i in list:
		cleardata(i,packagename)

		time.sleep(2)
		start_app(i,backage_name,activity_name)