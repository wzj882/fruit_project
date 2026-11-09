import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader

# 1. 自动检测设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('正在使用的设备:', device)

# 2. 图片预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 3. 指定刚刚建好的 data 文件夹路径
data_dir = "./data"
dataset = datasets.ImageFolder(data_dir, transform=transform)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

print("成功加载图片数量:", len(dataset))
print("识别到的分类:", dataset.classes)

# 4. 加载并修改模型 (迁移学习)
model = models.resnet18(weights="ResNet18_Weights.IMAGENET1K_V1")
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(512, 2) 
model = model.to(device)

# 5. 训练参数
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)
num_epochs = 20

# 6. 开始训练
print("\n开始训练，AI正在学习苹果...\n")
model.train()
for epoch in range(num_epochs):
    total_loss = 0.0
    for images, labels in dataloader:
        images = images.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(dataloader)
    print(f"第 {epoch+1}/{num_epochs} 轮 | 损失: {avg_loss:.4f}")

# 7. 保存模型
torch.save(model.state_dict(), "fruit_model.pth")
print("\n训练结束！模型已保存。")