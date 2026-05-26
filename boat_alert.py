import requests
import os

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# -------------------
# レース情報（ここを書き換える）
# -------------------

place = "江戸川"

wind = 6          # 風速
wave = 7          # 波高

st1 = 0.18        # 1号艇ST
st4 = 0.11        # 4号艇ST

motor1 = 32       # 1号艇モーター2連率

race_type = "一般戦"

# -------------------
# 条件判定
# -------------------

target_places = ["戸田", "平和島", "江戸川", "鳴門"]

if (
    place in target_places
    and wind >= 5
    and wave >= 5
    and st1 >= 0.17
    and st4 <= 0.13
    and motor1 <= 35
    and race_type == "一般戦"
):

    message = f"""
【荒れ条件一致】

開催場：{place}

風速：{wind}m
波高：{wave}cm

1号艇ST：{st1}
4号艇ST：{st4}

1号艇モーター：{motor1}%

4カド警戒
"""

    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(send_url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

    print("通知送信")

else:

    print("条件不一致")
