from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '')
    respuesta_ia = "Lo siento, hubo un error al procesar tu mensaje."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable y útil."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        respuesta_ia = response.choices[0].message.content.strip()
    except Exception as e:
        print("Error con OpenAI:", e)

    resp = MessagingResponse()
    resp.message(respuesta_ia)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
