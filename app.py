import streamlit as st
import torch
from PIL import Image
from torchvision import transforms, models
import torch.nn.functional as F

# 页面标题
st.title("🍇 AI 水果新鲜度检测神器 🍎")
st.write("请上传一张水果图片，让 AI 告诉你它新不新鲜！")

# 1. 加载 AI 模型 (和 test.py 保持一致)
device = torch.device('cpu')
model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(512, 2)
model.load_state_dict(torch.load("fruit_model.pth", map_location=device))
model.to(device)
model.eval()

# 2. 图片预处理 (和 train.py 里完全一样)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 3. 定义上传组件
uploaded_file = st.file_uploader("选择一张图片...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    
    # 左右分列显示
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📸 原图")
        st.image(image, width=300)

    with col2:
        # 开始推理
        image_tensor = transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(image_tensor)
            probs = F.softmax(outputs, dim=1)[0]

        fresh_conf = probs[0].item() * 100
        rotten_conf = probs[1].item() * 100
        
        # 获取预测结果
        predicted_idx = torch.argmax(probs).item()
        classes = ['新鲜 (Fresh)', '腐烂 (Rotten)']
        result = classes[predicted_idx]
        
        # 显示结果
        st.subheader("🤖 AI 分析报告")
        if predicted_idx == 0:
            st.success(f"AI 判断：该水果为 **{result}**", icon="✅")
        else:
            st.error(f"AI 判断：该水果为 **{result}**", icon="❌")
        
        # 画进度条
        st.write(f"🟢 新鲜的概率：{fresh_conf:.2f}%")
        st.progress(float(fresh_conf) / 100)
        st.write(f"🔴 腐烂的概率：{rotten_conf:.2f}%")
        st.progress(float(rotten_conf) / 100)