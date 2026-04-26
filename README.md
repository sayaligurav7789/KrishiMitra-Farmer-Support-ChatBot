# 🌾 KrishiMitra - Farmer Support ChatBot

KrishiMitra is an advanced, AI-powered multilingual chatbot designed to assist farmers by providing real-time information on crop prices, weather forecasts, agricultural techniques, pest management, and government schemes. It bridges the information gap in the agricultural sector through a conversational interface, making expert knowledge easily accessible.

## 🌟 Key Features

- **🗣️ Multilingual Support:** Interact in English, Hindi, Kannada, Telugu, Malayalam, and Tamil using Google Translate integration.
- **🎙️ Voice Interaction:** Supports Speech-to-Text and Text-to-Speech for seamless accessibility.
- **🧠 AI-Powered NLP:** Built with TensorFlow/Keras and NLTK for high-accuracy intent classification.
- **🌦️ Comprehensive Assistance:** Answers queries on weather, organic farming, soil management, livestock, and crop selection.
- **📄 Scheme Navigator:** Direct links and region-wise guidance for government agricultural schemes.
- **⚡ Real-time Communication:** Powered by Flask-SocketIO and React for instant responses.

## 🛠️ Technology Stack

- **Frontend:** React.js, Vite, Tailwind CSS, Socket.io-client
- **Backend:** Python, Flask, Flask-SocketIO
- **Machine Learning:** TensorFlow, Keras, NLTK
- **APIs & Services:** Web Speech API, Googletrans

---

## 🏗️ Architecture & Data Flow

### Data Flow Diagram           
<img width="583" height="341" alt="image" src="https://github.com/user-attachments/assets/6430204c-0731-489c-9775-27f79b6c690d" />

### System Architecture Diagram 
<img width="486" height="324" alt="image" src="https://github.com/user-attachments/assets/52b85e9b-f412-4efc-baba-bc62f94250d1" />

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python 3.12+

### 1. Backend Setup
```bash
cd Farmer-Support-ChatBot/Code/backend
python -m venv venv
# On Windows use: venv\Scripts\activate
# On Linux/Mac use: source venv/bin/activate
pip install -r requirements.txt
python chat.py
```

### 2. Frontend Setup
```bash
cd Farmer-Support-ChatBot/Code/frontend
npm install
npm run dev
```

---

## 📱 Implementation Results & Previews

### Choose response language:
<img width="633" height="308" alt="image" src="https://github.com/user-attachments/assets/a2109826-69ac-4016-98d1-5a132e739270" />

### Ask Different Queries:
<img width="627" height="290" alt="image" src="https://github.com/user-attachments/assets/48cce7c7-4875-4e51-98e4-57fddef92cb1" />

### Know Farming Schemes Region Wise:
<img width="627" height="302" alt="image" src="https://github.com/user-attachments/assets/89d7c499-c2f5-4f47-8d67-7702baf1f519" />

### Choices For Region:
<img width="609" height="300" alt="image" src="https://github.com/user-attachments/assets/e76c56d1-e6eb-461e-8596-ff60e8cd6a22" />

### Selected Region Delhi:
<img width="609" height="311" alt="image" src="https://github.com/user-attachments/assets/c7528686-8556-4023-9bf8-8463811a7d3a" />

### Redirect to website:
<img width="612" height="313" alt="image" src="https://github.com/user-attachments/assets/0d7eddea-debc-4057-a08d-e0c3dbdb028e" />

<img width="596" height="475" alt="image" src="https://github.com/user-attachments/assets/4f39f83e-28dc-4e17-8700-636556f2f943" />

---
## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License
This project is [MIT](LICENSE) licensed.
