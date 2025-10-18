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
    TextMessageContent,
    Postbackevent
)
import json
import os
import threading
import time

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
    timers = {}

@line_handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    user_id = event.source.user_id

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # ✅ 當按下「開始泡湯」時
        if data == "action=start_bathing":
            # 立即回覆確認訊息
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="已開始計時，半小時後會提醒您回報安全狀況💧")]
                )
            )

            # 開始計時（用 Thread 避免阻塞）
            def remind_later():
                time.sleep(30 * 60)
                line_bot_api.push_message(
                    ReplyMessageRequest(
                        to=user_id,
                        messages=[TextMessage(text="嗨～已經過半小時囉，請回報安全狀況💧")]
                    )
                )
                time.sleep(30 * 60)
                line_bot_api.push_message(
                    ReplyMessageRequest(
                        to=user_id,
                        messages=[TextMessage(text="已經過 1 小時囉～請再次確認安全狀況💧")]
                    )
                )

            t = threading.Thread(target=remind_later)
            t.start()
            timers[user_id] = t


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
            "text": "曲徑通幽，遠塵歸野。沿著鄉道而來，讓城市的喧囂漸行漸遠，只需一步，便能抵達心之所向。",
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
              "type": "uri",
              "label": "開車必看",
              "uri": "https://www.youtube.com/playlist?list=PLcWAIlKa95I9BWt9o5phqdXyiyFEASMex"
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
        elif text =='預約一場慢旅':
            line_flex_json = {
  "type": "bubble",
  "size": "mega",
  "hero": {
    "type": "image",
    "url": "https://liveyilan.com/wp-content/uploads/2025/04/進入官網-2.png",
    "size": "full",
    "aspectRatio": "2:2",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://liveyilan.com/countryroad/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "預約一場慢旅",
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
              "label": "包棟方案說明",
              "text": "#包棟方案說明"
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
              "type": "message",
              "label": "私訊人工預約",
              "text": "#私訊人工預約-鄉"
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
                    messages=[FlexMessage(alt_text='預約一場慢旅',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text =='分館拾光':
            line_flex_json = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/w0U89mPqW7ukKc0m6W4nK3kAulIqpwHUo01sGChJ.jpeg",
    "size": "full",
    "aspectRatio": "2:2",
    "aspectMode": "cover"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "分館拾光",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "松風輕語，溫泉映月，一隅寧靜，拾起光陰的柔和溫度。置身於此，便是與自然共鳴的美好時刻。",
            "size": "sm",
            "margin": "none",
            "wrap": True
          }
        ]
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
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "空間介紹",
          "text": "#空間介紹"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "溫泉湯屋",
          "text": "#溫泉湯屋"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "私訊人工預約",
          "text": "#私訊人工預約-松"
        }
      },
      {
        "type": "separator"
      },
      {
        "type": "button",
        "style": "primary",
        "color": "#00BFA5",
        "action": {
          "type": "postback",
          "label": "✅ 開始泡湯",
          "data": "action=start_bathing"
        }
      }
    ],
    "flex": 0
  }
}
    line_flex_str = json.dumps(line_flex_json)
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[FlexMessage(alt_text='分館拾光', contents=FlexContainer.from_json(line_flex_str))]
        )
    )
        elif text =='#艾草房型資訊':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/aiaKJf1.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://i.imgur.com/aiaKJf1.jpeg"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#和式乳膠標準床墊",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "2樓",
                "align": "center",
                "weight": "bold",
                "size": "md",
                "color": "#ffffff"
              }
            ],
            "position": "absolute",
            "width": "60px",
            "height": "25px",
            "backgroundColor": "#9A6852",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "offsetStart": "18px"
          }
        ],
        "paddingAll": "0px"
      },
      "size": "giga"
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9806_00087-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#雙人彈簧床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "align": "center",
                "weight": "bold",
                "size": "md",
                "color": "#ffffff"
              }
            ],
            "position": "absolute",
            "width": "60px",
            "height": "25px",
            "backgroundColor": "#9A6852",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "offsetStart": "18px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9194_00834-1-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#和式乳膠標準床墊",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "5樓",
                "align": "center",
                "weight": "bold",
                "size": "md",
                "color": "#ffffff"
              }
            ],
            "position": "absolute",
            "width": "60px",
            "height": "25px",
            "backgroundColor": "#9A6852",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "offsetStart": "18px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9254_00892-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#半戶外觀景陽台",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
{
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/Np0D3x9.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#免治馬桶　#乾濕分離",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/Dyvi9x7.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "艾草房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#淋浴間(無浴缸)",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='艾草房型資訊',contents=FlexContainer.from_json(line_flex_str))]
                )
            )         
        elif text =='#檀香房型資訊':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/FoRSlfc.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "檀香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#高磅數加大雙人彈簧床　#室內面山觀景窗　#可加1床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "2樓",
                "size": "md",
                "color": "#ffffff",
                "weight": "bold",
                "align": "center"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#9A6852",
            "offsetStart": "18px",
            "height": "25px",
            "width": "60px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9053_00714-1-1-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "檀香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#高磅數加大雙人彈簧床　#室內面山觀景窗　#可加1床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "6樓",
                "size": "md",
                "color": "#ffffff",
                "weight": "bold",
                "align": "center"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#9A6852",
            "offsetStart": "18px",
            "height": "25px",
            "width": "60px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/nAwaq5A.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "檀香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#乾濕分離　#免治馬桶",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/CXtGHOL.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "檀香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#私人浴缸　#對外窗",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='檀香房型資訊',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text =='#沉香房型資訊':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/BX1Ukcy.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "沉香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#高磅數加大雙人彈簧床　#室內面山觀景窗　#可加1-2床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "size": "md",
                "color": "#ffffff",
                "weight": "bold",
                "align": "center"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#9A6852",
            "offsetStart": "18px",
            "height": "25px",
            "width": "60px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://imgur.com/FbFf0jv.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "沉香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#高磅數加大雙人彈簧床　#室內面山觀景窗　#可加1-2床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "5樓",
                "size": "md",
                "color": "#ffffff",
                "weight": "bold",
                "align": "center"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#9A6852",
            "offsetStart": "18px",
            "height": "25px",
            "width": "60px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9180_00824-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "沉香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#半戶外觀景陽台",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/nAwaq5A.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "沉香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#乾濕分離　#免治馬桶",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://i.imgur.com/CXtGHOL.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "沉香房",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#私人浴缸　#對外窗",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='沉香房型資訊',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text =='#環境一隅':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9956_00220-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9875_00146-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9902_00171-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC9848_00126-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC0668_00603-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://liveyilan.com/wp-content/uploads/2016/02/DSC0580_00539-min.jpg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='環境一隅',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text =='#空間介紹':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/wi4OzLIj2sG7XsGm61AWvDeKmJzdGDaE5w5q4YoT.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "星滿意竹",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#樓中樓設計　#可加1-2床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "4樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/3hxp4sUNk45K1omLdsMMasS48SZWDquh727g7OZM.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "星滿意竹",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#懶骨頭沙發區",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "4樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/w0U89mPqW7ukKc0m6W4nK3kAulIqpwHUo01sGChJ.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "星滿意竹",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#半露天泡湯池",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "4樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/VuUG95980XtFefVLx9GqSspvakxV5VZvQkEkNTVp.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "有View最美",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#塌塌米觀景區",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/t2t5SdOoAI4xkufXNPYGXKxcyNGQnbBSwgQ5Iay9.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "有View最美",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#一般雙人浴池　#對外窗",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/Ef0yamZ8CE3v8yF2Dnaid7u0Hud1VG76Y9yHxclJ.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "日式簡約",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#室內沙發區",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/AGos5YRaqBlYUr6iDOZ6nYS6keXQXihntYZHTrXe.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "日式簡約",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#下崁式浴池　#泡起來較深",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "3樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/A8TwoY357ZoukAfOIy74xZ9R5sdWWsU9S2BKCTIW.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "悠悠時光",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#四人房　#兩張標準雙人床",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "2樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://static.owlting.com/booking/image/h/d1afba1c-30f3-423c-9b65-a6922af450fe/images/4x1bKa0P87CVPKkyMNmNbArrnXsmRoUcNVigu7GE.jpeg",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:2",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "悠悠時光",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "#一般雙人浴池　#對外窗",
                    "color": "#ebebeb",
                    "size": "sm",
                    "flex": 0,
                    "wrap": True
                  }
                ],
                "spacing": "lg"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px",
            "paddingTop": "18px",
            "background": {
              "type": "linearGradient",
              "angle": "0deg",
              "startColor": "#00000099",
              "endColor": "#00000000"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "2樓",
                "color": "#ffffff",
                "align": "center",
                "size": "md"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#95CACA",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='空間介紹',contents=FlexContainer.from_json(line_flex_str))]
                )
            )
        elif text =='#包棟方案說明':
            line_flex_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://lihi2.com/m1tUu",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://lihi2.com/m1tUu"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "👉點我看包棟溫馨小提醒",
              "text": "#包棟溫馨小提醒"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "👉點我看官網資訊",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://lihi2.com/hudqo",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top",
            "action": {
              "type": "uri",
              "label": "action",
              "uri": "https://lihi2.com/hudqo"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "👉點我看包棟溫馨小提醒",
              "text": "#包棟溫馨小提醒"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "👉點我看官網資訊",
              "uri": "https://liveyilan.com/countryroad/"
            }
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text='包棟方案說明',contents=FlexContainer.from_json(line_flex_str))]
                )
            )

