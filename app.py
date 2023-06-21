import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def linebot_test(request):
    try:
        access_token = 'MYoGxJuKZbYgOdIhfiiFbm9BKeFXQAwmgkgbGNENCtAqg1XTmRGdqCzxYMmK+5homRui1cNlrDFEOU3kYKBGgkV3GHwIVwox5oHRbAUFjBuP4DyaNKXklxP0qreeCwIy5TQdKHyY8sGwWmpZAUJ1agdB04t89/1O/w1cDnyilFU='
        secret = '8ef1afb585b2ad36cbaf047e77e6e989'
        body = request.get_data(as_text=True)                # 取得收到的訊息內容
        json_data = json.loads(body)                         # json 格式化訊息內容
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得 LINE 收到的訊息類型
        msg = json_data['events'][0]['message']['text']      # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        
        if type=='text':                                     # 如果是收到文字 text
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            reply = msg
        else:
            reply = '試試看傳文字給我吧！'

        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(request.args)
    return 'OK'                                              # 驗證 Webhook 使用，不能省略