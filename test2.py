import google.generativeai as genai

# 1️⃣ İlk API Key (örneğin flash)
genai.configure(api_key="AIzaSyBEhKQ6xUzE0WNTAhjy24Pu3fgi86vvAyE")
model1 = genai.GenerativeModel("gemini-2.5-flash")

# 2️⃣ Sorgu
prompt = "Nasılsın"

response1 = model1.generate_content(prompt)
answer1 = response1.text.strip()

# 3️⃣ İkinci API Key (örneğin pro)
genai.configure(api_key="AIzaSyBEhKQ6xUzE0WNTAhjy24Pu3fgi86vvAyE")
model2 = genai.GenerativeModel("gemini-2.5-pro")

response2 = model2.generate_content(prompt)
answer2 = response2.text.strip()

# 4️⃣ Karşılaştırma
if answer1 == answer2:
    print("✅ İki model de aynı cevabı verdi:")
    print(answer1)
else:
    print("⚠️ Modeller farklı cevaplar verdi:")
    print("Flash:", answer1)
    print("Pro  :", answer2)
