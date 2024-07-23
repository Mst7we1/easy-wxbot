import requests
from datetime import datetime
from wxauto import WeChat

# 初始化微信自动化工具
wx = WeChat()


# 定义发送消息的函数
def send_msg(content, recipient=''):
  # recipient中填入发送消息对象昵称&备注
    wx.SendMsg(content, recipient)


# 获取当前时间并发送
local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
send_msg(f'现在是{local_time}')


# 定义获取天气信息的函数
def get_weather_info(location_code, api_key):
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location_code}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        update_time = data['updateTime']
        daily_forecast = data['daily'][0]
        date = daily_forecast['fxDate']
        temp_max = daily_forecast['tempMax']
        temp_min = daily_forecast['tempMin']
        weather_condition_day = daily_forecast['textDay']
        return {
            'update_time': update_time,
            'date': date,
            'temp_max': temp_max,
            'temp_min': temp_min,
            'weather_condition_day': weather_condition_day
        }
    else:
        return None


# 获取天气信息并发送
weather_info = get_weather_info(Location_ID, "token")
# 将Location_ID替换为所要城市代码 见：https://github.com/qwd/LocationList
# token替换为自己的，在和风天气控制台获取
if weather_info:
    weather_message = (
        '>>>--xx天气--<<<\n'
        f"日期: {weather_info['date']}\n"
        f"最高气温: {weather_info['temp_max']}°C\n"
        f"最低气温: {weather_info['temp_min']}°C\n"
        f"天气状态: {weather_info['weather_condition_day']}"
    )
    send_msg(weather_message)


# 定义获取名言的函数
def get_clean_hitokoto():
    url = "https://v1.hitokoto.cn/"
    response = requests.get(url)
    if response.status_code == 200:
        hitokoto_data = response.json()
        hitokoto = hitokoto_data['hitokoto'].split(' (')[0]
        return hitokoto
    else:
        return "Failed to fetch hitokoto."


# 获取名言并发送
hitokoto = get_clean_hitokoto()
send_msg(f'每日一言\n{hitokoto}')
