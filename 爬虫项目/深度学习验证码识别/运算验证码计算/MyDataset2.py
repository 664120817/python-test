from torch.utils.data import Dataset
import os
from PIL import Image
import torch

class Letter2Dataset(Dataset):
    def __init__(self, root: str, transform=None):
        super(Letter2Dataset, self).__init__()
        self.path = root
        self.transform = transform
        # 可优化
        self.mapping = [i for i in '_0123456789加减乘+-*']

    def load_picture_path(self):
        picture_list = list(os.walk(self.path))[0][-1]
        # 这里可以增加很多的错误判断
        return picture_list

    def __len__(self):
        return len(self.load_picture_path())

    def __getitem__(self, item):
        load_picture = self.load_picture_path()
        image = Image.open(self.path + '/' +load_picture[item])
        if self.transform:
            image = self.transform(image)
        labels = [self.mapping.index(i) for i in load_picture[item].split('_')[0]]
        for i in range(9-len(labels)):
            labels.insert(0, 0)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        return image, labels, len(labels)

if __name__ == '__main__':
    from tqdm import tqdm
    import numpy as np
    from torchvision import transforms
    transform = transforms.Compose([transforms.ToTensor(),])
    my_train = Letter2Dataset(root="./picture", transform=transform)
    total_mean = [[], [], []]
    total_std = [[], [], []]
    res_total = [0, 0, 0]
    res_std = [0, 0, 0]
    for i in tqdm(range(len(my_train))):
        for j in range(len(total_std)):
            total_mean[j].append([np.array(my_train[i][0][j])])
            total_std[j].append([np.array(my_train[i][0][j])])

    for i in range(len(total_std)):
        res_total[i] = np.mean(total_mean[i])
        res_std[i] = np.std(total_std[i])
    print(res_total, res_std)