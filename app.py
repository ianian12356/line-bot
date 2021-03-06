from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('4ETCNY+UQ96H13R2AdzboRMDyg6OGnbsOBmnZ9LyrSc+qw8Xs69IyRj18vMxKID05nVMLMWNi4odIkUAU49ctl5lNbAmPNLYLdH7dgvljWQSQcf/mQzhaxBOAm6ObLlFhowGR3AFMdg6YYwDmqnRxAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2d011db52b5199d8fa04408feca37a29')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        msg = event.message.text
        s = '很抱歉，聽不太懂你說甚麼?'
        if msg in ['你好', '嗨嗨','哈哈']:
            s = '你好'
        elif '飯' in msg:
            s = '還沒'
        elif msg == '你是誰':
            s = '我是帥哥'
        elif '愛你' in msg:
            sticker_message = StickerSendMessage(
                package_id='1',
                sticker_id='1'
            )

            line_bot_api.reply_message(
                event.reply_token,
                sticker_message )
            return

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= s))


if __name__ == "__main__":
    app.run()