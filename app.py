import os
from flask import Flask, request, render_template, send_file
import edge_tts
from docx import Document

app = Flask(__name__)

VOICES = {
    "en-AU-NatashaNeural": "Alice (Australia)",
    "en-AU-WilliamNeural": "Oscar (Australia)",
    "en-AU-AnnetteNeural": "Sophie (Australia)",
    "en-AU-CarlyNeural": "Jack (Australia)",
    "en-CA-ClaraNeural": "Ella (Canada)",
    "en-CA-LiamNeural": "Noah (Canada)",
    "en-GB-SoniaNeural": "Eleanor (UK)",
    "en-GB-RyanNeural": "Oliver (UK)",
    "en-GB-LibbyNeural": "Charlotte (UK)",
    "en-GB-AbbiNeural": "Harry (UK)",
    "en-HK-YanNeural": "Grace (Hong Kong)",
    "en-HK-SamNeural": "Leo (Hong Kong)",
    "en-IE-EmilyNeural": "Finn (Ireland)",
    "en-IE-ConnorNeural": "Maeve (Ireland)",
    "en-IN-NeerjaNeural": "Asha (India)",
    "en-IN-PrabhatNeural": "Rohan (India)",
    "en-KE-AsiliaNeural": "Zuri (Kenya)",
    "en-KE-ChilembaNeural": "Jabari (Kenya)",
    "en-NG-EzinneNeural": "Chinyere (Nigeria)",
    "en-NG-AbeoNeural": "Obi (Nigeria)",
    "en-NZ-MollyNeural": "Ruby (New Zealand)",
    "en-NZ-MitchellNeural": "Liam (New Zealand)",
    "en-PH-RosaNeural": "Isabel (Philippines)",
    "en-PH-JamesNeural": "Gabriel (Philippines)",
    "en-SG-LunaNeural": "Kai (Singapore)",
    "en-SG-WayneNeural": "Leah (Singapore)",
    "en-TZ-ImaniNeural": "Tendo (Tanzania)",
    "en-TZ-ElimuNeural": "Juma (Tanzania)",
    "en-US-JennyNeural": "Emily (US)",
    "en-US-JennyMultilingualNeural3": "Max (US)",
    "en-US-GuyNeural": "Sophia (US)",
    "en-US-AriaNeural": "Ethan (US)",
    "en-US-DavisNeural": "Ava (US)",
    "en-US-AmberNeural": "Logan (US)",
    "en-US-AnaNeural": "Chloe (US)",
    "en-US-AshleyNeural": "Mason (US)",
    "en-US-BrandonNeural": "Harper (US)",
    "en-US-ChristopherNeural": "Zoe (US)",
    "en-US-CoraNeural": "Jackson (US)",
    "en-US-ElizabethNeural": "Emma (US)",
    "en-US-EricNeural": "Madison (US)",
    "en-US-JacobNeural": "Lily (US)",
    "en-US-JaneNeural": "Caleb (US)",
    "en-US-JasonNeural": "Avery (US)",
    "en-US-MichelleNeural": "Wyatt (US)",
    "en-US-MonicaNeural": "Grace (US)",
    "en-US-NancyNeural": "Elijah (US)",
    "en-US-RogerNeural": "Hannah (US)",
    "en-US-SaraNeural": "Benjamin (US)",
    "en-US-SteffanNeural": "Natalie (US)"
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        voice = request.form["voice"]
        output_file = "output.mp3"

        async def convert_text_to_speech():
            communicate = edge_tts.Communicate(text, voice)
            with open(output_file, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])

        import asyncio
        asyncio.run(convert_text_to_speech())

        return send_file(output_file, as_attachment=True)

    return render_template("index.html", voices=VOICES)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
