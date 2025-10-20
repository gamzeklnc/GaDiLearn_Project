import os
import re
import json
import requests
import google.generativeai as genai

# 🔑 API KEY'LER — Buraya kendi anahtarlarını gir veya ortam değişkeni olarak ayarla
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyBEhKQ6xUzE0WNTAhjy24Pu3fgi86vvAyE"
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

# 📝 Problem prompt'unu JSON formatında yanıt istemek için hazırlıyoruz
def build_prompt(problem: str) -> str:
    return f"""
You are a careful math solver. Solve the problem step by step, but RETURN YOUR OUTPUT AS PURE JSON ONLY with this schema:
{{
  "final_answer": "<string>",
  "steps": ["step 1", "step 2", "..."]
}}
Rules:
- final_answer must be simplified, exact if possible (e.g., 2/3, sqrt(2), pi/4).
- Do NOT add any text before or after the JSON.
Problem:
{problem}
""".strip()

# 🧠 JSON çıkarma fonksiyonu + fallback
def extract_json(text: str):
    if not text:
        return None
    text = text.strip()
    # JSON yakalama
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
    # Fallback: metinden doğrudan sayı yakala
    match = re.search(r'(-?\d+(\.\d+)?)', text)
    if match:
        return {"final_answer": match.group(1), "steps": []}
    return None

# 🧼 Cevap normalizasyonu (boşluk, nokta vs. temizleme)
def normalize_answer(s: str) -> str:
    if not s:
        return ""
    s = str(s)
    s = re.sub(r'[\s\n\t\r]+', '', s)
    s = re.sub(r'\.$', '', s)
    return s.lower()

# ⚡ Gemini'den cevap alma
def ask_gemini(problem: str, model_name: str = "gemini-flash-latest") -> dict:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(build_prompt(problem))
    data = extract_json(resp.text or "")
    return data or {"final_answer": "", "steps": [], "raw": resp.text}

# 🧠 Mistral (OpenRouter) cevabı
def ask_mistral(problem: str, model_name: str = "mistralai/mistral-7b-instruct") -> dict:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": "Return ONLY pure JSON as specified."},
        {"role": "user", "content": build_prompt(problem)}
    ]
    payload = {"model": model_name, "messages": messages}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    text = r.json()["choices"][0]["message"]["content"]
    data = extract_json(text or "")
    return data or {"final_answer": "", "steps": [], "raw": text}

# 🧠 İki modelin cevabını karşılaştır
def solve_with_consensus(problem: str):
    print(f"\n🧪 Problem: {problem}\n")

    g = ask_gemini(problem)
    m = ask_mistral(problem)

    g_ans_raw = g.get("final_answer", "")
    m_ans_raw = m.get("final_answer", "")

    g_ans = normalize_answer(g_ans_raw)
    m_ans = normalize_answer(m_ans_raw)

    # Debug için
    print(f"GEMINI RAW FINAL: {repr(g_ans_raw)}")
    print(f"MISTRAL RAW FINAL: {repr(m_ans_raw)}")

    if g_ans and g_ans == m_ans:
        print(f"\n✅ Konsensüs (Gemini + Mistral): {g_ans_raw}")
        if g.get("steps"):
            print("\n📌 Çözüm Adımları (Gemini):")
            for i, s in enumerate(g["steps"], 1):
                print(f"{i}. {s}")
    else:
        print("\n⚠️ Modeller farklı cevaplar verdi:")
        print(f"Gemini : {g_ans_raw}")
        print(f"Mistral: {m_ans_raw}")

        if g.get("steps"):
            print("\n[Gemini Steps]")
            for s in g["steps"]:
                print(f"- {s}")

        if m.get("steps"):
            print("\n[Mistral Steps]")
            for s in m["steps"]:
                print(f"- {s}")

# 🚀 Test
if __name__ == "__main__":
    problem = "15+10 nedir "
    solve_with_consensus(problem)
