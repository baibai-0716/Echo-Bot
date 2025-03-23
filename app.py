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
        "url": "https://imgur.com/TZZorzt.jpeg",
        "position": "relative",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "contents": [
              {
                "type": "span",
                "text": "鄉道茶語｜",
                "weight": "bold",
                "size": "xl"
              },
              {
                "type": "span",
                "text": "About",
                "style": "normal",
                "weight": "bold",
                "size": "lg"
              }
            ],
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "一條鄉道，連接著田野與茶香；一間茶屋，安放著歲月與風聲。在這裡，時間慢了下來，讓人得以停步，細品茶湯、靜聽自然，尋回心之所安。",
                "size": "sm",
                "margin": "sm",
                "gravity": "center",
                "wrap": True
              }
            ]
          }
        ],
        "margin": "none",
        "maxHeight": "200px"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "xl",
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
        "cornerRadius": "none",
        "justifyContent": "center",
        "alignItems": "center"
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
            "text": "居所篇章｜About Rooms",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True,
            "contents": [
              {
                "type": "span",
                "text": "居所篇章｜",
                "size": "xl"
              },
              {
                "type": "span",
                "text": "Room Types",
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "一室一景，靜候遠人。晨曦灑落木窗，微風輕拂茶香，每一間房都是詩意的棲居，安放身心，靜享時光的溫柔流轉。",
                "size": "sm",
                "margin": "sm",
                "gravity": "center",
                "wrap": True
              }
            ]
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
            ],
            "alignItems": "center"
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
        "layout": "vertical",
        "spacing": "xs",
        "contents": [
          {
            "type": "text",
            "text": "啟程指南︱Map",
            "weight": "bold",
            "size": "xl",
            "position": "relative",
            "align": "center",
            "wrap": True,
            "contents": [
              {
                "type": "span",
                "text": "啟程指南｜",
                "size": "xl"
              },
              {
                "type": "span",
                "text": "Traffic Guidance",
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "曲徑通幽，遠塵歸野。沿著鄉道而來，讓城市的喧囂漸行漸遠，只需一步，便能抵達心之所向。",
                "size": "sm",
                "margin": "sm",
                "gravity": "center",
                "wrap": True
              }
            ]
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
            "wrap": True,
            "contents": [
              {
                "type": "span",
                "text": "茶屋漫遊誌｜",
                "size": "xl"
              },
              {
                "type": "span",
                "text": "Travel Map",
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "茶屋之外，是寫滿故事的小路。隨興選一條，或通往綠蔭深處，或遇見稻浪翻騰，讓步伐決定風景，讓心境丈量遠方。",
                "size": "sm",
                "margin": "sm",
                "gravity": "center",
                "wrap": True
              }
            ]
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
                    messages=[FlexMessage(alt_text='探尋鄉道',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        
