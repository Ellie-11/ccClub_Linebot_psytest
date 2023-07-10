import json
import openai #匯入 open ai 模組

from linebot import LineBotApi, WebhookHandler     # 載入 LINE Message API 相關函式庫
from linebot.models import MessageEvent, TextMessage, TextSendMessage  # 載入模組
from linebot.models import StickerSendMessage, ImageSendMessage, LocationSendMessage  # 載入模組
from linebot.models import PostbackAction, URIAction
from linebot.models import MessageAction, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, ButtonsTemplate
from linebot.models import FlexSendMessage, BubbleContainer, ImageComponent # 載入模組
from linebot.exceptions import InvalidSignatureError

from firebase import firebase
# ccClub project 的Firebase Realtime database URL
url = 'https://ccclub-linebot-psytest-default-rtdb.firebaseio.com/'
fdb = firebase.FirebaseApplication(url, None)  # 初始化 Firebase Realtime database

# ccClub proect Line 的 token, secret
token = 'MYoGxJuKZbYgOdIhfiiFbm9BKeFXQAwmgkgbGNENCtAqg1XTmRGdqCzxYMmK+5homRui1cNlrDFEOU3kYKBGgkV3GHwIVwox5oHRbAUFjBuP4DyaNKXklxP0qreeCwIy5TQdKHyY8sGwWmpZAUJ1agdB04t89/1O/w1cDnyilFU='
secret = '8ef1afb585b2ad36cbaf047e77e6e989'

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

#主要的程式碼(進入點)
def linebot(request): 
    def test_result(points):                     # 測驗結果計算公式
       type_a = '人人稱羨的快樂阿宅94你'
       des_a = '不用前進世界的盡頭，也能有滿足於自我的快樂！沒有哪裡比待在家裡更適合你！無論是追劇或是離不開床，擁有冷氣就擁有純粹的快樂，不用特別去哪開運。'
       img_a = 'https://lh3.googleusercontent.com/pw/AIL4fc_lhEzWWLfcVA1yMcGI910ihdB_-NK-WhC7W7oKnoVbFrJTmJp_1RDADDTblK0apoqc-lonkIuiRw0hgNImCPwZkZKKaObONlxArYgbbT-kwWm61-tPalJc52foHjTQkkmUKgHLvbdXz9wnyDua-gP2pjS-Ewwo8y1Dxf5E6m3IOjoiZaA7r3mOOKxFPLoXm6oGLWRnVXdte5dPy6af_2W8RoU8CbvprUopYYJZulFKAfY7hOyXNVE0MRvPI5Z3jSBFOFJrzrCFzhHcS_8avj_T1h7qt3xISlCVZIZ6kyDFMgTgnsqG1hZWZqxPm_tac3KWDli7OV8SLFQuX3X7ob7N5OM10vynFdsoa8RMc2br4k-G7RuQ6eZ0x3bNhKgYSFVCiLUsToHBboNA0D7fRyxgsRYhFM6F656U5rmlZwEln27P-PP9SaFluM7-KncaHv5W8Hl4nTNUDXbVVhtewCvQ4eU0LaJibf4XIgB0cx7YGOw0oPMRIDl6zCz14KHzXooLLZSbkWZ-U4lAW_OHNewH4X44IcvECAA-l-mdQytvMXNC6xJx0Jw9hGXJHmQS1sNdbEporYJfKmWYQaDJJLRwJldmqWwX_CA4E3N3keYzBYSBwkDE6_47fP-9_oxUL0-kGRS6bHciKwQPsbgCI47ujieGtHpdPFR_OIIp2q_J9Umo9gzhgucxiDjJyHTzsHLCBV1my8diylMjzg00d4yS47gJDy7ps2FUGwmAvfQtIe71lHEBWPrEXsb6MiIg6xFlkqfVrs7LlH7nGpKW8bM7j4Hwqd9cwPEd_GO1qc2Vj5oDYo5E-rRg2L_SSbbfwHT6N_IssZm6r0B159aZGKt5bBNp-4_8xbbVsfPx4kzW2VJksynzh4GTYhdn26KbxSQkuQSu--BrDKRAtSh4=w1337-h902-s-no?authuser=0'

       type_b = '世界祥和的溫柔派～'
       des_b = '書店、花店或是逛市集都是你充電的好去處！原本習慣緩和生活步調的你，容易在夏日熱氣蒸騰之下顯得無精打采，擁有豐富藏書或是繽紛顏色的場所，能提升你的活力，帶來開運的效果。'
       img_b = 'https://lh3.googleusercontent.com/pw/AJFCJaWZKRTUSAhhGyObgQUXgP-AGWnO185-QK5v1_3fzeEJgLVNpUfPYH5_t4s4vD8D_WJAxjwNei0oQWAWJ8Zd1rfihAXFpU8PrKCi5La2ZPHwtwHTwmzAfHngAe5JUuWkB55PBf8Sa7u28Z-yBTlcyGgMxqJaORbDRaPFgQKnTipr-vnuoBFbyC7X4stvtosDqKRNfdx796KAaE4N2-vCo9q3vW3-E2h_fOSh4qZGeOGG2ZF7QYRpTONxPprfuEBOjLhrFJJYZnXKDhB-z7MmJFSdhFEZu8lcHU3Rphu9_PIzwBJvHDfu3IxXAIciRL822bZowjIO_5ia_8_QeDYf1ojdCVoFvJoTssgvNj2BC9j2jC1CwFVu8_XkBG4JwN0H1G-ihc7YxvFY-kNkU0GlJrVWgAQctX8_zFj6gOXpw-BhhNwzkSU3qVaQL2Z0GexdB8SZtHKWAg021HTXvznVZhf9RwgZl_V-Sx1e8JYiybniNJygVUHNSzRoySjWRKoH2nb-YmYanQI_WLgdBzbvEltm_IjEtRrmubdXoVxTc-9HNuCsRWVQLTxE1G8YbD7lCxM0ffjshMdGZ_mHR7M3JJQMbWjI7UFKnn8xNzdJbcWHnqiQldLrEwMzYsRlX7QFrdB3H47tpT_ctAvw7Pw_3Ftm4F1RaZ8T7q_vgoGK3cWhsl3_lxKlh1HutYXoBUc5UD8T4wvCVsmQdyOd6_BmPnvOElG70YxSR4UyEZiBTcay0gbEqrDq6VbFfb4gqn2W8hc6yQRG5hO31Vo2SGKSBZDLWou9Hjjex1AH10LW55MtKEIGqRecsfLQk8aNEIDLRC9lznER8wIlT_OmdxxgUMVHLa7Vo_E123xQilbyaAhNb0LHrm55TzTCafcYufOvsTeINKGQhcH5WrPGzCBZ=w1043-h902-s-no?authuser=0'

       type_c = '你是忠於自我又富有想像力的哲學家'
       des_c = '別具特色的咖啡廳、電影院或是慵懶舒適的酒吧最適合你。看著外頭的高溫烤晒日常，窩在舒適的空間內喝上一杯，或看部有趣的電影，都有助於你跳出思緒上的迴圈。'
       img_c = 'https://lh3.googleusercontent.com/pw/AIL4fc_03HRATrlK4cX6m8y_kiCNEeDJ-VWSD_kLdH5BQcVWyHoJMKmlcS98hY6SxSAqqV6shIBTE1xc1oU_sUqJlhhjh6NYfTmD8CwGC8EHVrwl8ntZZ-F7QKWR2-sJ9-m4YrelJH9-bLJ6x9EXn-Zx1RRwX4SOTLmjAAErVbO_2dcTx-beopDrlZ6Rd_ww8LuE52_LzB2JL1ogSQV1tIloWWwSYqU71141BmQkohJwogx8K_jRQZ-ddP2zXJcPPrwtQvPRHfN-IHe6g3evdOhbd6HStTkxGdFZDkEtLQ9aTAE1V1qO4Sbhloc7ztl140CBVaher11BGp1waeT-sV43ArdZVARDr6XpRFfQj9-xYe5GPZ2Wr3bPjvGByFzhZ90Do1MD2rjMun-7YLVPxLebxKJEa3bLD-792nR-VsMSieT29HkHJR82E4_i5DUBvSj4kt_GCxc7jXOhXBHOylCNeG16Sp1zQhLjqdVeOXmh8cR-nlagOC3pjQZ0azfM2u5745mDolcbI7OG93h3DnPrWl6p0cR8SFuCVjEZJn5QnDhjsJ2EKocSAE2QbxMJqarZ0bNTukar0RQmCSFAkU8wrAr610tbifmIKVT1qcGabuu2SPrXDCFmTheSJLV5J2CYPa22jPQuDzW69jOu7xDjJ5ON-5U8lqA_1yCypi-AxcjBupaw4IZkGe-Ty-VMnzyLVF7DnUad3eZugcdI_9Lhin34lSZw0ERpDd0AOgQ_2p044j5GttwHkqfwb9GuWlDiOy_JvDuqWSXyFOIJjLGx1a4EGYy-Bgdz_3qpexmp_o2rL_vKi3JB-H6I8kpWXoiHXI5pvQAO28CG1UTW14IVhS5Bk6CY4kMmRr71tD4sdgK-Q6l6e5RQot8jVRHuNAFdQkhpdzaK41FgDzRWhbmE=w1203-h902-s-no?authuser=0'

       type_d = '你率真又自然～'
       des_d = '適合徜徉大自然，走入山林感受山的遼闊與平靜，為你淨化庸碌瑣事積累的壓力，沉浸於夏日生意盎然的森林，不僅適合避開夏日燠熱，更是你的沉澱好所在。'
       img_d = 'https://lh3.googleusercontent.com/pw/AIL4fc_Rys84IS3-g78RHO02CzD3O7qDmD_cGxp3R0fiq7SI8fV5k2iQJsrula_0oSbpT_3wX80_Zu_xl20W47vAjRL2CtI7Kf91-_RxpU6ge6tmCxhbAp3RZ-7XSmdj49WERAUSUWWWN-Qq3rmrq9japjj3pul8yf__uD0jMtI00l4b80-aWV9iJjW8YJed3FDrQemhS4CZIm6KQbByndu7FW4JfFPI-ilupCcOnLeYdiW8riE5Z8kbRuNpvh27sF9W4Y6-IDVoBV0JaKaRQn1bc0lMVepcaepNiecq1bEJLAMJEUzLSn-xDsdoX1AYC4MHL2Id6iu7KXrNKAAAFRSzvzQiPEB1MHDGLOdd2ejQ-ykaQMsT3JRu_LJ3cWK50YOzNuf_pghG1bJ7jS-UD5ZaOObPtGhZdM2PlrVL9cvxQwd_eHxPtNt9OQ6ethUhomQ52BufVCBJ2QGQ5QwHYw36RjwR70iWaMcbDD6LRUCyF2U2uCW8b9AT4826hDlOLQl3stHX8y4zsivzKQthA4tO4QlveZtTxGZ-4_QjfQqtZNVUBTDZKbNzQAzqV5a6q3QMo9K2hc9OwBJsNyrWMoOQmlNeLuI54E6NhbKLy91RgpaqcXNibZxgj_Ae2MeIxfIIINTfvckWuNfYXEFqtaj4Jde12gHvf1Hd9iI13heUYzW1HO2ffL3OlNXDns3DJHj_1EMQdf_r_WMaNp6jq2FcnaHb59ejuSWgGWIIyHZAHl8vBzNcLFs-6NqQ6pv6wPMu94C3AchRh8dgqr_ySEF7bPVQpX4RXl45Y_dp4h12QuoQTBwr0JtCIYX6YQJXPZgCO8LSH_oHxCo5Xsg5BhefZGj8Bhwhwe_ePtx9Cf8m0zn-2IdgTZ9Sve_qnWvUP5W_BuH0DIbbHOiMxvuE54Ev=w1203-h902-s-no?authuser=0'

       type_e = '熱血仔是你！'
       des_e = '下海衝浪或浮潛都讓你感覺真實擁抱夏天，最適合來到與海相關的場景，吸滿熱情陽光與粗獷海味之後，最能為你打開心的能量！'
       img_e = 'https://lh3.googleusercontent.com/pw/AIL4fc9P7StnnZbTpNNhwpMZAKmb7fuNc8-YD7QVKSxZiUwM1o3pCAUIwu4rpgPcxhMN-7KDJzFgl0wKnh3sXgoIjf1wisLXE1ZMMdsW2_WEb_jq5pyVh5CK9K07OWZagPP-TU9InDjDuz3oh09KWGWP6Q4n9kOabNG_n3btTWvzfR3Q8p5hf8U9l6rhpHx5mlhSz0VCRVbqMrQkrN81jzxHmfbbZbvlwYEkO7TjaApm18uCNWxUfJB2-BCaP3hVZeTRE5HN_YtlF2xHMoB_yU4Cv9OKlZjQZqdQ_aSSruXTR_zHS5yXSONgjKH3oofglPkPbGGl8SvM76-8ft6UwKmAyciRLgoCKLV3P5yUr6BH4p6f2fM1OuYOTWPhpWQ_e_n2jsm4MJjUhL75ax11ZO-Pste5jJB24JegCqwiwYI4wOHcp8jrTkSy8BnnjVA3PBlGT2YuaGlQPztrktY1qMGewm91nkwhFLH0zGjbyYYLKEI0XzjNsFq5RYoX_h5oOzLiDtGO65SJAjitKiwNI6tF1kBjYZSWzVZQjV3roOlqDqLKeWl6bx1KCYOgIv-U0vj2VWuKaFDw92V5lyNSZJZewGImdSf0oFTMLHkrd1bw6J9z2UTFDD9AfDhsD30mizHbzZY3JKH0_skM_ySFYrlBiNMDAqlO-4RgOioNZ1XPWy5wii53nyXjwcfBvef5rYhS0wigtTeqFIx7-z8xsl3ssicUi8k_6OKlZ5X7bVB_PM3xzygtrzvj9-msftYHXbzyiJPOJNU6Jz74FbDZQPb4fQ4FCfAWiU4AkWdOhxO21dDhkUMz1Pg1N9ILUGlB0tv8wljKvzbxwrm_PLJtWWS2X3VTgo4yA4THd5InQwkTsl8Gett-yekxRkgs-XqqtpLouRFNqW3NQlyWDDsArmUZ=w1520-h902-s-no?authuser=0'

       if points <= 8:
          test_type = 'A'              # '人人稱羨的快樂阿宅94你'
          return [type_a, des_a, img_a]
       elif points > 8 and points <= 11:
          test_type = 'B'              # '世界祥和的溫柔派～'
          return [type_b, des_b, img_b]
       elif points > 11 and points <= 14:
          test_type = 'C'              # '你是忠於自我又富有想像力的哲學家'
          return [type_c, des_c, img_c]
       elif points > 14 and points <= 17:
          test_type = 'D'              # '你率真又自然～'
          return [type_d, des_d, img_d]
       else:
          test_type = 'E'              # '熱血仔是你！'
          return [type_e, des_e, img_e]
          
    def check_points():
       check_q1 = fdb.get('/', f'{user_id}/Q1') != None             # 檢查是否有Q1答案，若無，則為 False
       check_q2 = fdb.get('/', f'{user_id}/Q2') != None             # 檢查是否有Q2答案，若無，則為 False
       check_q3 = fdb.get('/', f'{user_id}/Q3') != None             # 檢查是否有Q3答案，若無，則為 False
       check_q4 = fdb.get('/', f'{user_id}/Q4') != None             # 檢查是否有Q4答案，若無，則為 False
       check_q5 = fdb.get('/', f'{user_id}/Q5') != None             # 檢查是否有Q5答案，若無，則為 False
       if not (check_q1 and check_q2 and check_q3 and check_q4 and check_q5):
           return False                       # 如果有任一個為 False，就回傳 False
       else:
           return True                        # 反之如果都有答案，就回傳 True

    def reset():                         # 執行重置測驗
       points = 0                       # 重置測驗分數
       start = False                      # 將開始測驗標誌改為 False
       result = 0                       # 重置測驗結果
       fdb.delete('/', f'{user_id}')    # 清空firebase裡，該userid的所有資料

    body = request.get_data(as_text=True)             # 取得 request body 文字訊息
    json_data = json.loads(body)                      # 將訊息轉換為 json 格式
    print(json_data)                                   # 印出 Linebot 收到的訊息
    try:
       line_bot_api = LineBotApi(token)
       handler = WebhookHandler(secret)
       signature = request.headers['X-Line-Signature']   # 加入回傳的 headers
       handler.handle(body, signature)                   # 綁定訊息回傳的相關資訊
       tk = json_data['events'][0]['replyToken']         # 取得回傳訊息的 Token
       msg = json_data['events'][0]['message']['text']   # 取得 LINE 收到的文字訊息
       tp = json_data['events'][0]['message']['type']      # 取得 收到的訊息類型
       user_id = json_data['events'][0]['source']['userId']   # 取得使用者 ID
       chatgpt_reply_msg = ''                 # 設定chatgpt回覆所使用的訊息

       global points  # 引用全局變量
       global start
       global result

       def send_question1():                        # 送出測驗Q1
          if fdb.get('/', f'{user_id}/Q1') != None :        # 每次送出問題前，若原本該userid有該題的分數，就先清空該題資料
            fdb.delete('/', f'{user_id}/Q1')   
          line_bot_api.reply_message(tk, TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://lh3.googleusercontent.com/pw/AJFCJaXyOoZOKIXoQCZylUmw-7N3DTWtkiWhxW0MnzfW86cgGSIqQqtBG8QewcwkpegZsdn_x9e1cY9kjtkhrJ7yssHu9UPFYEuMYToyrDelUcW7cf5whtyw-lat8In-HBrQZTcqKgx3kSH1pfcJ6lKVTZfUDBvHluY2QxrsIVe9BumQvoB5KReJq_gWlYTLIdj85Q5krThAW2JAieEBtljntOar0cCbnpwlhuSEQegu2cJWXSX_YMTIfQCeVVFMf_2gIRwI-vrSg-X8mRKr_2F681uQVJj_1Wzun2cgDP_PoiEeWf9xEQdgKJMEaU8nlKurVEfgFutb1j6b21xR5ADAd3II_hBV7NQIh82skU7Rg1lNTxyQOhcAe1Cy8YFtERNbMkIANAbEUxxXkcnGEiydZZTJnCooZWI6Xz4frF54djz73DcYh3pikz0i5yuoft4geITomLrkfNSd2P3NQioF3wVoBnU3pg5WFuns6Vbx6PdnLX5Iwr2uXMScdg62r1Ppug9nl5sYe47wl04F6ocebrtCOnqKa8GN-YTd2Un5ZmYSEPKkyD6qGbkhTLbGvGM-fTMsHTWlX-XRex6wCmSC3KcwR0kTKaRVZrp2bOSVmV7cmbYChuoa0xXxUWK0fvU_4JlhsvibVpGklyIZC6j-KplPKyieHFOy2ORZy9w0ISjTflD-2q2-EutMEuqhLFsNSfhCtqcRsv3MfIVSTWmKVdamTTwcnDU5Bx4iALNPL_wKnEMAjf17gerQDZZZlK2eY1IM_66vOpCVljfqFR7Ji_76zCTcdLqFUp9yMKpa95Apt95wwHdkJsRVehzOCgIFh-DWjrIkZjn8t9QBwwS1c4D4fiObqVFAqUgikfqqC8YMhWFhiUG8Zn2k_1xofCbsnZvj22WjIc7fXKnvNQyi=w1353-h902-s-no?authuser=0',
              # 女孩背影圖
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
          if fdb.get('/', f'{user_id}/Q2') != None :        # 每次送出問題前，若原本該userid有該題的分數，就先清空該題資料
            fdb.delete('/', f'{user_id}/Q2')        
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://lh3.googleusercontent.com/pw/AIL4fc_JrmEIqZ2d49Q-n0zjvH31Fo4ZNknpYsvtU4U4n9oYEBHEAW7t5P7PIFj1T009F8pYaG24ZeBC5FOaVhEyaA46PGUTQ0XhjCa3d534a5Vv1dknjks2R7OMGRDGIfGpFx94GrSwFQhYpH-ALCXMpqY=w1380-h776-s-no?authuser=0',
              # 乾旱圖
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
          if fdb.get('/', f'{user_id}/Q3') != None :        # 每次送出問題前，若原本該userid有該題的分數，就先清空該題資料
            fdb.delete('/', f'{user_id}/Q3') 
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://lh3.googleusercontent.com/pw/AIL4fc_LfwZtBg1CFm0GXpz5RoSqXUG_LiJFnD8aIZyBJ_WDbxpX__fsuW68r9rGKJ8ofORVCqTPseKl46AyYZtIQ-EGZ07Y-jAIxIVbe5OD1ldg1jZiTVYJQZA9zPdxIIEDuihDMY0S_EQiCWolFY7SDDJDx6LRMiQyFtFo3k6S_lIjAoG7-3jGsDIa39Zu_6cjvLvfceDJaGZ_9V_ZEZGKcytd80z8luFz44ZnZTSew4lWHbDVSRDasoK1qkSM5yfyQdlVap8-fdj17fQs4RJSXBkX-co3IgtkLYns3awzJpoa4QMRDytbfPQ0M0wDO3u-f-hIlby9R5hekWpfNA352yf52P5IIehKby4MCGKaXCVw4lkTks__bc8JdVq7RXaaX2bD6fdLp5C1t7CVUNh2eBT5gy29XdXOfO34uT0SxUYcvTVGbq2_3_fYqz0C32h2v7R-km1osdcm5si7hrEHHSEMVXUWecGrLKI_17JQKG6Of4n0dE265y5XhxFzrbghrkRcQbcbC4TeAn4Hrc1hws4Gox227kmtzKGkfViD92Mpmmw7y4oopxoWzC_t6CWQoSaczdLM1j8QUIibbpeSwz0ikNKuRTOUK__XrYAb82KTMAck55CWqasfmRJtmJCvNeGO3uY9_OOvkbQP05nQB8zEyHFv_1z5fAOeya0pvfkleQ8sOdjvZSCyUbW5E8FJuJsQ7Xup_nVygFbmjdHPcBu7_uqgXKKigjwLgWUxfmngVTWg7UYRReTicJ35wo2BbhWMAb0VEjYlUKxG4WWSCuD0ht4HN8Br6M6VXm-kgUb6Ff_izjWTeLwCGomaFsUWTPK0p6gU37Td6vgq5S22EaQHD_zEWz729L2kd_btZ8fp14NkPIeDCGbk81XDS7jlZrHkKnKnFptOconhvgn-=w507-h902-s-no?authuser=0',
              # 雲朵圖
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
          if fdb.get('/', f'{user_id}/Q4') != None :        # 每次送出問題前，若原本該userid有該題的分數，就先清空該題資料
            fdb.delete('/', f'{user_id}/Q4') 
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://lh3.googleusercontent.com/pw/AIL4fc9wdrBXDCcMYg2ZItGdwaJsFh-GCS8Wtl2XTxuFP_Bg2UWrAXnE8aLJBuRnz2f5FgrUVfJ_xxvdolRpf_f9FybX0YTxvQgIMLwADqUe_tHuRAVPtcG-2l_XVKW80lu6Jbls18ctpAaSGn164y7_QaGDahYkqySd0MeF6vr3SY-AF_fmKclQP91BgvD4DM5RMQoDscQsigZ0OZ7PXSs9gPRLIS2QpQGi-tqr1iEeHGrUHlg3VLjZTZqcq4Z5C9ullo-QGX0Xv6H30mHHMbk6PsT0mvXkNf8aGkWz6uAqMSVNmrqZO0OVlRPc018bqqHkF6FBgFG8l4PVtq_VZhitHFtWyTMNjofqhrwIWTMHLUZIbpuGC64pXgGXxmcqOMSkt9C7r-bdms3cMkujGZXssrD3Flzpjle9OlCVATEXA6LTbJ1ADIgKVcN1U4f_5_D1-D2zWcOLu0nW1hB53estdi9D4ic3inpBKpLx9KJbCzj7egxC3cpXOCutGyhOxacrslAHBB5yQBale3HZH8mdYzT03Hai6gFmEi-9cuf2SB4OvbSOAbl_VPq2RwpLI2L-5PGGydwpqq6SIPj2x_v6u44yQmxgpTQdOgRpTA9TV2Xj043jPxkCVD9XBtZq0Gr7dCE4rnxusA_29NivYLOPD_NoGFIt7nbVZ0ld-b73WrT888dPYpxUoKMsriPLPJ-YkCR9BKA1X2cIRxMp-h9DMhVMGzQ950TwTESZzViIZybEgGlIWjQo8rWsTpWffRzwonx6GtbWxaOtkMbWBpt4z4qxNHA2XmBd1oq2S3-Cc9JhvmcrqxXJ3gftXIF1t4YLiEx8aRlpwODdJ8PuLf98LxGzFHYRFFRthmiYiGqe6Ucmj4KZ9JbnHW1Ttqz7-jxGSssQmtRMhiBDYZFg3TXa=w768-h902-s-no?authuser=0',
              # 辦公室圖
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
          if fdb.get('/', f'{user_id}/Q5') != None :        # 每次送出問題前，若原本該userid有該題的分數，就先清空該題資料
            fdb.delete('/', f'{user_id}/Q5') 
          line_bot_api.reply_message(tk,TemplateSendMessage(
              alt_text='ButtonsTemplate',
              template=ButtonsTemplate(
              thumbnail_image_url='https://lh3.googleusercontent.com/pw/AIL4fc_KN1mXlzTdYoBGIcPR1oypXSNtpyPUtLBNjggKCOopqb4GiLJrDAgNIRd1IRsYytJgjh9oN33_1HNySAvkL7VHYRxTTCZeYjrtR7ktbZzDczxhbNHwO6sq7BxRiiOLZrFL1foJdvc5g6mEzl1lAvJTbDwYQPTOV7QD00E_z2YyM8kiORKU34920q64onSDJOBcgSg0IuUXOFZJWmjJjQKGe69ymmAb-R7Sj6qwJLV3crURVh-brnFsL3s0T4Z4aOuLlGd3qC_b6WF1ocwwgMPi44Ee_Ost-sN4uAumo_OePZLDIOwq03SXcQB0DwX-cAGp2HnD3HvMJ5EimANKinjYl6GABXRfesz9jVNJLln3pSvZGE96LrflTEB7YQe8zRLry_sMmeZZ3pCj-fp91sP-HhLYQVHdWph-MZvM4BHCNMgQrAGcR7z4WC7x2w_BizgPncqMOPN6Mqxl2MNikC-mLt423Z0ijvmn_JcKtGaQe4avbCvlmAKev1-k3v3uMlULVc-oJ2dG6e4me9E_m6EVTv-nYESeGzxXT0WgiuCzWQblAmcV5XVoZ_iD2-0mEIIy1gpnXOtaKfluSBMOQSKpWd0koIejNUs4F3aWX09I_wWzDR9w9gy0cRd_9xWRhUEKRNV6-OoM09nwEp2v0D5_ybPjDK6TZbuNVv6bjbrbEDAaXRNAc8eXS2ZlKriZtw94ejK6PL2OyfrVecRb7FRc6Zg5OCFlMIwrBHWvFMUyQfqNX3C7PPHHWvkgeS4bvjYKiTuW_vDQVHWqDvxGvfk-jOAGT9znh0f5A3HlKWDcRPYs-q2_qfNYFT9yRcssmCsXT0T7m1MZqvitAuNQyFlGBdL5u97G-ukJh-l3VxXw5uKiNuI2TrUc7u9f4nEL3AnKFklU-8jV3NWsI7MY=w1238-h902-s-no?authuser=0',
              # 塞車圖
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
            reset()                                            # 重置測驗
        
            line_bot_api.reply_message(tk,TemplateSendMessage(
               alt_text='ButtonsTemplate',
               template=ButtonsTemplate(
               thumbnail_image_url='https://lh3.googleusercontent.com/pw/AIL4fc_uWI-GQRxixXvXKVQeZKySVhVWPTrTBOsaxybnNrmQkhE3IEv8zhd9ZiDXFEzOiLgauys0CmHFmt_JeqdJccbmgLAypd0l-COjrl9LiYEu8rychjIXdcZXd75hYbOCzqdrkfMzqCHZiGB_0FZNY39Ril5CbqBlaFstwvEAxeQX2jdSOLVO1h-2Dn2-qbwC4C-RKHzj32kBI3fFqmAeIKOyoWHQgz77yBAEoKzi_hGVwDb4VTcaCl05hMvwUtrlFQMYYSHkBrb_8t_Qk7b6PzjibSSQ6teXH-5hgob29GWKk55Wzgqp0FXIcpoSjqF3UA4RiWDUg8iL_KvHFlfCrjhb_atZPuH7h8jbG-WHvVALG3CyTBn_X-AaPHLuHgsq8CEY8xA1QpoQVWJK0iGfkYbxbz54DKzu9XufrD8g6fQv-8aN42c9tpKdKINkGiQ87VVcswcCfS6gfjR51dUESXk9tFbcWfKEGE6CPjrk1WIijt2qFQptqfTDzmO6_tReV8UkiximGrhzP3Ad7smMAEOx5w7F7CAIXwF3qhO_Omdop4pZ2ZM6rPiUgaVwjyZ3vMNOophuEIscyXORGXMzA2Sq9GleZPYqmBBBdOlBEJGN1c-cSZnSw4BuuKuNI4qMHuM0IbXy-eWNaww5kwEcD7kmOkSFI254w-UT_g8kDWHp38aTlvuA273wCCJbvQAoxM6DLrOoIfzPNtvuXS0lrJx8dZIkV111BUt3PjCSZ_BFtqi95z0hh7Xm9X4S3vARLr7s2VbOo1lBMLWRYwi87X_rRea7B6oIMgrH86YyoKRdp7jwE_fsHQ2EoBTlLY34A1-_WQ1lYta4dABmBUbTR1vR-NIWngRTWC8EFwn6xb6PjtFdTTjSc4H2ws5C7AsvfTq8FghhPP_a6rujEyBo=w602-h902-s-no?authuser=0',
               # 黑猩猩思考人生圖
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

       elif msg == '算了，太晚我就不要了':               # 使用者拒絕測驗
          reset()                                      # 重置測驗
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
            "url": "https://lh3.googleusercontent.com/pw/AIL4fc9LuOH8CZGWLRimB0n7-LtERCFqkpo2GsOOSDNKKGtomR1susgkSDuqaT4_oEcPzXgNlgmNw0sqTmFCsiMD9IsYJo18UALydkna_NbZChfGqJt9OmSWQkGPUO6bo5E9VfukKplqQiOcMShp2iw4NXOMoc2Yc_u2Fr326cJwHdbnpnLwKycnrm0hKuvKCEieC2eEWvvL6CK7FJYZp88jA3H4BmSm6L42rAUfsRqMH3DoVpATaVPLA9Ypqm1PlIzjK0KStVSdZEo27Uc-z_yZUFnIHX8PMgGvpj5V2HOqCqy0yb2z5RLAcms5CAYFlDwkn--jwVkjaAqg0dM2Uu9pNQdh0y3TKpLMfjnueDFc6q3U6mU-FwVmP5EYkn6l3IGNilK2z5WBZLJS44XPf42Pdy9YEt8ZAdLY6U3MaqZXazmiPXvfbm5VAexGpGKkSs1eMta0KaJrJOqelzb8GaO_5eyq-rRtKk0Njel6U9RBKBj6n265GunJdy47t9DA1UtWmK0yPp_-edA8mrGs2GtwolgVDBokYCG7kpIIgzGtJ0C5HNyoVtYU58JBgnpIMeHj1jNByI9U-seEXsGhwHn3BZRr56-KUP13AwZaOg4za4frLWj6-qvNSrVQDIFk65uHA5BmOVYVFJulp-lFPczI8BDlI9i_YexnmGepo0ayXWXToCaaj1xqsyYAXNGKCtDqNjCpWwyzspdKwEUKIMgBY1Uc2B6NM4WnOWhd1pvLPbOpmcwT_7wwl1xiFMCSB6lhfoLF3Ag7UZdICY1Jc-uc_8ACLzZNaJ0DqSkfLzaRznGuAaY_SVJWMMoC6O64IH9WayEbf612QFh-qHreOQAJoH1sbY2HQ-zXaEK1fpYHdKpdhJbpkSTqwNu_Uuge6NZX7nJHhlgA2WEKil7gpXyw=w677-h902-s-no?authuser=0",
            #圖
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
}))
          line_bot_api.reply_message(tk, reply_bye_array)

       elif msg == 'Got it! 開始吧！':
          fdb.delete('/', f'{user_id}')                 # 每次開始測驗前，都清空該userid的所有資料
          if start == False:                  # 若原本開始測驗標誌是 False，則改為 True
            start = True
            send_question1()                  # 送出Q1題目
          else:
            send_question1()

       elif msg in q1_choice.values() and start:               # 處理 Q1 答案
          new_q1_choice = {v:k for k, v in q1_choice.items()}   # 把選項字典 value, key 互換
          ans_num = new_q1_choice.get(msg)              # 從新的字典取得答案編號
          this_point = 70 - ord(ans_num) - 1           # 儲存該題答案的分數(經轉換代號而來)
          question_points = {'ans':f'{ans_num}', 'points':f'{this_point}'} #題目與分數組合的字典

          fdb.put('/', f'{user_id}/Q1', question_points)       # 以同步新增，在userid/題號節點，紀錄題目與分數
          snapshot = fdb.get('/', f'{user_id}/Q1')
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:                         # 當開始標記為真
              send_question2()                  # 收到答案後，提出下一題

       elif msg in q2_choice.values():               # 處理 Q2 答案
          new_q2_choice = {v:k for k, v in q2_choice.items()}
          ans_num = new_q2_choice.get(msg)              # 從新的字典取得答案編號
          this_point = 70 - ord(ans_num) - 1           # 儲存該題答案的分數(經轉換代號而來)
          question_points = {'ans':f'{ans_num}', 'points':f'{this_point}'} #題目與分數組合的字典

          fdb.put('/', f'{user_id}/Q2', question_points)       # 以同步新增，在userid/題號節點，紀錄題目與分數
          snapshot = fdb.get('/', f'{user_id}/Q2')
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question3()                   # 收到答案後，提出下一題

       elif msg in q3_choice.values():               # 處理 Q3 答案
          new_q3_choice = {v:k for k, v in q3_choice.items()}
          ans_num = new_q3_choice.get(msg)              # 從新的字典取得答案編號
          this_point = 70 - ord(ans_num) - 1           # 儲存該題答案的分數(經轉換代號而來)
          question_points = {'ans':f'{ans_num}', 'points':f'{this_point}'} #題目與分數組合的字典

          fdb.put('/', f'{user_id}/Q3', question_points)       # 以同步新增，在userid/題號節點，紀錄題目與分數
          snapshot = fdb.get('/', f'{user_id}/Q3')
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question4()                  # 收到答案後，提出下一題

       elif msg in q4_choice.values():               # 處理 Q4 答案
          new_q4_choice = {v:k for k, v in q4_choice.items()}
          ans_num = new_q4_choice.get(msg)              # 從新的字典取得答案編號
          this_point = 70 - ord(ans_num) - 1           # 儲存該題答案的分數(經轉換代號而來)
          question_points = {'ans':f'{ans_num}', 'points':f'{this_point}'} #題目與分數組合的字典

          fdb.put('/', f'{user_id}/Q4', question_points)       # 以同步新增，在userid/題號節點，紀錄題目與分數
          snapshot = fdb.get('/', f'{user_id}/Q4')
          print(snapshot)                      # 輸出資料庫內容檢查
          if start:
             send_question5()                  # 收到答案後，提出下一題

       elif msg in q5_choice.values():               # 處理 Q5 答案
          new_q5_choice = {v:k for k, v in q5_choice.items()}
          ans_num = new_q5_choice.get(msg)              # 從新的字典取得答案編號
          this_point = 70 - ord(ans_num) - 1           # 儲存該題答案的分數(經轉換代號而來)
          question_points = {'ans':f'{ans_num}', 'points':f'{this_point}'} #題目與分數組合的字典

          fdb.put('/', f'{user_id}/Q5', question_points)       # 以同步新增，在userid/題號節點，紀錄題目與分數
          snapshot = fdb.get('/', f'{user_id}/Q5')
          print(snapshot)                      # 輸出資料庫內容檢查
          check = check_points()                   # 檢查每題是否都有分數
          print(check)

          if start and check:                    # 若start與check皆為真
              print(user_id)                   # 將 user_id 印出來檢查
              point_list = []                   # 建立一個存放分數的空串列
              for num in range(1, 6):              # 1~5執行迴圈
                  test_points = fdb.get(f'/{user_id}', f'Q{num}') # 取得user_id/Q 節點下的資料(答案、分數)
                  points_value = int(test_points['points'])    # 把分數字串轉為整數
                  point_list.append(points_value)          # 逐一加入存放分數的串列

              total_points = sum(point_list)           # 加總，得到總分
              result = test_result(total_points)            # 執行測驗結果計算公式

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
            # 箭頭再玩一次圖
            "url": "https://lh3.googleusercontent.com/pw/AJFCJaWmf0m36ORYaqBDVwztC1gis9sTmS4GSzMI9Dx_4C_86ogUNXfFbp8TyCMFueyT-4W-M4f6V9hUGMyC5O12uhBHid8Jsh4F6YAoS_V1RcFQvYCUrPo2itxkYfksvBT1noELbWVLzzv2jwtg4DIovk1H86LfqpDSvzfK4MHn-W9i8B9Yha_WsoHlv2MgawebE6yp5WiFC7p2wknEYCiddzE5Zy9mFSmiBS5-iFH1ws9bzeTeXIhi1AnpmcQUlupH7Cl7Yn089hv9SRadoQ0BMiCVNvm8-Cskks-pGAi1zvdOoO-_fU0LUo4dzWlpYU5AaNMy0eXLzhcW-QHFoJ8N6QbYhhtWzSUw1_VCjebrB1-U37JPrZcoxKak0mXl0tHqb2iXsReWNATypPydTq23KnOg1fFfd5RuT5uh5oCO1v18Sx1MrnMNIB6TEnHEwsRYGV653hxlT71BIFxnhSrZPtvWfLEgZ4471NSVm8YumNk9jp6DGL-LpW1-AIpl32UxV-_A6KM4A4STklOPhlVZHBGMFDpKJTUG8qp29yK_c0XgO6mxIjp3dzgqV5XBxE_novp963eUgZ_j7iSrXd-cR5rMfJmbEmKXYGNCAQigssINqctwHm4FEQqO38NrgL7x6RijTHsya1estKTHGYwTOdwp7PIRgcgTsLXF1Sj6KUpqdJ2So6dDgUGp-Bb6lC1pvLb57y5wlptWPD0S3uKA7HjxtSJ4G3wBrLl0Cg1_9cy3relE3r4O9sFPc6g7DkOi9X74JGyt9GOgzq6lK-OxKe7JQre7wCwf9pr45MbVtzyfjzJHMjdq_9TPvjcOAWtIK7ZXTGTPIM3V0E7bEI55KvkUUblbnCC3RUqH-YXEWIFu-eOgNG8h4gitwLY7rvXo3V5QmDZL2WUJz2pErJPn=w1347-h902-s-no?authuser=0",
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
              reset()                                                   # 執行重置測驗

          else:                             # 反之，如果開始標誌或check為 False
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
            # 
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
            line_bot_api.reply_message(tk, reply_restart_array)        # 回覆重新開始的訊息

       else:
        openai.api_key = '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'  # Ellie的openai key
        chatgpt_response = openai.Completion.create(
            model = 'text-davinci-003',
            prompt = msg,   # 將所有訊息發送給 OpenAI
            max_tokens = 150, # 可使用的 token 數，會影響回話長度
            temperature = 0.5,
            )
        # 接收到使用者訊息後，移除換行符號後，透過chatgpt回覆訊息
        chatgpt_reply_msg = chatgpt_response["choices"][0]["text"].replace('\n','')
        text_message = TextSendMessage(text = chatgpt_reply_msg)
        line_bot_api.reply_message(tk, text_message)

    except Exception as e:
        print('Error:', e)                        # 輸出詳細的錯誤訊息
    return 'OK'