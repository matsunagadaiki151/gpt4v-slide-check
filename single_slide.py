import base64
from openai import OpenAI
from dotenv import load_dotenv

from utils.load_yaml import load_model_name

# タイトルスライドを添削してもらうためのプログラム
# 詳細な添削と100点満点中何点かを添削してもらえる。

# OPENAI_API_KEYを利用するために必要
load_dotenv(".env")

client = OpenAI()

model_name = load_model_name()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


presenter_name = "{PRESENTER_NAME}"


# パワーポイントのタイトルのスライド(手動でpngに変換)
base64_image = encode_image("images/bad_slide.png")

prompt = f"""
以下はAI勉強会で発表する予定のスライドのタイトルです。このタイトルスライドのデザインを添削してください。
なお、{presenter_name}は発表者の名前です。
また、このスライドの総合点を100点満点でつけてください。
"""

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        # base64の指定方法
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high",
                    },
                },
            ],
        }
    ],
    temperature=0,
    # 多めにしておくといいかも
    max_tokens=1000,
)

message = response.choices[0].message.content
print(message)

with open("message.txt", "w", encoding="utf8") as f:
    f.write(message)
