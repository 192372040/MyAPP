from flask import request, jsonify
import google.generativeai as genai

# Paste your Gemini API key here
genai.configure(
    api_key="AQ.Ab8RN6LIYXjTQK2DoRI9j0Z-jIxmIEpaIx8XIqf0iIXwIkXlNQ"
)

model = genai.GenerativeModel("gemini-2.5-flash")

def ai_chat():

    data = request.json

    message = data.get("message", "")

    try:

        prompt = f"""
        You are MedAI.

        Answer only healthcare, wellness,
        nutrition, fitness, mental health,
        and medical education questions.

        If the question is not related to health,
        reply:

        'I am a healthcare assistant.
        Please ask health-related questions.'

        User Question:
        {message}
        """

        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "reply": response.text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })