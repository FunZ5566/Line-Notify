function getBinanceData() {
  var apiUrl = "https://api.binance.us/api/v3/ticker/price";

  try {
    var response = UrlFetchApp.fetch(apiUrl);
    var data = JSON.parse(response.getContentText());
    return data;
  } catch (e) {
    Logger.log("獲取幣安資料時出錯: " + e);
    return null;
  }
}

/*function getPastHourlyCandles(symbol, interval, limit) {
  var apiEndpoint = "https://api.binance.us/api/v3/klines";
  var params = {
    "symbol": symbol,
    "interval": interval,
    "limit": limit
  };

  try {
    var response = UrlFetchApp.fetch(apiEndpoint, { "method": "get", "muteHttpExceptions": true, "payload": params });
    var data = JSON.parse(response.getContentText());
    Logger.log(data)
    return data;
  } catch (e) {
    Logger.log("獲取K線數據時出錯: " + e);
    return null;
  }
}
*/
function getPastHourlyCandles(symbol, interval, limit) {
  var apiEndpoint = "https://api.binance.us/api/v3/klines";
  var params = {
    "symbol": symbol,
    "interval": interval,
    "limit": limit
  };

  try {
    var queryString = Object.keys(params).map(function(key) {
      return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
    }).join('&');

    var response = UrlFetchApp.fetch(apiEndpoint + '?' + queryString);
    var data = JSON.parse(response.getContentText());
    return data;
  } catch (e) {
    Logger.log("獲取K線數據時出錯: " + e);
    return null;
  }
}
function checkUpwardTrend(candles,nCandles) {
  var consecutiveUpwardCount = 0;
  for (var i = 0; i < candles.length - 1; i++) {
    if (parseFloat(candles[i + 1][4]) > parseFloat(candles[i + 1][1]) && parseFloat(candles[i][4]) > parseFloat(candles[i][1])) {
      consecutiveUpwardCount++;
    }
    //  else {
    //   consecutiveUpwardCount = 0;
    // }

    if (consecutiveUpwardCount >=nCandles) {
      return true;
    }
  }

  return false;
}

function sendLineNotification(message) {
  var lineNotifyToken = "";
  var lineNotifyEndpoint = "https://notify-api.line.me/api/notify";

  try {
    var options = {
      "method": "post",
      "headers": {
        "Authorization": "Bearer " + lineNotifyToken
      },
      "payload": {
        "message": message
      }
    };

    UrlFetchApp.fetch(lineNotifyEndpoint, options);
    Logger.log("Line通知已發送: " + message);
  } catch (e) {
    Logger.log("發送Line通知時出錯: " + e);
  }
}

function main() {
  // 獲取幣安資料
  var binanceData = getBinanceData();
  var hours = 1;
  var hour = hours+"h";
  var hwCandles = 24;
  var nCandles = 8;
  if (binanceData) {
    // 創建一個空列表，用於存儲符合條件的交易對
    var notificationList = [];

    // 遍歷每個交易對，檢查是否為USDT交易對
    for (var i = 0; i < binanceData.length; i++) {
      var symbolData = binanceData[i];

      if (symbolData.symbol.endsWith('USDT')) {
        var symbol = symbolData.symbol;

        // 獲取過去12小時的每小時K線數據
        var candles = getPastHourlyCandles(symbol, hour, hwCandles);
        //var candles2 = getPastHourlyCandles(symbol,"1h",12);
        if (candles) {
          // 檢查上漲趨勢
          if (checkUpwardTrend(candles,nCandles)) {
            var message = "\n" + symbol;
            notificationList.push(message);
          }
        } else {
          Logger.log("無法獲取 " + symbol + " 的K線數據");
        }
      }
    }

    // 將通知列表轉換為字符串
    var notificationString = notificationList.join("");

    // 發送Line通知
    sendLineNotification(notificationString+
                         "\n\n以上加密貨幣過去"+
                         hours*hwCandles+"H有至少"+
                         "基於"+hour+"K線有"+
                         nCandles+"根K線是上漲的");
    //sendLineNotification("\n 以上加密貨幣過去"+hours*hwCandles+"H有至少"+nCandles+"根K線是上漲的");
  } else {
    Logger.log("無法獲取幣安資料");
  }
}
