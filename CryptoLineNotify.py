import requests
import json
import os

def get_binance_data():
    api_url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"獲取幣安資料時出錯: {e}")
        return None

def get_past_hourly_candles(symbol, interval, limit):
    api_endpoint = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"獲取K線數據時出錯: {e}")
        return None

def check_upward_trend(candles, n_candles):
    consecutive_upward_count = 0
    for i in range(len(candles) - 1):
        if float(candles[i + 1][4]) > float(candles[i + 1][1]) and float(candles[i][4]) > float(candles[i][1]):
            consecutive_upward_count += 1
        if consecutive_upward_count >= n_candles:
            return True
    return False

def check_volume_increase(candles):
    volumes = [float(candle[5]) for candle in candles]
    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])
    latest_volume = volumes[-1]
    return latest_volume > avg_volume

def send_line_notification(message):
    line_notify_token = os.environ['LINE_NOTIFY_TOKEN']
    line_notify_endpoint = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {line_notify_token}"
    }
    payload = {
        "message": message
    }
    try:
        response = requests.post(line_notify_endpoint, headers=headers, data=payload)
        response.raise_for_status()
        print(f"Line通知已發送: {message}")
    except requests.RequestException as e:
        print(f"發送Line通知時出錯: {e}")

def main():
    binance_data = get_binance_data()
    hours = 1
    hour = f"{hours}h"
    hw_candles = 12
    n_candles = 6
    if binance_data:
        notification_list = []
        for symbol_data in binance_data:
            if symbol_data['symbol'].endswith('USDT'):
                symbol = symbol_data['symbol']
                candles = get_past_hourly_candles(symbol, hour, hw_candles)
                if candles:
                    if check_upward_trend(candles, n_candles) and check_volume_increase(candles):
                        message = f"\n{symbol}"
                        notification_list.append(message)
                else:
                    print(f"無法獲取 {symbol} 的K線數據")
        notification_string = "".join(notification_list)
        send_line_notification(notification_string +
                               f"\n\n以上加密貨幣過去{hours * hw_candles}H有至少" +
                               f"基於{hour}K線有{n_candles}根K線是上漲的，且最新交易量大於過去平均交易量")
    else:
        print("無法獲取幣安資料")

if __name__ == "__main__":
    main()
