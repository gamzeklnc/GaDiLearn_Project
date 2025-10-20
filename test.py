import google.generativeai as genai
from PIL import Image 

genai.configure(api_key="AIzaSyBEhKQ6xUzE0WNTAhjy24Pu3fgi86vvAyE")

model = genai.GenerativeModel("gemini-2.5-flash")

img = Image.open("C:/Users/gamze/Pictures/Screenshots/soru1.png")

response = model.generate_content(
    [
        "Lütfen bu matematik sorusunu adım adım çöz.",
        img
    ]
)

print(response.text)