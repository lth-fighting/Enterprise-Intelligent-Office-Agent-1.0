import speech_recognition as sr
import requests
from config import BAIDU_API_KEY, BAIDU_SECRET_KEY


class VoiceCommandSystem:
    def __init__(self,
                 listen_timeout=8,
                 max_retries=1,
                 baidu_api_key=None,
                 baidu_secret_key=None):
        # 核心参数初始化
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listen_timeout = listen_timeout
        self.max_retries = max_retries
        self.baidu_api_key = baidu_api_key
        self.baidu_secret_key = baidu_secret_key
        self.access_token = self._get_baidu_token()
        self.running = True  # 控制监听状态
        self.recognized_result = None  # 用于保存识别结果的变量

        # 初始化麦克风
        try:
            with self.microphone as source:
                print("正在调整麦克风以适应环境噪音...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("初始化完成，请说话（识别到语音后将自动退出）")
        except Exception as e:
            print(f"麦克风初始化失败: {e}")

    def _get_baidu_token(self):
        """获取百度语音识别访问令牌"""
        if not (self.baidu_api_key and self.baidu_secret_key):
            print("未配置百度API密钥，无法使用语音识别")
            return None

        try:
            url = (
                f"https://aip.baidubce.com/oauth/2.0/token"
                f"?grant_type=client_credentials"
                f"&client_id={self.baidu_api_key}"
                f"&client_secret={self.baidu_secret_key}"
            )
            response = requests.get(url)
            token = response.json().get("access_token")
            if token:
                print("百度语音识别服务已就绪")
                return token
            print("获取百度令牌失败")
            return None
        except Exception as e:
            print(f"获取令牌出错: {e}")
            return None

    def _recognize_baidu(self, audio_data):
        """调用百度API识别语音"""
        if not self.access_token:
            return None

        try:
            # 转换音频格式为百度API要求的PCM
            pcm_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
            url = f"https://vop.baidu.com/server_api?cuid=python_voice&token={self.access_token}"
            headers = {"Content-Type": "audio/pcm; rate=16000"}

            response = requests.post(url, data=pcm_data, headers=headers)
            result = response.json()

            if result.get("err_no") == 0:
                return "".join(result["result"])
            print(f"识别失败: {result.get('err_msg')}")
            return None
        except Exception as e:
            print(f"识别过程出错: {e}")
            return None

    def listen_for_command(self):
        """单次监听并返回识别结果"""
        if not self.access_token:
            return None

        try:
            with self.microphone as source:
                print(f"正在监听...（超时 {self.listen_timeout} 秒）")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.listen_timeout,
                    phrase_time_limit=60  # 适配百度短语音最大60秒限制
                )

            # 调用百度识别
            result = self._recognize_baidu(audio)
            if result:
                print(f"识别结果: {result}")
                self.recognized_result = result  # 保存识别结果到实例变量
            return result

        except sr.WaitTimeoutError:
            print("未检测到语音输入")
            return None
        except Exception as e:
            print(f"监听出错: {e}")
            return None

    def process_audio_file(self, file_path):
        if not self.access_token:
            return None

        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)

            result = self._recognize_baidu(audio)
            if result:
                print(f"语音识别结果: {result}")
                self.recognized_result = result  # 保存识别结果到实例变量
                return result
            return None
        except sr.WaitTimeoutError:
            print("未检测到语音输入")
            return None
        except Exception as e:
            print(f"监听出错: {e}")
            return None

    def start_listening(self):
        """启动监听，识别到语音后自动退出"""
        retry_count = 0
        while self.running:
            command = self.listen_for_command()

            # 识别到有效语音后立即退出
            if command:
                print("已识别到语音，程序自动退出")
                self.stop()
                break

            # 重试逻辑（仅针对未检测到语音的情况）
            if not command:
                retry_count += 1
                if retry_count >= self.max_retries:
                    print(f"已达最大重试次数（{self.max_retries}次），程序退出")
                    self.stop()
                    break

    def stop(self):
        """停止系统运行"""
        self.running = False

    def get_recognized_result(self):
        """获取识别结果的方法"""
        return self.recognized_result


def voice_to_txt():
    voice_system = VoiceCommandSystem(
        listen_timeout=8,
        max_retries=1,
        baidu_api_key=BAIDU_API_KEY,
        baidu_secret_key=BAIDU_SECRET_KEY
    )

    try:
        voice_system.start_listening()

        final_result = voice_system.get_recognized_result()
        if final_result:
            print(final_result)
            return final_result
        else:
            return "未识别到有效语音内容"

    except KeyboardInterrupt:
        print("\n用户中断，正在退出...")
    finally:
        voice_system.stop()


def file_to_txt(file_path):
    """处理单个音频文件并返回识别结果"""
    voice_system = VoiceCommandSystem(
        listen_timeout=8,
        max_retries=1,
        baidu_api_key=BAIDU_API_KEY,
        baidu_secret_key=BAIDU_SECRET_KEY
    )

    try:
        result = voice_system.process_audio_file(file_path)
        if result:
            print(result)
            return result
        else:
            return "未识别到有效语音内容"

    except Exception as e:
        print(f"语音识别出错: {str(e)}")
        return None
    finally:
        voice_system.stop()
