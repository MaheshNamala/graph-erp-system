import google.generativeai as genai

# 🔑 Put your API key here
genai.configure(api_key="YAIzaSyAwhiTjT4T0oApxwFj8NSCVeWovPcMVtjU")

# ✅ Updated model (IMPORTANT FIX)
model = genai.GenerativeModel("gemini-1.5-flash")


def classify_query(user_query):
    try:
        prompt = f"""
Classify this ERP query into ONE label:

1. NOT_BILLED
2. DELIVERED_NOT_BILLED
3. NOT_PAID
4. TRACE
5. UNKNOWN

Return ONLY the label.

Query: {user_query}
"""

        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip().upper()
        else:
            return "UNKNOWN"

    except Exception as e:
        print("LLM ERROR:", e)
        return "UNKNOWN"