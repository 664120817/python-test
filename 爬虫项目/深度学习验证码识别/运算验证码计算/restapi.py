"""
Run a rest API exposing the yolov5s object detection model
"""
import io
from flask import Flask, request
from torch import load
import torch
from torchvision import transforms
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.MyModels2 import ResNetLstm
import os,re
from PIL import Image
import itertools




def api():
    # 实例化模型
    size = (50, 150)
    model = ResNetLstm(size)
    if os.path.exists('./models/model.pkl'):
        model.load_state_dict(load("./models/model.pkl"))
    my_transforms = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.9238877, 0.9249362, 0.9240683), std=(0.2109205, 0.20895848, 0.2106626))
        ]
    )
    mapping = [i for i in '_0123456789加减乘+-*']
    model.eval()




    with torch.no_grad():
        images = my_transforms(Image.open('yzm.png'))
        images = images.view(1, 3, 50, 150)
        output = model(images)
        # 通过结果计算损失
        output = output.permute(1, 0, 2)  # [2 19 17]
        # print(output)
        for i in range(output.shape[0]):
            output_result = output[i, :, :]
            output_result= output_result.max(-1)[-1]
            output_s = [mapping[i[0]] for i in itertools.groupby(output_result.cpu().numpy()) if i[0] != 0]
            print(output_s)
            num=''.join(output_s)
            g=re.findall(r"(\d+).*?(\d+)",num)
            f = re.findall(r"\d+(.*?)\d+", num)
            # print(f[0].replace('减','-'))
            # print(g[0][0])
            print(f[0])
            if f[0] == "减" or f[0]=="-":
                res= int(g[0][0]) - int(g[0][1])
                print("减：",res,)
                return res
            elif f[0] == "加"or f[0] == "+" :
                res = int(g[0][0]) + int(g[0][1])
                print("加：",res)
                return res
            elif f[0] == "乘" or f[0] == "*":
                res = int(g[0][0]) * int(g[0][1])
                print("乘：",res)
                return res


app = Flask(__name__)

DETECTION_URL = "/img"

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
      return "空"
    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        img.save("yzm.png")
        r = api()
        print(r)
        return str(r)
    return

if __name__ == "__main__":

    app.run(port=88,host='127.0.0.1')
