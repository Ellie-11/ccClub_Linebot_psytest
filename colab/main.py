# 主要程式碼 main.py
from flask_ngrok import run_with_ngrok          # colab 使用，本機環境請刪除
from flask import Flask, request, session
import os

import json

from linebot import LineBotApi, WebhookHandler     # 載入 LINE Message API 相關函式庫
from linebot.models import MessageEvent, TextMessage, TextSendMessage  # 載入模組
from linebot.models import StickerSendMessage, ImageSendMessage, LocationSendMessage  # 載入模組
from linebot.models import PostbackAction, URIAction
from linebot.models import MessageAction, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, ButtonsTemplate
from linebot.models import FlexSendMessage, BubbleContainer, ImageComponent
from linebot.exceptions import InvalidSignatureError

from firebase import firebase
# ccClub project 的Firebase Realtime database URL
url = 'https://ccclub-linebot-psytest-default-rtdb.firebaseio.com/'
fdb = firebase.FirebaseApplication(url, None)  # 初始化 Firebase Realtime database

app = Flask(__name__, root_path=os.getcwd())             # 初始化 Flask

# ccClub proect Line 的 token, secret
line_bot_api = LineBotApi(
    'MYoGxJuKZbYgOdIhfiiFbm9BKeFXQAwmgkgbGNENCtAqg1XTmRGdqCzxYMmK+5homRui1cNlrDFEOU3kYKBGgkV3GHwIVwox5oHRbAUFjBuP4DyaNKXklxP0qreeCwIy5TQdKHyY8sGwWmpZAUJ1agdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8ef1afb585b2ad36cbaf047e77e6e989')

points = 0  # 設定心理測驗分數(全局變量)
start = False  # 測驗開始標誌變量
result = 0  # 設定測驗結果類型

#測驗問題1
q1_title = '1.說到夏天，你第一個聯想到的是？'
q1_choice = { 'A':'海邊', 'B':'西瓜', 'C':'啤酒', 'D':'剉冰' }
#測驗問題2
q2_title = '2.高溫走在路上熱到要融化，希望立馬來上一杯？'
q2_choice = { 'A':'冰可樂/氣泡水', 'B':'冰咖啡', 'C':'微冰無糖茶飲', 'D':'沁涼白開水' }
#測驗問題3
q3_title = '3.晴朗無比的好天氣，你看見蔚藍天空的一朵雲，雲的形狀看起來像是？'
q3_choice = { 'A':'催狂魔', 'B':'一隻烏龜', 'C':'是鯨魚', 'D':'就是一片雲該有的形狀' }
#測驗問題4
q4_title = '4.辦公室冷氣吹好吹滿，上班族必備小物必須有？'
q4_choice = { 'A':'妮妮媽媽的兔兔', 'B':'社畜以公司為家需要拖鞋', 'C':'舒適午睡枕/毛毯', 'D':'提醒喝水大水壺' }
#測驗問題5
q5_title = '5.暑假出遊但卻塞在高速公路上，這時需要音樂嗨起來，歌單想來點？'
q5_choice = { 'A':'台味好！獨立搖滾聽團仔', 'B':'Kpop韓團系列', 'C':'英文歌曲pop music', 'D':'爵士樂 不死' }

@app.route("/", methods=['POST'])
def linebot(): #主要的程式碼(進入點)
    def test_result(points):                     # 測驗結果計算公式
       type_a = '人人稱羨的快樂阿宅94你'
       des_a = '不用前進世界的盡頭，也能有滿足於自我的快樂！沒有哪裡比待在家裡更適合你！無論是追劇或是離不開床，擁有冷氣就擁有純粹的快樂，不用特別去哪開運。'
       img_a = 'https://i.imgur.com/WoicAgS.jpeg'

       type_b = '世界祥和的溫柔派～'
       des_b = '書店、花店或是逛市集都是你充電的好去處！原本習慣緩和生活步調的你，容易在夏日熱氣蒸騰之下顯得無精打采，擁有豐富藏書或是繽紛顏色的場所，能提升你的活力，帶來開運的效果。'
       img_b = 'https://pica.zhimg.com/50/v2-6b091ed37be61ff3e8c87f9b2d42b20b_720w.jpg'

       type_c = '你是忠於自我又富有想像力的哲學家'
       des_c = '別具特色的咖啡廳、電影院或是慵懶舒適的酒吧最適合你。看著外頭的高溫烤晒日常，窩在舒適的空間內喝上一杯，或看部有趣的電影，都有助於你跳出思緒上的迴圈。'
       img_c = 'https://image1.gamme.com.tw/news2/2020/05/70/o5eYoaWblaWZqg.jpg'

       type_d = '你率真又自然～'
       des_d = '適合徜徉大自然，走入山林感受山的遼闊與平靜，為你淨化庸碌瑣事積累的壓力，沉浸於夏日生意盎然的森林，不僅適合避開夏日燠熱，更是你的沉澱好所在。'
       img_d = 'https://sw.cool3c.com/user/93262/2023/3a646ba5-c66c-43fc-a32a-9ffbb0cdc6ef.jpg'

       type_e = '熱血仔是你！'
       des_e = '下海衝浪或浮潛都讓你感覺真實擁抱夏天，最適合來到與海相關的場景，吸滿熱情陽光與粗獷海味之後，最能為你打開心的能量！'
       img_e = 'https://cdn2.ettoday.net/images/1780/1780413.jpg'

       if points <= 8:
          test_type = 'A'
          return [type_a, des_a, img_a]
       elif points > 8 and points <= 11:
          test_type = 'B'
          return [type_b, des_b, img_b]
       elif points > 11 and points <= 14:
          test_type = 'C'
          return [type_c, des_c, img_c]
       elif points > 14 and points <= 17:
          test_type = 'D'
          return [type_d, des_d, img_d]
       else:
          test_type = 'E'
          return [type_e, des_e, img_e]

    def check_points():
       check_q1 = fdb.get('/', 'Q1',) != None             # 檢查是否有Q1答案，若沒有，則為 False
       check_q2 = fdb.get('/', 'Q2',) != None             # 檢查是否有Q2答案，若沒有，則為 False
       check_q3 = fdb.get('/', 'Q3',) != None             # 檢查是否有Q3答案，若沒有，則為 False
       check_q4 = fdb.get('/', 'Q4',) != None             # 檢查是否有Q4答案，若沒有，則為 False
       check_q5 = fdb.get('/', 'Q5',) != None             # 檢查是否有Q5答案，若沒有，則為 False
       if not (check_q1 and check_q2 and check_q3 and check_q4 and check_q5):
           return False                       # 如果有任一個為 False，就回傳 False
       else:
           return True                        # 反之如果都有答案，就回傳 True

    def reset():                         # 執行重置測驗
       points = 0                       # 重置測驗分數
       start = False                      # 將開始測驗標誌改為 False
       result = 0                       # 重置測驗結果
       fdb.delete('/', None)                  # 將 firebase 資料全部清空

    body = request.get_data(as_text=True)             # 取得 request body 文字訊息
    json_data = json.loads(body)                  # 將訊息轉換為 json 格式
    print(json_data)                         # 印出 Linebot 收到的訊息
    try:
       signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
       handler.handle(body, signature)              # 綁定訊息回傳的相關資訊
       tk = json_data['events'][0]['replyToken']         # 取得回傳訊息的 Token
       msg = json_data['events'][0]['message']['text']      # 取得 收到的文字訊息
       tp = json_data['events'][0]['message']['type']      # 取得 收到的訊息類型
       user_id = json_data['events'][0]['source']['userId']   # 取得使用者 ID

       global points  # 引用全局變量
       global start
       global result

       def send_question1():                        # 送出測驗Q1
          if fdb.get('/', 'Q1') != None :           # 每次送出問題前，如果原本該題有分數，就將資料清空
            fdb.delete('/', 'Q1')
          line_bot_api.reply_message(tk, TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://m.media-amazon.com/images/M/MV5BNmYyZDgyZjItNTkxNC00OTUxLTlkZjAtODg3NDM2ZGE1ODlhXkEyXkFqcGdeQXVyOTA1ODU0Mzc@._V1_FMjpg_UX1000_.jpg',
              # 小智和神奇寶貝們的奔跑圖
              title = q1_title,
              text='依直覺回答哦～',
              actions=[MessageAction(
                  label = q1_choice['A'],        # 取得選項字串
                  text = q1_choice['A'],
                  ),
                  MessageAction(
                  label = q1_choice['B'],
                  text = q1_choice['B']
                  ),
                  MessageAction(
                  label = q1_choice['C'],
                  text = q1_choice['C']
                  ),
                  MessageAction(
                  label = q1_choice['D'],
                  text = q1_choice['D']
                  )
                  ]
              )))

       def send_question2():                        # 送出測驗Q2
          if fdb.get('/', 'Q2') != None :           # 每次送出問題前，如果原本該題有分數，就將資料清空
            fdb.delete('/', 'Q2')
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://www.looper.com/img/gallery/weird-things-about-ash-and-pikachus-relationship/intro-1543321039.jpg',
              # 皮卡丘鄙視小智圖
              title = q2_title,
              text = '依直覺回答哦～',
              actions=[MessageAction(
                  label = q2_choice['A'],        # 取得選項字串
                  text = q2_choice['A'],
                  ),
                  MessageAction(
                  label = q2_choice['B'],
                  text = q2_choice['B']
                  ),
                  MessageAction(
                  label = q2_choice['C'],
                  text = q2_choice['C']
                  ),
                  MessageAction(
                  label = q2_choice['D'],
                  text = q2_choice['D']
                  )
                  ]
              )))

       def send_question3():                        # 送出測驗Q3
          if fdb.get('/', 'Q3') != None :           # 每次送出問題前，如果原本該題有分數，就將資料清空
            fdb.delete('/', 'Q3')
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://poketouch.files.wordpress.com/2017/12/happy_may_and_bulbasaur_hugging_while_smiling_in_pokemon.jpg',
              # 小瑤抱妙蛙種子圖
              title = q3_title,
              text = '依直覺回答哦～',
              actions=[MessageAction(
                  label = q3_choice['A'],        # 取得選項字串
                  text = q3_choice['A'],
                  ),
                  MessageAction(
                  label = q3_choice['B'],
                  text = q3_choice['B']
                  ),
                  MessageAction(
                  label = q3_choice['C'],
                  text = q3_choice['C']
                  ),
                  MessageAction(
                  label = q3_choice['D'],
                  text = q3_choice['D']
                  )
                  ]
              )))

       def send_question4():                        # 送出測驗Q4
          if fdb.get('/', 'Q4') != None :           # 每次送出問題前，如果原本該題有分數，就將資料清空
            fdb.delete('/', 'Q4')
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://img.toy-people.com/member/167603694324.png',
              # 傑尼龜墨鏡圖
              title = q4_title,
              text = '依直覺回答哦～',
              actions=[MessageAction(
                  label = q4_choice['A'],        # 取得選項字串
                  text = q4_choice['A'],
                  ),
                  MessageAction(
                  label = q4_choice['B'],
                  text = q4_choice['B']
                  ),
                  MessageAction(
                  label = q4_choice['C'],
                  text = q4_choice['C']
                  ),
                  MessageAction(
                  label = q4_choice['D'],
                  text = q4_choice['D']
                  )
                  ]
              )))

       def send_question5():                        # 送出測驗Q5
          if fdb.get('/', 'Q5') != None :           # 每次送出問題前，如果原本該題有分數，就將資料清空
            fdb.delete('/', 'Q5')
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/seasons/season01/season01_ep11_ss01.jpg',
              # 小火龍瞪皮卡丘圖
              title = q5_title,
              text = '依直覺回答哦～',
              actions=[MessageAction(
                  label = q5_choice['A'],        # 取得選項字串
                  text = q5_choice['A'],
                  ),
                  MessageAction(
                  label = q5_choice['B'],
                  text = q5_choice['B']
                  ),
                  MessageAction(
                  label = q5_choice['C'],
                  text = q5_choice['C']
                  ),
                  MessageAction(
                  label = q5_choice['D'],
                  text = q5_choice['D']
                  )
                  ]
              )))

       if msg in ['開始測驗','再玩一次']:                    # 開始測驗樣板
        reset()  # 重置測驗

        line_bot_api.reply_message(tk,TemplateSendMessage(
            alt_text='ButtonsTemplate',
            template=ButtonsTemplate(
            thumbnail_image_url='https://img.dennyli.com/2019/11/1602040070-a708d22693d453d7d0df1e2855580f5b.png',
            # 快龍開心圖
            title='每到夏天我要去哪邊～',
            text='Are you ready?',
            actions=[MessageAction(
                label='Got it! 開始吧！',
                text='Got it! 開始吧！'
                ),
                MessageAction(
                label='算了，太晚我就不要了',
                text='算了，太晚我就不要了'
                )
                ]
            )))

       elif msg == '算了，太晚我就不要了':             # 使用者拒絕測驗
          reset()                         # 重置測驗
          reply_bye_array = []                         # 回覆使用者拒絕的訊息陣列
          reply_bye_array.append( TextSendMessage(text='残念ですね。。。沒關係 QQ') )  # 回覆測驗結果訊息(description)
          reply_bye_array.append( FlexSendMessage(               # flex message 內容
              alt_text='點我開始測驗',
              contents = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "kilo",
      "body": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://www.niusnews.com/upload/posts/po5_29953_1421316750.jpg",
            "size": "full",
            "margin": "none",
            "position": "relative",
            "gravity": "center",
            "aspectMode": "cover",
            "aspectRatio": "20:13",
            "align": "center"
          },
          {
            "type": "text",
            "text": "點我開始測驗",
            "position": "relative",
            "align": "start",
            "gravity": "center",
            "wrap": False,
            "margin": "lg",
            "color": "#6e89b2",
            "weight": "bold",
            "style": "normal",
            "decoration": "none",
            "action": {
              "type": "message",
              "label": "action",
              "text": "開始測驗"
            }
          }
        ],
        "position": "relative"
      }
    }
  ]
}) )
          line_bot_api.reply_message(tk, reply_bye_array)

       elif msg == 'Got it! 開始吧！':
          fdb.delete('/', None)                 # 每次開始測驗前，都將所有資料清空
          if start == False:                  # 若原本開始測驗標誌是 False，則改為 True
            start = True
            send_question1()
          else:
            send_question1()

       elif msg in q1_choice.values() and start:               # 處理 Q1 答案
          new_q1_choice = {v:k for k, v in q1_choice.items()}   # 把選項字典 value, key 互換
          ans_num = new_q1_choice.get(msg)              # 從新的字典取得答案編號
          fdb.put('/', 'Q1', 70 - ord(ans_num) - 1)       # 轉換代號為分數，並以同步新增，在節點Q1紀錄分數
          snapshot = fdb.get('/', 'Q1')              
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:                         # 當開始標記為真
              send_question2()                  # 收到答案後，提出下一題

       elif msg in q2_choice.values():               # 處理 Q2 答案
          new_q2_choice = {v:k for k, v in q2_choice.items()}
          ans_num = new_q2_choice.get(msg)
          fdb.put('/', 'Q2', 70 - ord(ans_num) - 1)     # 轉換代號為分數，並以同步新增，在節點Q2紀錄分數
          snapshot = fdb.get('/', 'Q2')      
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question3()                   # 收到答案後，提出下一題
             
       elif msg in q3_choice.values():               # 處理 Q3 答案
          new_q3_choice = {v:k for k, v in q3_choice.items()}
          ans_num = new_q3_choice.get(msg)
          fdb.put('/', 'Q3', 70 - ord(ans_num) - 1)     # 轉換代號為分數，並以同步新增，在節點Q3紀錄分數
          snapshot = fdb.get('/', 'Q3') 
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question4()                  # 收到答案後，提出下一題


       elif msg in q4_choice.values():               # 處理 Q4 答案
          new_q4_choice = {v:k for k, v in q4_choice.items()}
          ans_num = new_q4_choice.get(msg)
          fdb.put('/', 'Q4', 70 - ord(ans_num) - 1)      # 轉換代號為分數，並以同步新增，在節點Q4紀錄分數
          snapshot = fdb.get('/', 'Q4')
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question5()                  # 收到答案後，提出下一題


       elif msg in q5_choice.values():               # 處理 Q5 答案
          new_q5_choice = {v:k for k, v in q5_choice.items()}
          ans_num = new_q5_choice.get(msg)
          fdb.put('/', 'Q5', 70 - ord(ans_num) - 1)      # 轉換代號為分數，並以同步新增，在節點Q5紀錄分數
          snapshot = fdb.get('/', 'Q5')             
          print(snapshot)                      # 輸出資料庫內容檢查
          check = check_points()                   # 檢查每題是否都有分數
          print(check)

          if start and check:                    # 如果 start 為真且 check 為真
            test_points = fdb.get('/', None)            # 取出每題分數，並以字典紀錄
            print(test_points)                     # 印出每題分數的字典
            points_list = list(test_points.values())         # 把字典的值取出轉為串列
            print(points_list)                     # 印出分數的串列
            total_points = sum([int(num) for num in points_list]) # 將分數串列轉為整數後，再加總，得到總分
            print(total_points)                     # 印出總分
        

            result = test_result(total_points)            # 執行測驗結果計算公式
            print(result)                        # 印出測驗結果

            reply_result_array=[]                       # 將要回覆結果的訊息放進陣列
            reply_result_array.append( TextSendMessage(text = result[0]))  # 回覆測驗結果訊息(type)
            reply_result_array.append( TextSendMessage(text = result[1]))  # 回覆測驗結果訊息(description)
            reply_result_array.append( ImageSendMessage(original_content_url = result[2],
                          preview_image_url = result[2])) # 回覆測驗結果訊息(image)
            reply_result_array.append( FlexSendMessage(         # 回覆flex message 內容
              alt_text='再玩一次',
              contents = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "kilo",
      "body": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            # 伊布燦笑圖
            "url": "https://mrmad.com.tw/wp-content/uploads/2016/07/pokemon-go-eevee-evolution-cover.png",
            "size": "full",
            "margin": "none",
            "position": "relative",
            "gravity": "center",
            "aspectMode": "cover",
            "aspectRatio": "20:13",
            "align": "center"
          },
          {
            "type": "text",
            "text": "再玩一次",
            "position": "relative",
            "align": "start",
            "gravity": "center",
            "wrap": False,
            "margin": "lg",
            "color": "#6e89b2",
            "weight": "bold",
            "style": "normal",
            "decoration": "none",
            "action": {
              "type": "message",
              "label": "action",
              "text": "再玩一次"
            }
          }
        ],
        "position": "relative"
      }
    }
  ]
}) )
            line_bot_api.reply_message(tk, reply_result_array)        # 以陣列回覆訊息
            reset()                              # 執行重置測驗

          else:                            # 反之，如果開始標誌或check為 False
            reset()                         # 執行重置測驗
            reply_restart_array=[]                       # 將要回覆重新開始的訊息放進陣列
            reply_restart_array.append( TextSendMessage(text='測驗一共有5題哦，一起做完吧！') )  # 回覆測驗結果訊息(description)
            reply_restart_array.append( FlexSendMessage(               # flex message 內容
              alt_text='重新開始測驗',
              contents = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "kilo",
      "body": {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "image",
            "url": "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2023/03/pokemon-horizons-captain-pikachu-feature-image.jpg",
            "size": "full",
            "margin": "none",
            "position": "relative",
            "gravity": "center",
            "aspectMode": "cover",
            "aspectRatio": "20:13",
            "align": "center"
          },
          {
            "type": "text",
            "text": "重新開始測驗",
            "position": "relative",
            "align": "start",
            "gravity": "center",
            "wrap": False,
            "margin": "lg",
            "color": "#6e89b2",
            "weight": "bold",
            "style": "normal",
            "decoration": "none",
            "action": {
              "type": "message",
              "label": "action",
              "text": "開始測驗"
            }
          }
        ],
        "position": "relative"
      }
    }
  ]
}))
            line_bot_api.reply_message(tk, reply_restart_array)

    except Exception as e:
        print('Error:', e)                        # 輸出詳細的錯誤訊息
    return 'OK'

if __name__ == "__main__":
  run_with_ngrok(app)
  app.run()