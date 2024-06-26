## 用於加密貨幣交易的自動通知程式
## Python版
## Google app scrpit 版
   -https://api.binance.com 拒絕來自google的請求，需改用https://api.binance.us
   -可使用Google app scrpit 觸發條件,來達成定時自動化通知
1. **獲取幣安資料：**
   - 使用幣安 API 獲取最新的加密貨幣價格資料。

2. **獲取過去12小時的每小時K線數據：**
   - 使用幣安 API 獲取指定交易對過去12小時的每小時K線數據。

3. **檢查上漲趨勢：**
   - 分析每小時K線數據，檢查是否出現連續上漲的情況。

4. **發送Line通知：**
   - 如果符合條件的加密貨幣交易對出現上漲趨勢，將通知發送到指定的 Line 帳號。

### 使用方法：

1. 將程式碼中的 Line 通知金鑰填入 `line_notify_token` 變數中。
2. 執行程式，它將自動獲取幣安資料並進行分析。
3. 如果符合條件，將通知發送到你的 Line 帳號。

### 注意事項：

- 確保在使用 Line 通知功能前，已獲取 Line Notify 的金鑰。
- 根據需要修改程式中的符號、時間間隔和 K 線數量等參數。
![image](https://github.com/FunZ5566/Line-Notify/blob/main/linenotify3.jpg?raw=true)
