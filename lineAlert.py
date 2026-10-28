from linebot import LineBotApi
from linebot.models import TextSendMessage
from project import config
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient, ImageCarouselTemplate,TemplateMessage,URIAction, ImageCarouselColumn, DatetimePickerAction
from linebot.v3.messaging.models.multicast_request import MulticastRequest
from linebot.v3.messaging.models import TextMessage, PushMessageRequest, ImageMessage
from linebot.v3.messaging.rest import ApiException
import time
import os
Channel_secret = config.Channel_secret
Channel_access_token = config.Channel_access_token
basic_id = config.basic_id
user_ids = [config.B_id, config.C_id, config.L_id]

configuration = Configuration(
    host = "https://api.line.me"
)
configuration = Configuration(
    access_token = Channel_access_token
)

# กำหนด path ที่คุณต้องการ
path = r'D:\forecast\forecast\public\outputImg'  # เปลี่ยน path ตามที่คุณต้องการ
thumbnails_path = r'D:\forecast\forecast\public\outputImg\thumbnails'
url = "https://myblog-8a9d9.web.app/outputImg/"
thumbnails_url = "https://myblog-8a9d9.web.app/outputImg/thumbnails/"
def rainy(message='มีฝน'):
    #time_string = time.strftime('%H:%M') + " UTC"
    # ใช้ os.listdir() เพื่อดึงรายการไฟล์ใน path ที่กำหนด
    files = os.listdir(path)
    # กรองเฉพาะไฟล์ที่มีนามสกุล .jpg
    jpg_files = [file for file in files if file.lower().endswith('.jpg')]
    jpg_files = sorted(jpg_files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
    # ใช้ os.listdir() เพื่อดึงรายการไฟล์ใน thumbnails_path ที่กำหนด
    thumbnails_files = os.listdir(thumbnails_path)
    jpg_thumbnails_files = [file for file in thumbnails_files if file.lower().endswith('.jpg')]
    jpg_thumbnails_files = sorted(jpg_thumbnails_files, key=lambda f: os.path.getmtime(os.path.join(thumbnails_path, f)))
    image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-7])
    alt_text_name = "RTR " + jpg_files[-1][0:6] + " UTC"
    first_label = "{}".format(jpg_files[-1][0:6])+"+0"
    second_label = "{}".format(jpg_files[-1][0:6])+"+15"
    third_label = "{}".format(jpg_files[-1][0:6])+"+30"
    fourth_label = "{}".format(jpg_files[-1][0:6])+"+45"
    fifth_label = "{}".format(jpg_files[-1][0:6])+"+60"
    with ApiClient(configuration) as api_client:
        messaging_api = MessagingApi(api_client)
        image_carousel_template = ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-7]),
                            action=URIAction(
                                label=first_label,uri = url + "{}".format(jpg_files[-7])
                            ),
                        ),
                        ImageCarouselColumn(
                             image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-6]),
                             action=URIAction(
                                label=second_label,uri = url + "{}".format(jpg_files[-6])
                             ),
                        ),
                        ImageCarouselColumn(
                             image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-5]),
                             action=URIAction(
                                label=third_label,uri = url + "{}".format(jpg_files[-5])
                             ),
                        ),
                        ImageCarouselColumn(
                             image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-4]),
                             action=URIAction(
                                label=fourth_label,uri = url + "{}".format(jpg_files[-4])
                             ),
                        ),
                        ImageCarouselColumn(
                             image_url=thumbnails_url + "{}".format(jpg_thumbnails_files[-3]),
                             action=URIAction(
                                label=fifth_label,uri = url + "{}".format(jpg_files[-3])
                             ),
                        ),
                    ]
                )
        template_message = TemplateMessage(
                        alt_text = '{}'.format(alt_text_name) ,
                        template = image_carousel_template
                )
        messaging_api.multicast(
            MulticastRequest(
                to = user_ids,
                messages = [TextMessage(text="https://myblog-8a9d9.web.app"),
                             template_message,
                             TextMessage(text=f'{message}')]
            )
        )

# messages = [TextMessage(text='มีฝนบริเวณสนามบิน'),
#             ImageMessage(original_content_url='https://weather.tmd.go.th/srt/srt240_latest.jpg',
#                             preview_image_url='https://weather.tmd.go.th/srt/srt240_latest.jpg')
#             ]
# def rainy():
#     with ApiClient(configuration) as api_client:
#         messaging_api = MessagingApi(api_client)

#         for user_id in user_ids:
#             messaging_api.push_message(
#                 PushMessageRequest(
#                 to = user_id,
#                 messages=[TextMessage(text='มีฝนตกบริเวณสนามบิน')]
#                 )
#             )
#             time.sleep(0.5)