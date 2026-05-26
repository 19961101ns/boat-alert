import requests
from bs4 import BeautifulSoup
import os
import re

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# 対象場
TARGET_PLACES = {
    "戸田": "01",
    "平和島": "04",
    "江戸川": "03",
    "鳴門": "14"
}

message_list = []

for place, code in TARGET_PLACES.items():

    url = f"https://www.boatrace.jp/owpc/pc/race/index?jcd={code}"

    try:

        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text()

        # 風速取得
        wind_match = re.search(r"風速\s*(\d+)m", text)

        # 波高取得
        wave_match = re.search(r"波高\s*(\d+)cm", text)

        if wind_match and wave_match:

            wind = int(wind_match.group(1))
            wave = int(wave_match.group(1))

            # 条件
            if wind >= 5 and wave >= 5:

                message_list.append(
                    f"【荒れ注意】\n"
                    f"{place}\n"
                    f"風速 {wind}m\n"
                    f"波高 {wave}cm"
                )

    except Exception as e:

        print(f"{place} エラー")
        print(e)

# 通知
if message_list:

    message = "\n\n".join(message_list)

    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(send_url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

    print("通知送信")

else:

    print("該当なし")
