import google.generativeai as genai
from PIL import Image

# --- API anahtarını ayarla ---
genai.configure(api_key="AIzaSyBEhKQ6xUzE0WNTAhjy24Pu3fgi86vvAyE")

# --- Modeli tanımla ---
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Resmi aç ---
img = Image.open("C:/Users/dilar/OneDrive/Resimler/image1.jpg")

# --- Sohbet oturumunu başlat ---
chat = model.start_chat(history=[
    {"role": "user", "parts": ["Lütfen bu matematik sorusunu adım adım çöz.", img]}
])

# --- İlk yanıtı al ---
response = chat.send_message("Bu soruyu adım adım çöz.")
print("\n🤖 İlk yanıt:")
print(response.text)
print("-" * 60)

# --- Kullanıcı bitir diyene kadar konuşmayı sürdür ---
while True:
    user_input = input("👤 Sen: ")
    if user_input.lower() in ["bitir", "exit", "quit", "q"]:
        print("🔚 Konuşma sonlandırıldı.")
        break

    response = chat.send_message(user_input)
    print("\n🤖 Gemini:")
    print(response.text)
    print("-" * 60)
