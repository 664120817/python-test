from torch import save, load
import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from torch import optim
from tqdm import tqdm
import os
import numpy as np
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.MyModels2 import ResNetLstm
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.MyDataset2 import Letter2Dataset
import itertools


mapping = [i for i in '_0123456789加减乘+-*']
def test():
    # 实例化模型
    model = ResNetLstm((50, 150))
    optimizer = optim.Adam(model.parameters())
    batch_size = 16
    # 加载已经训练好的模型和优化器继续进行训练
    if os.path.exists('./models/model.pkl'):
        model.load_state_dict(load("./models/model.pkl"))
        optimizer.load_state_dict(load("./models/optimizer.pkl"))

    my_transforms = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.9238877, 0.9249362, 0.9240683), std=(0.2109205, 0.20895848, 0.2106626))
        ]
    )
    mnist_train = Letter2Dataset(root="./test", transform=my_transforms)
    success = 0
    total = 0
    dataloader = DataLoader(mnist_train, batch_size=batch_size, shuffle=True, drop_last=True)
    dataloader = tqdm(dataloader, total=len(dataloader))
    model.eval()
    with torch.no_grad():
        for images, labels, _ in dataloader:
            output = model(images)
            # 通过结果计算损失
            output = output.permute(1, 0, 2)  # [2 19 17]
            for i in range(output.shape[0]):
                output_result = output[i, :, :]
                output_result = output_result.max(-1)[-1]
                print(output_result)
                labels_s = [mapping[i] for i in labels[i].cpu().numpy() if mapping[i] != '_']
                output_s = [mapping[i[0]] for i in itertools.groupby(output_result.cpu().numpy()) if i[0] != 0]
                if labels_s == output_s:
                    print(labels_s,output_s)
                    success += 1
                total += 1

    return success/total

test()