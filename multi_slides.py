import base64
from openai import OpenAI
from dotenv import load_dotenv
import glob

from utils.load_yaml import load_model_name

# スライド一式を添削してもらうためのプログラム
# 詳細な添削と100点満点中何点かを添削してもらえる。

load_dotenv(".env")

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
model_name = load_model_name()


prompt = """
以下はAI勉強会で発表する予定のスライドです。このスライド全体のデザインを添削してください。
また、このスライドの総合点を100点満点でつけてください。
書かれている内容の添削は不要です。
"""

# スライド一覧
slides = sorted(glob.glob("images/bad_slides/bad_slide*.png"))

# contentプロパティを動的に生成する。
contents = [{"type": "text", "text": prompt}]
for slide in slides:
    base64_image = encode_image(slide)
    image_prop = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{base64_image}",
            "detail": "low",
        },
    }
    contents.append(image_prop)

response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": contents}],
    temperature=0,
    # 多めにしておくといいかも
    max_tokens=2000,
)

message = response.choices[0].message.content
print(message)

with open("message.txt", "w", encoding="utf8") as f:
    f.write(message)
