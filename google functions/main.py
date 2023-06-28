
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json

from linebot import LineBotApi, WebhookHandler     # 載入 LINE Message API 相關函式庫
from linebot.models import MessageEvent, TextMessage, TextSendMessage  # 載入模組
from linebot.models import StickerSendMessage, ImageSendMessage, LocationSendMessage  # 載入模組
from linebot.models import PostbackAction, URIAction
from linebot.models import MessageAction, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, ButtonsTemplate

from firebase import firebase
# ccClub project 的Firebase Realtime database URL
url = 'https://ccclub-linebot-psytest-default-rtdb.firebaseio.com/'
fdb = firebase.FirebaseApplication(url, None)  # 初始化 Firebase Realtime database

# ccClub proect Line 的 token, secret
line_bot_api = LineBotApi(
    'MYoGxJuKZbYgOdIhfiiFbm9BKeFXQAwmgkgbGNENCtAqg1XTmRGdqCzxYMmK+5homRui1cNlrDFEOU3kYKBGgkV3GHwIVwox5oHRbAUFjBuP4DyaNKXklxP0qreeCwIy5TQdKHyY8sGwWmpZAUJ1agdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8ef1afb585b2ad36cbaf047e77e6e989')

points = 0  # 設定心理測驗分數(全局變量)
got_it = False  # 標誌變量
result = 0  # 設定測驗結果類型

def linebot(request):         #主要的程式碼(進入點)
    def test_result(points):  # 測驗結果計算公式
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

    body = request.get_data(as_text=True)  # 取得 request body 文字訊息
    json_data = json.loads(body)           # 將訊息轉換為 json 格式
    print(json_data)                       # 印出收到的訊息
    try:
       # 確認 secret 是否正確
       signature = request.headers['X-Line-Signature']
       handler.handle(body, signature)                   # 加入回傳的 headers
       tk = json_data['events'][0]['replyToken']         # 取得回傳訊息的 Token
       msg = json_data['events'][0]['message']['text']   # 取得 LINE 收到的文字訊息

       global points  # 引用全局變量
       global got_it
       global result

       def question1():
          line_bot_api.reply_message(tk, TemplateSendMessage(
             alt_text='ButtonsTemplate',
             template=ButtonsTemplate(
             thumbnail_image_url='https://img.dennyli.com/2019/11/1602040070-a708d22693d453d7d0df1e2855580f5b.png',
             title='Q1.想到夏天會讓你第一個聯想到下列哪一個選項?',
             text='依直覺回答哦～',
                  actions=[
                      MessageAction(
                          label='A. 海邊',
                          text='A. 海邊'
                          ),
                      MessageAction(
                          label='B. 西瓜',
                          text='B. 西瓜'
                          ),
                      MessageAction(
                          label='C. 啤酒',
                          text='C. 啤酒'
                          ),
                      MessageAction(
                          label='D. 剉冰',
                          text='D. 剉冰'
                          )
                      ]
                  )
              )
            )

       def question2():
          line_bot_api.reply_message(tk,TemplateSendMessage(
             alt_text='ButtonsTemplate',
             template=ButtonsTemplate(
             thumbnail_image_url='https://www.looper.com/img/gallery/weird-things-about-ash-and-pikachus-relationship/intro-1543321039.jpg',
             title = 'Q2.高溫走在路上熱到要融化,希望立馬來上一杯?',
             text='依直覺回答哦～',
             actions=[MessageAction(
                          label='A. 冰可樂/氣泡水',
                          text='A. 冰可樂/氣泡水'
                          ),
                      MessageAction(
                          label='B. 冰咖啡',
                          text='B. 冰咖啡'
                          ),
                      MessageAction(
                          label='C. 微冰無糖茶飲',
                          text='C. 微冰無糖茶飲'
                          ),
                      MessageAction(
                          label='D. 沁涼白開水',
                          text='D. 沁涼白開水'
                          )
                      ]
                  )
              )
            )

       def question3():
          line_bot_api.reply_message(tk,TemplateSendMessage(
             alt_text='ButtonsTemplate',
             template=ButtonsTemplate(
             thumbnail_image_url='https://poketouch.files.wordpress.com/2017/12/happy_may_and_bulbasaur_hugging_while_smiling_in_pokemon.jpg',
             title = 'Q3.晴朗無比的好天氣,你看見蔚藍天空的一朵雲,雲的形狀看起來像是?',
             text='依直覺回答哦～',
             actions=[MessageAction(
                          label='A. 催狂魔',
                          text='A. 催狂魔'
                          ),
                      MessageAction(
                          label='B. 一隻烏龜',
                          text='B. 一隻烏龜'
                          ),
                      MessageAction(
                          label='C. 是鯨魚',
                          text='C. 是鯨魚'
                          ),
                      MessageAction(
                          label='D. 就是一片雲該有的形狀',
                          text='D. 就是一片雲該有的形狀'
                          )
                      ]
                  )
              )
            )

       def question4():
          line_bot_api.reply_message(tk,TemplateSendMessage(
             alt_text='ButtonsTemplate',
             template=ButtonsTemplate(
             thumbnail_image_url='https://img.toy-people.com/member/167603694324.png',
             title = 'Q4.辦公室冷氣吹好吹滿,上班族必備小物必須有?',
             text='依直覺回答哦～',
             actions=[MessageAction(
                          label='A. 妮妮媽媽的兔兔',
                          text='A. 妮妮媽媽的兔兔'
                          ),
                      MessageAction(
                          label='B. 社畜以公司為家需要拖鞋',
                          text='B. 社畜以公司為家需要拖鞋'
                          ),
                      MessageAction(
                          label='C. 舒適午睡枕/毛毯',
                          text='C. 舒適午睡枕/毛毯'
                          ),
                      MessageAction(
                          label='D. 提醒喝水大水壺',
                          text='D. 提醒喝水大水壺'
                          )
                      ]
                  )
              )
            )

       def question5():
          line_bot_api.reply_message(tk,TemplateSendMessage(
             alt_text='ButtonsTemplate',
             template=ButtonsTemplate(
             thumbnail_image_url='https://assets.pokemon.com/assets/cms2/img/watch-pokemon-tv/seasons/season01/season01_ep11_ss01.jpg',
             title = 'Q5.暑假出遊但卻塞在高速公路上,這時需要音樂嗨起來,歌單想來點?',
             text='依直覺回答哦～',
             actions=[MessageAction(
                          label='A. 台味好！獨立搖滾聽團仔',
                          text='A. 台味好！獨立搖滾聽團仔'
                          ),
                      MessageAction(
                          label='B. Kpop韓團系列',
                          text='B. Kpop韓團系列'
                          ),
                      MessageAction(
                          label='C. 英文歌曲pop music',
                          text='C. 英文歌曲pop music'
                          ),
                      MessageAction(
                          label='D. 爵士樂 不死',
                          text='D. 爵士樂 不死'
                          )
                      ]
                  )
              )
            )

       if msg == '開始測驗':
        points = 0 # 重置測驗分數
        got_it = False
        result = 0

        line_bot_api.reply_message(tk,TemplateSendMessage(
           alt_text='ButtonsTemplate',
           template=ButtonsTemplate(
           thumbnail_image_url='https://img.dennyli.com/2019/11/1602040070-a708d22693d453d7d0df1e2855580f5b.png',
           title='每到夏天我要去哪邊～',
           text='依照直覺回答以下問題！',
           actions=[MessageAction(
                          label='Got it! 開始吧！',
                          text='Got it! 開始吧！'
                          ),
                    MessageAction(
                          label='算了，太晚我就不要了',
                          text='算了，太晚我就不要了'
                          )
                      ]
                  )
              ))

       elif msg == '算了，太晚我就不要了':
          points = 0 # 重置測驗分數
          got_it = False
          result = 0
          reply_bye_array = []                     # 回覆使用者拒絕的訊息陣列
          reply_bye_array.append( TextSendMessage(text='残念ですね。。。') )  # 回覆測驗結果訊息(description)
          reply_bye_array.append( ImageSendMessage(
             original_content_url = 'https://www.niusnews.com/upload/posts/po5_29953_1421316750.jpg',
             preview_image_url = 'https://www.niusnews.com/upload/posts/po5_29953_1421316750.jpg')) 
             # 皮卡丘哭哭圖
          line_bot_api.reply_message(tk, reply_bye_array)

       elif msg == 'Got it! 開始吧！':
          if not got_it:
             got_it = True
             question1()
          else:
             line_bot_api.reply_message(tk,TextSendMessage(
                text='請從 Q1 開始回答哦！'))

       elif msg in ['A. 海邊', 'B. 西瓜', 'C. 啤酒', 'D. 剉冰']:    # Q1 答案
          if got_it:
             fdb.put('/', 'Q1', 70 - ord(msg[0]) - 1) # 轉換代號為分數，並以同步新增，在節點Q1紀錄分數
             question2()                          # 收到答案後，提出下一題
             # 輸出資料庫內容檢查
             snapshot = fdb.get('/', 'Q1')
             print(snapshot)

       elif msg in ['A. 冰可樂/氣泡水', 'B. 冰咖啡', 'C. 微冰無糖茶飲', 'D. 沁涼白開水']: # Q2 答案
          if got_it:               
             fdb.put('/', 'Q2', 70 - ord(msg[0]) - 1) # 轉換代號為分數，並以同步新增，在節點Q2紀錄分數
             question3()                          # 收到答案後，提出下一題                       
             # 輸出資料庫內容檢查
             snapshot = fdb.get('/', 'Q2')
             print(snapshot)
    
       elif msg in ['A. 催狂魔', 'B. 一隻烏龜', 'C. 是鯨魚', 'D. 就是一片雲該有的形狀']: # Q3 答案
          if got_it:               
             fdb.put('/', 'Q3', 70 - ord(msg[0]) - 1) # 轉換代號為分數，並以同步新增，在節點Q3紀錄分數
             question4()                          # 收到答案後，提出下一題
             # 輸出資料庫內容檢查
             snapshot = fdb.get('/', 'Q3')
             print(snapshot)

       elif msg in ['A. 妮妮媽媽的兔兔', 'B. 社畜以公司為家需要拖鞋', 'C. 舒適午睡枕/毛毯', 'D. 提醒喝水大水壺']: # Q4 答案
          if got_it:               
             fdb.put('/', 'Q4', 70 - ord(msg[0]) - 1) # 轉換代號為分數，並以同步新增，在節點Q4紀錄分數
             question5()                          # 收到答案後，提出下一題
             # 輸出資料庫內容檢查
             snapshot = fdb.get('/', 'Q4')
             print(snapshot)

       elif msg in ['A. 台味好！獨立搖滾聽團仔', 'B. Kpop韓團系列', 'C. 英文歌曲pop music', 'D. 爵士樂 不死']:  # Q5 答案
        if got_it:
           fdb.put('/', 'Q5', 70 - ord(msg[0]) - 1) # 轉換代號為分數，並以同步新增，在節點Q5紀錄分數
           # 輸出資料庫內容檢查
           snapshot = fdb.get('/', 'Q5')
           print(snapshot)
           # 以字典格式輸出所有答案
           test_points = fdb.get('/', None)              
           print(test_points)          # 印出每題分數的字典
           points_list = list(test_points.values())
           print(points_list)          # 印出分數的串列
           total_points = sum([int(num) for num in points_list]) # 將分數串列轉為整數後，再加總，得到總分
           print(total_points)          # 印出總分
           result = test_result(total_points) # 執行測驗結果計算公式
           print(result)             # 印出測驗結果

           reply_array=[]            # 將要回覆的訊息放進陣列
           reply_array.append( TextSendMessage(text = result[0]))  # 回覆測驗結果訊息(type)
           reply_array.append( TextSendMessage(text = result[1]))  # 回覆測驗結果訊息(description)
           reply_array.append( ImageSendMessage(original_content_url = result[2], preview_image_url = result[2])) # 回覆測驗結果訊息(image)

           line_bot_api.reply_message(tk, reply_array)  # 以陣列回覆訊息
    except Exception as e:
        print('Error:', e)                        # 輸出詳細的錯誤訊息
    return 'OK'    