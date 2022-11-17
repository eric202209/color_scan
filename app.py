from flask import Flask, request, abort, current_app

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, FollowEvent, UnfollowEvent,
    ImageMessage, ImageSendMessage, QuickReply, QuickReplyButton, CameraAction, CameraRollAction
)

from extentions import db, migrate
from apps.models.user import User
from color import *

# PyCharm的Terminal視窗執行程式碼： ngrok http 5000 --region=ap


app = Flask(__name__)
with app.app_context():
    # within this block, current_app points to app.
    a = current_app
    b = current_app.config['DEBUG']


line_bot_api = LineBotApi('xxxxx')
handler = WebhookHandler('xxxxx')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xxxx:xxxx@xxxxxxxx:xxxx/xxxxxx'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')


db.app = app
db.init_app(app)
migrate.init_app(app, db)


class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'postgresql://xxxx:xxxx@xxxxxxxx:xxxx/xxxxxx'

app.config.from_object(Config)


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


@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """歡迎使用LINE顏色掃描機器人
-這是111年AI資訊工程師班03期機器人的紀錄-
-希望您給予見解與指教-"""
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_msg))


@handler.add(UnfollowEvent)
def handle_follow(event):
    print("Got Unfollow event:" + event.source.user_id)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    if message_text == '@color':
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='拍照或選取照片,做顏色偵測',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=CameraAction(label="開啟相機")
                    ),
                    QuickReplyButton(
                        action=CameraRollAction(label="開啟相簿")
        )])))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    print(event)
    image_url = "https://upload.cc/i1/2022/10/28/MFCBLQ.jpg"
    text_message = "顏色無法辨識！"
    line_bot_api.reply_message(event.reply_token,
                               [ImageSendMessage(preview_image_url=image_url,
                                                 original_content_url=image_url),
                                TextSendMessage(text=text_message)])


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    number = random.randint(0, 100)
    print(event)
    if event.message.type == "image":
        # 取得圖片資料
        image_content = line_bot_api.get_message_content(event.message.id)
        # 定義圖片檔名為訊息ID
        # file_path = f'./{event.message.id}.jpg'
        path = f'./img{str(number)}.jpg'
        # 儲存照片
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
        # 執行圖片預測, 顏色偵測
        pred_result = color_detect(path)
        # 截圖拍照
        color_search = color_grab(path)
        # 上傳照片
        img_name = 'img' + str(number) + '.jpg'
        save_photo = upload_file(img_name)
        # 將預測回傳的訊息包裝成Line的訊息格式
        message = TextSendMessage(pred_result, color_search, save_photo)
        # 將訊息回傳給使用者
        line_bot_api.reply_message(event.reply_token, message)

    # 如果收到的訊息不是圖片
    else:
        # 回傳錯誤訊息給使用者
        message = TextSendMessage("請提供一張圖片!")
        line_bot_api.reply_message(event.reply_token, message)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run()

