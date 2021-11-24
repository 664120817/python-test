from torch import save, load
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.test_p2 import test
from torchvision import transforms
from torch.utils.data import DataLoader
from torch import nn
from torch import optim
from tqdm import tqdm
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.MyModels2 import ResNetLstm
from 我爱自学.猿人学课程作业.sec9.Image_Text.letter2.MyDataset2 import Letter2Dataset
import os
import numpy as np
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# 实例化模型
size = (50, 150)
model = ResNetLstm(size)
model = model.to(device)
optimizer = optim.Adam(model.parameters())
batch_size = 16
# 加载已经训练好的模型和优化器继续进行训练
if os.path.exists('./models/model.pkl'):
    model.load_state_dict(load("./models/model.pkl"))
    optimizer.load_state_dict(load("./models/optimizer.pkl"))

loss_function = nn.CTCLoss()
my_transforms = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.9238877, 0.9249362, 0.9240683), std=(0.2109205, 0.20895848, 0.2106626))
    ]
)
mnist_train = Letter2Dataset(root="./picture", transform=my_transforms)
def train(epoch):
    total_loss = []
    dataloader = DataLoader(mnist_train, batch_size=batch_size, shuffle=True, drop_last=True)
    dataloader = tqdm(dataloader, total=len(dataloader))
    model.train()
    for images, labels, labels_lengths in dataloader:
        images = images.to(device)
        labels = labels.to(device)
        # 梯度置0
        optimizer.zero_grad()
        # 前向传播
        output = model(images)
        # 通过结果计算损失

        input_lengths = torch.IntTensor([output.shape[0]]*output.shape[1])
        # print(input_lengths.shape)
        loss = loss_function(output, labels, input_lengths, labels_lengths)
        total_loss.append(loss.item())
        dataloader.set_description('loss:{}'.format(np.mean(total_loss)))
        # 反向传播
        loss.backward()
        # 优化器更新
        optimizer.step()

    save(model.state_dict(), './models/model.pkl')
    save(optimizer.state_dict(), './models/optimizer.pkl')
    # 打印一下训练成功率, test.test_success()
    print('第{}个epoch，成功率, 损失为{}'.format(epoch, np.mean(total_loss)))

for i in range(12):
    train(i)
    print(test())