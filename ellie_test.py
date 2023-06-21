from flask_ngrok import run_with_ngrok          # colab 使用，本機環境請刪除
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage, ImageSendMessage  # 載入 StickerSendMessage 模組
from linebot.models import MessageEvent, TextMessage, TextSendMessage # 載入SendMessage模組
from linebot.models import LocationSendMessage #載入 LocationSendMessage 模組
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body) #將訊息轉換為 json 格式
    print(json_data)
    try:
        line_bot_api = LineBotApi('3LsJuvwl9uJzsF4SlN/2J5Cgi5Juxx26Sx2ROw6QNkPc8kY5xE56XSR9v56+08G4eifpj79zTgV81d21YBO38l1CWmpGRuBalO4ULSRa3wPilPf9submMAckVkSVgJOOsnjGmnDvLi0pZdRbnktseAdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('e0ee7e3d6f78c0fffa24dd926c683887')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']        # 取得 LINE 收到的訊息類型
        msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
        img_url = reply_img(msg)   # 取得對應的圖片，如果沒有取得，會是 False

        if type=='text':
            if img_url:
              # 如果有圖片網址，回傳圖片
              img_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
              line_bot_api.reply_message(tk,img_message)
            else:
              msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
              reply = msg
              line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
        else:
            stickerId = json_data['events'][0]['message']['stickerId'] # 取得 stickerId
            packageId = json_data['events'][0]['message']['packageId'] # 取得 packageId
            sticker_message = StickerSendMessage(sticker_id=stickerId, package_id=packageId) # 設定要回傳的表情貼圖
            line_bot_api.reply_message(tk, [sticker_message])  # 注意將 sticker_message 放在列表中
    except:
       print(body)                      # 如果發生錯誤，印出收到的內容
    return 'OK'                        # 驗證 Webhook 使用，不能省略

# 建立回覆圖片的函式
def reply_img(text):
    # 文字對應圖片網址的字典
    img = {
        '皮卡丘':'https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_Pikachu_art.png',
        '傑尼龜':'https://upload.wikimedia.org/wikipedia/en/5/59/Pok%C3%A9mon_Squirtle_art.png'
    }
    if text in img:
      return img[text]
    else:
      # 如果找不到對應的圖片，回傳 False
      return False

if __name__ == "__main__":
    run_with_ngrok(app)
    app.run()