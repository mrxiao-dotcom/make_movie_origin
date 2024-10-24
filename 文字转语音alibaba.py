import time
import threading
import sys

import nls


URL = "wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN = "c96de4ff910d4fa6bd63bdec0c93c3c3"  # 参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = "sNoyW1nvmbfpqYdJ"  # 获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist

TEXT = '大壮正想去摘取花瓣，谁知阿丽和阿强突然内讧，阿丽拿去手枪向树干边的阿强射击，两声枪响，阿强直接倒入水中'

# 以下代码会根据上述TEXT文本反复进行语音合成
class TestTts:
    def __init__(self, tid, test_file):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file

    def start(self, text):
        self.__text = text
        self.__f = open(self.__test_file, "wb")
        self.__th.start()

    def test_on_metainfo(self, message, *args):
        print("on_metainfo message=>{}".format(message))

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))

    def __test_run(self):
        print("thread:{} start..".format(self.__id))
        tts = nls.NlsSpeechSynthesizer(url=URL,
                                       token=TOKEN,
                                       appkey=APPKEY,
                                       on_metainfo=self.test_on_metainfo,
                                       on_data=self.test_on_data,
                                       on_completed=self.test_on_completed,
                                       on_error=self.test_on_error,
                                       long_tts=True,
                                       on_close=self.test_on_close,
                                       callback_args=[self.__id])
        print("{}: session start".format(self.__id))
        r = tts.start(self.__text,voice="zhixiang",aformat="mp3")   #aifei，aixiang，zhilun
        print("{}: tts done with result:{}".format(self.__id, r))


def multiruntest(num=500,text="",wav_file_path="wav\text.mp3"):
    if text == "":
        text = "我是钢铁侠"

    for i in range(0, num):
        name = "thread" + str(i)
        t = TestTts(name, wav_file_path)
        t.start(text)


def convert_txt_to_mp3(text, wav_file_path):

    nls.enableTrace(True)
    multiruntest(1,text,wav_file_path)

if __name__ == '__main__':
    convert_txt_to_mp3("我是钢铁侠，不久，法医便发现，死者的脚部有红豆大小的疤痕。","test.mp3")

