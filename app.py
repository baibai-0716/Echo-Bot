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
        "url": "https://i.imgur.com/TZZorzt.jpeg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "鄉道茶語｜",
            "wrap": True,
            "weight": "bold",
            "size": "xl",
            "gravity": "top",
            "align": "center",
            "contents": [
              {
                "type": "span",
                "text": "鄉道茶屋｜"
              },
              {
                "type": "span",
                "text": "About",
                "size": "lg"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": []
          },
          {
            "type": "text",
            "text": "一條鄉道，連接著田野與茶香；一間茶屋，安放著歲月與風聲。在這裡，時間慢了下來，讓人得以停步，細品茶湯、靜聽自然，尋回心之所安。",
            "wrap": True,
            "size": "xs"
          }
        ]
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
              "label": "初心理念",
              "text": "#初心理念"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "環境一隅",
              "text": "#環境一隅"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "text": "#常見問題",
              "label": "常見問題"
            }
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
        "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9053_00714-1-1-min.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "鄉道茶語｜",
            "wrap": True,
            "weight": "bold",
            "size": "xl",
            "gravity": "top",
            "align": "center",
            "contents": [
              {
                "type": "span",
                "text": "居所篇章｜"
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
            "layout": "baseline",
            "contents": []
          },
          {
            "type": "text",
            "text": "一室一景，靜候遠人。晨曦灑落木窗，微風輕拂茶香，每一間房都是詩意的棲居，安放身心，靜享時光的溫柔流轉。",
            "wrap": True,
            "size": "xs"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
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
              "label": "檀香房",
              "text": "#檀香房型資訊"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "text": "#艾草房型資訊",
              "label": "艾草房"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "text": "#入住須知",
              "label": "入住須知"
            }
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
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "鄉道茶語｜",
            "wrap": True,
            "weight": "bold",
            "size": "xl",
            "gravity": "top",
            "align": "center",
            "contents": [
              {
                "type": "span",
                "text": "啟程指南｜"
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
            "layout": "baseline",
            "contents": []
          },
          {
            "type": "text",
            "text": "曲徑通幽，遠塵歸野。沿著鄉道而來，讓城市的喧囂漸行漸遠，只需一步，便能抵達心之所向",
            "wrap": True,
            "size": "xs"
          }
        ]
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
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "開車必看",
              "text": "#開車必看"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "text": "#大眾交通",
              "label": "大眾交通"
            }
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
        "url": "https://liveyilan.com/wp-content/uploads/2024/08/187979-696x522.jpg"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "鄉道茶語｜",
            "wrap": True,
            "weight": "bold",
            "size": "xl",
            "gravity": "top",
            "align": "center",
            "contents": [
              {
                "type": "span",
                "text": "茶屋漫遊誌｜"
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
            "layout": "baseline",
            "contents": []
          },
          {
            "type": "text",
            "text": "茶屋之外，是寫滿故事的小路。隨興選一條，或通往綠蔭深處，或遇見稻浪翻騰，讓步伐決定風景，讓心境丈量遠方。",
            "wrap": True,
            "size": "xs"
          }
        ]
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
              "label": "鄉道散步地圖",
              "text": "#鄉道散步地圖"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "宜蘭精選景點地圖",
              "uri": "http://reurl.cc/zpj9p6"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "text": "#管家深度漫遊",
              "label": "管家深度漫遊"
            }
          }
        ]
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
elif text == '預約一場漫遊':
            line_flex_json = {
  "type": "bubble",
  "size": "mega",
  "hero": {
    "type": "image",
    "url": "https://static.owlting.com/booking/image/h/9b1e91af-ca77-438d-bc38-5726214b9872/images/mlvUicVMjmILrhHVCszY7voZpLh9W7aWKuiKhPZv.jpeg",
    "size": "full",
    "aspectRatio": "2:2",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://line.me/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "預約一場漫遊",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "預約一場慢旅，為身心留白。輕點指間，茶香與田野已在遠方靜候您的到來。",
            "size": "xs",
            "wrap": True,
            "margin": "none"
          }
        ]
      }
    ],
    "spacing": "sm"
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
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
              "label": "優惠方案說明",
              "text": "#優惠方案說明"
            },
            "margin": "none"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "私訊人工預約",
              "text": "#私訊人工預約-鄉"
            }
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "鄉道線上預約",
              "uri": "https://booking.owlting.com/countryroad?lang=zh_TW&adult=1&child=0&infant=0"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "官方網站",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ]
      }
    ],
    "flex": 0
  }
}
                line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='預約一場漫遊',contents=FlexContainer.from_json(line_flex_str))]
                )
            )

else:
line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )
