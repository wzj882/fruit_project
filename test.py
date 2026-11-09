import torch
import os
from torchvision import transforms, models
from PIL import Image
import torch.nn.functional as F

# 1. 基础配置
device = torch.device('cpu')
classes = ['fresh', 'rotten'] # AI 只认识这两个词

# 2. 图片预处理（和训练时一模一样）
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 3. 加载 AI 大脑 (模型)
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(512, 2)
model.load_state_dict(torch.load('fruit_model.pth', map_location=device))
model.to(device)
model.eval()

# 4. 直接指定你要测试的图片路径
# 比如你桌面上那张叫 hh.webp 的图
image_path = r'C:\Users\Administrator\Desktop\hh.webp' 

# 5. 开始测试
if os.path.exists(image_path):
    try:
        print(f"📸 正在让 AI 观察图片：hh.webp...")
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(image_tensor)
            probs = F.softmax(outputs, dim=1)[0]
            
        predicted_idx = torch.argmax(probs).item()
        confidence = probs[predicted_idx].item() * 100
        
        print(f"🤖 AI 最终判断：这是一个 {classes[predicted_idx]} 的水果")
        print(f"💪 AI 的自信程度：{confidence:.2f}%")
        
    except Exception as e:
        print(f"❌ 识别失败，错误原因：{e}")
else:
    print(f"❌ 没找到这张图片！")
    print(f"请确保你的电脑桌面上有一张叫 hh.webp 的照片。")
    print(f"或者，直接把你想测试的图片路径填在代码的第 32 行 image_path 里。")