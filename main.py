from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent,
    FlexSendMessage, BubbleContainer, BoxComponent,
    TextComponent, ButtonComponent, URIAction, PostbackAction,
    ImageComponent, SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

# 請替換為您的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('ZpEfYZFM6KPt5Vk2XNAysHD7FS3hxvaXoYJ8A80kbr6M5a5FTRIi8Dkkmrl6TVuwa6WJc2qAzn9JT7UrN4Bg1L3E9w/J+R83EFARAmkvoT6fUnV8uhvNDua//LTKph/8z2rBfX3GxWbLXTHHqUUHogdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c3687fcf360b9d8689b39ea48409ffa8')

def create_welcome_flex_message():
    """建立歡迎訊息的 Flex Message 含按鈕"""
    bubble = BubbleContainer(
        hero=ImageComponent(
            url="https://example.com/smile3d_logo.jpg",
            size="full",
            aspect_ratio="20:13",
            aspect_mode="cover"
        ),
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(
                    text="歡迎來到 smile3D 影像真人公仔",
                    weight="bold",
                    size="xl",
                    color="#1DB446",
                    wrap=True
                ),
                TextComponent(
                    text="台中店即將於9月中旬盛大開幕",
                    size="md",
                    color="#666666",
                    margin="md",
                    wrap=True
                ),
                SeparatorComponent(margin="lg"),
                TextComponent(
                    text="我們的服務項目",
                    weight="bold",
                    size="lg",
                    margin="lg"
                ),
                TextComponent(
                    text="3D打印紀念品 (現場拍攝 10-30分鐘)",
                    size="sm",
                    color="#333333",
                    margin="sm",
                    wrap=True
                ),
                TextComponent(
                    text="寵物鑰匙圈 (一張照片即可完成)",
                    size="sm",
                    color="#333333",
                    margin="sm",
                    wrap=True
                ),
                TextComponent(
                    text="已故往生紀念品 (一張照片30天完成)",
                    size="sm",
                    color="#333333",
                    margin="sm",
                    wrap=True
                ),
                TextComponent(
                    text="樹葉雕刻紀念品 (照片雷射雕刻)",
                    size="sm",
                    color="#333333",
                    margin="sm",
                    wrap=True
                )
            ]
        ),
        footer=BoxComponent(
            layout="vertical",
            spacing="sm",
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=PostbackAction(
                        label="拍攝須知",
                        data="action=filming_guide"
                    )
                ),
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=PostbackAction(
                        label="價格資訊",
                        data="action=pricing_menu"
                    )
                ),
                ButtonComponent(
                    style="secondary",
                    height="sm",
                    action=PostbackAction(
                        label="合作洽詢",
                        data="action=partnership"
                    )
                ),
                ButtonComponent(
                    style="link",
                    height="sm",
                    action=URIAction(
                        label="追蹤 Instagram",
                        uri="https://www.instagram.com/smile3d2025?igsh=MXE4NHdoa2piczc2dQ%3D%3D&utm_source=qr"
                    )
                )
            ]
        )
    )
    
    return FlexSendMessage(alt_text="歡迎來到 smile3D!", contents=bubble)

def create_filming_guide_flex():
    """建立拍攝須知的 Flex Message"""
    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(
                    text="拍攝須知",
                    weight="bold",
                    size="xl",
                    color="#1DB446"
                ),
                SeparatorComponent(margin="lg"),
                TextComponent(
                    text="服裝穿搭建議",
                    weight="bold",
                    size="lg",
                    margin="lg"
                ),
                TextComponent(
                    text="• 淺色服裝優先，避免過深色彩\n• 避免細高跟鞋與懸空袖擺\n• 避免全黑服飾\n• 避免透明或半透明衣物\n• 避免亮片、反光材質\n• 避免過細、懸空配件",
                    size="sm",
                    color="#333333",
                    margin="md",
                    wrap=True
                )
            ]
        ),
        footer=BoxComponent(
            layout="vertical",
            spacing="sm",
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=PostbackAction(
                        label="髮型妝容建議",
                        data="action=makeup_guide"
                    )
                ),
                ButtonComponent(
                    style="secondary",
                    height="sm",
                    action=PostbackAction(
                        label="寵物拍攝須知",
                        data="action=pet_guide"
                    )
                ),
                ButtonComponent(
                    style="link",
                    height="sm",
                    action=PostbackAction(
                        label="返回主選單",
                        data="action=main_menu"
                    )
                )
            ]
        )
    )
    
    return FlexSendMessage(alt_text="拍攝須知", contents=bubble)

def get_makeup_guide_message():
    """髮型妝容建議訊息"""
    return TextSendMessage(
        text="髮型妝容建議\n\n為讓五官與臉部特徵清晰呈現，拍攝時請注意：\n\n• 避免瀏海遮額或碎髮\n• 避免煙燻妝及過長假睫毛\n• 避免懸空辮子或馬尾\n• 眉毛與唇色適度加強\n\n建議自然妝容，避免過度修飾，讓真實的美感呈現在作品中。"
    )

def get_pet_guide_message():
    """寵物拍攝須知訊息"""
    return TextSendMessage(
        text="寵物拍攝須知\n\n拍攝前請事先告知需一同拍攝的寵物，門市人員將依寵物類型與體型提供專用與建議。\n\n• 建議攜帶能吸引寵物注意的道具或零食\n• 提高拍攝穩定度\n• 若拍攝寵物數量較多，請至少安排一位陪同人員協助現場控制\n\n我們會盡力協助您完成最佳的拍攝效果。"
    )

def create_pricing_menu_flex():
    """建立價格選單的 Flex Message"""
    bubble = BubbleContainer(
        body=BoxComponent(
            layout="vertical",
            contents=[
                TextComponent(
                    text="價目表",
                    weight="bold",
                    size="xl",
                    color="#1DB446",
                    align="center"
                ),
                SeparatorComponent(margin="lg"),
                TextComponent(
                    text="請選擇您想了解的價格資訊：",
                    size="md",
                    margin="lg",
                    wrap=True
                )
            ]
        ),
        footer=BoxComponent(
            layout="vertical",
            spacing="sm",
            contents=[
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=PostbackAction(
                        label="人物公仔價格",
                        data="action=human_pricing"
                    )
                ),
                ButtonComponent(
                    style="primary",
                    height="sm",
                    action=PostbackAction(
                        label="寵物公仔價格",
                        data="action=pet_pricing"
                    )
                ),
                ButtonComponent(
                    style="secondary",
                    height="sm",
                    action=PostbackAction(
                        label="加購項目價格",
                        data="action=addon_pricing"
                    )
                ),
                ButtonComponent(
                    style="link",
                    height="sm",
                    action=PostbackAction(
                        label="返回主選單",
                        data="action=main_menu"
                    )
                )
            ]
        )
    )
    
    return FlexSendMessage(alt_text="價目表選單", contents=bubble)

def get_human_pricing_message():
    """人物公仔價格訊息"""
    return TextSendMessage(
        text="人物公仔價格表\n\n【站立姿勢】\n單人：\n9cm - NT 1,799\n12cm - NT 2,499\n15cm - NT 4,399\n18cm - NT 8,799\n\n多人/位：\n9cm - NT 1,600\n12cm - NT 2,200\n15cm - NT 4,150\n18cm - NT 8,499\n\n【蹲姿/半蹲】單人：\n9cm - NT 2,399\n12cm - NT 4,399\n15cm - NT 7,599\n18cm - NT 12,999\n\n【全蹲/坐地】單人：\n9cm - NT 5,899\n12cm - NT 12,999\n15cm - NT 20,999\n18cm - NT 36,999"
    )

def get_pet_pricing_message():
    """寵物公仔價格訊息"""
    return TextSendMessage(
        text="寵物單獨拍攝 - 隨意度公仔製作\n\n【坐地姿勢】\n小型寵物：\n7cm - NT 3,799\n9cm - NT 5,599\n\n中大型寵物：\n7cm - NT 2,699\n9cm - NT 4,299\n\n【四腳站立姿勢】\n小型寵物：\n7cm - NT 4,499\n9cm - NT 6,299\n\n中大型寵物：\n7cm - NT 3,599\n9cm - NT 5,399\n\n【趴地姿勢】\n小型寵物：\n7cm - NT 8,599\n9cm - NT 11,999\n\n中大型寵物：\n7cm - NT 11,999\n9cm - NT 15,399"
    )

def get_addon_pricing_message():
    """加購項目價格訊息"""
    return TextSendMessage(
        text="加購項目價格表\n\n【附加寵物拍攝 - 隨人等比例縮放】\n小型犬加購：\n9cm - NT 800\n12cm - NT 1,050\n15cm - NT 1,200\n18cm - NT 1,450\n\n中大型犬加購：\n9cm - NT 1,100\n12cm - NT 1,600\n15cm - NT 2,100\n18cm - NT 2,500\n\n【附加服飾、道具拍攝】\n小型道具加購：\n9cm - NT 200\n12cm - NT 250\n15cm - NT 280\n18cm - NT 310\n\n中大型道具加購：\n9cm - NT 650\n12cm - NT 1,100\n15cm - NT 1,500\n18cm - NT 1,900"
    )

def get_partnership_message():
    """合作洽詢訊息"""
    return TextSendMessage(
        text="合作機會\n\n尋找合作夥伴中\n時薪1000元 + 銷售分潤15%\n\n合作內容：\n• 自由創作風格\n• 提供專屬下單連結\n• 彈性工作時間\n• 豐厚收入機會\n\n歡迎洽詢：闕濬權\nLine ID: chazifan1991\n\n讓我們一起創造美好回憶，同時獲得理想收入！"
    )

def get_color_tech_message():
    """顏色還原與技術限制說明"""
    return TextSendMessage(
        text="顏色還原與技術限制說明\n\n由於3D列印色彩表現受限，部分色系呈現可能略有誤差，屬正常現象：\n\n• 深色：可能偏黑，細節表現力較弱\n• 深褐色：成品可能略偏紅\n• 白色：可能偏粉紅\n• 同批/不同批次製作的公仔間也可能存在些許色差\n\n眼睛部位將額外進行人工修飾（如加強眼神光），增添神韻。\n\n鬈髮髮型或寵物長毛無法100%還原空氣感，建議適當穿衣增添立體感與色彩層次。"
    )

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理用戶訊息"""
    user_message = event.message.text.lower()
    
    # 建立快速回覆選項
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=PostbackAction(label="拍攝須知", data="action=filming_guide")),
        QuickReplyButton(action=PostbackAction(label="價格資訊", data="action=pricing_menu")),
        QuickReplyButton(action=PostbackAction(label="合作洽詢", data="action=partnership")),
        QuickReplyButton(action=PostbackAction(label="主選單", data="action=main_menu"))
    ])
    
    # 問候語或開始關鍵字
    greeting_keywords = ['hi', 'hello', '你好', '哈囉', '開始', 'start', '歡迎', '主選單']
    service_keywords = ['服務', '項目']
    
    if any(keyword in user_message for keyword in greeting_keywords):
        reply_message = create_welcome_flex_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif any(keyword in user_message for keyword in service_keywords):
        service_text = "smile3D 服務項目詳細介紹：\n\n3D打印紀念品\n• 需現場拍攝\n• 製作時間：10-30分鐘\n• 立體真人公仔，栩栩如生\n\n寵物鑰匙圈\n• 只需一張清晰照片\n• 讓愛寵陪伴您身邊\n\n已故往生紀念品\n• 半身或全身皆可製作\n• 只需一張照片\n• 製作時間約30天\n• 永恆懷念的最佳方式\n\n樹葉雕刻紀念品\n• 精密雷射雕刻技術\n• 只需一張照片\n• 天然樹葉材質"
        
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=service_text, quick_reply=quick_reply)
        )
    else:
        # 一般回覆
        reply_text = "感謝您的訊息\n\n請選擇您想了解的資訊：\n• 拍攝須知\n• 價格資訊\n• 合作洽詢\n\n或直接點選下方快速選項"
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text, quick_reply=quick_reply)
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    """處理按鈕點擊事件"""
    data = event.postback.data
    
    if data == "action=filming_guide":
        reply_message = create_filming_guide_flex()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=makeup_guide":
        reply_message = get_makeup_guide_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=pet_guide":
        reply_message = get_pet_guide_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=pricing_menu":
        reply_message = create_pricing_menu_flex()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=human_pricing":
        reply_message = get_human_pricing_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=pet_pricing":
        reply_message = get_pet_pricing_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=addon_pricing":
        reply_message = get_addon_pricing_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=pricing_info":
        reply_message = get_pricing_info_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=partnership":
        reply_message = get_partnership_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=color_tech":
        reply_message = get_color_tech_message()
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    elif data == "action=main_menu":
        reply_message = create_welcome_flex_message()
        line_bot_api.reply_message(event.reply_token, reply_message)

# 新用戶加入時的歡迎訊息
from linebot.models import FollowEvent

@handler.add(FollowEvent)
def handle_follow(event):
    """當用戶加入好友時發送歡迎訊息"""
    welcome_message = create_welcome_flex_message()
    line_bot_api.reply_message(event.reply_token, welcome_message)

if __name__ == "__main__":
    app.run(debug=True, port=5011)