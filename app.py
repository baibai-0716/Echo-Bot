from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    URIAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import json
import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if text == '探尋鄉道':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "2:2",
        "aspectMode": "cover",
        "url": "https://imgur.com/TZZorzt.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "text": "鄉道茶語",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True
          }
        ],
        "margin": "none"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xxl",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "介紹1",
              "uri": "https://line.me/"
            },
            "margin": "none"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "介紹2",
              "uri": "http://linecorp.com/"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "介紹3",
              "uri": "http://linecorp.com/"
            }
          }
        ],
        "margin": "none",
        "cornerRadius": "none"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "2:2",
        "aspectMode": "cover",
        "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9053_00714-1-1-min.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "text": "居所篇章",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True
          }
        ],
        "margin": "none"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "艾草房",
                  "text": "#艾草房型資訊"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "檀香房",
                  "text": "#檀香房型資訊"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "沉香房",
                  "text": "#沉香房型資訊"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "入住須知",
                  "text": "#入住須知"
                }
              }
            ]
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "2:2",
        "aspectMode": "cover",
        "url": "https://i.imgur.com/cfRzPMZ.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "horizontal",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "text": "歸途引路︱啟程指南",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True
          }
        ],
        "margin": "none"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xxl",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "鄉道地址",
              "text": "#鄉道地址"
            },
            "margin": "none"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "開車必看",
              "uri": "https://www.youtube.com/playlist?list=PLcWAIlKa95I9BWt9o5phqdXyiyFEASMex"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "大眾交通",
              "text": "#大眾交通"
            }
          }
        ],
        "margin": "none"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "2:2",
        "aspectMode": "cover",
        "url": "https://liveyilan.com/wp-content/uploads/2024/08/187979-696x522.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "text": "茶屋漫遊誌",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True
          }
        ],
        "margin": "none"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xxl",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "散步地圖",
              "text": "#散步地圖"
            },
            "margin": "none"
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "宜蘭精選旅程",
              "uri": "https://reurl.cc/zpj9p6"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "管家深度漫遊",
              "text": "#管家深度漫遊"
            }
          }
        ],
        "margin": "none"
      }
    }
  ]
}           
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='詳細說明',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        
