# line_notify_token = ""
# line_notify = LineNotify(line_notify_token)
# 設定您的Line通知金鑰
# line_notify_token = ""
import requests
from line_notify import LineNotify

# 幣安API端點
api_endpoint = "https://api.binance.us/api/v3/ticker/price"

# 設定您的Line通知金鑰
line_notify_token = ""
line_notify = LineNotify(line_notify_token)


def get_binance_data():
    try:
        response = requests.get(api_endpoint)
        data = response.json()
        return data
    except Exception as e:
        print("獲取幣安資料時出錯:", e)
        return None


def get_past_hourly_candles(symbol,interval,limit):
    try:
        api_endpoint = "https://api.binance.us/api/v3/klines"
        interval = interval  # 每小時K線
        limit = limit  # 獲取最近6根K線數據

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(api_endpoint, params=params)
        data = response.json()

        # data現在包含了最近6根指定交易對的每小時K線數據
        return data
    except Exception as e:
        print("獲取K線數據時出錯:", e)
        return None


def check_upward_trend(candles):
    try:
        # 初始化計數器
        consecutive_upward_count = 0

        # 遍歷K線數據
        for i in range(len(candles) - 1):
            # 檢查相鄰的兩根K線是否呈上漲趨勢（收盤價高於開盤價）
            if float(candles[i + 1][4]) > float(candles[i + 1][1]) and float(candles[i][4]) > float(candles[i][1]):
                consecutive_upward_count += 1
            else:
                consecutive_upward_count = 0

            # 如果連續上漲的次數達到4次，則返回True
            if consecutive_upward_count >= 4:
                return True

        # 如果沒有達到連續上漲4次的情況，則返回False
        return False
    except Exception as e:
        print("檢查上漲趨勢時出錯:", e)
        return False


def send_line_notification(message):
    try:
        line_notify.send(message)
        print("Line通知已發送:", message)
    except Exception as e:
        print("發送Line通知時出錯:", e)

def main():
    # 獲取幣安資料
    binance_data = get_binance_data()

    if binance_data:
        # 創建一個空列表，用於存儲符合條件的交易對
        notification_list = []

        # 遍歷每個交易對，檢查是否為USDT交易對
        for symbol_data in binance_data:
            if symbol_data['symbol'].endswith('USDT'):
                symbol = symbol_data['symbol']

                # 獲取過去12小時的每小時K線數據
                candles = get_past_hourly_candles(symbol,"4h",6)
                if candles:
                    # 檢查上漲趨勢
                    if check_upward_trend(candles):
                        message = f"\n{symbol}"
                        notification_list.append(message)
                else:
                    print(f"無法獲取 {symbol} 的K線數據")

        send_line_notification(notification_list)
        send_line_notification("\n 以上加密貨幣過去6小時有至少3根K線是上漲的")

    else:
        print("無法獲取幣安資料")
if __name__ == "__main__":
    main()
