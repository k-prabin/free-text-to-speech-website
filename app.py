import os
from flask import Flask, request, render_template, send_file
import edge_tts
from docx import Document

app = Flask(__name__)

VOICES = {
    "en-AU-NatashaNeural": "Natasha (Australia)",
    "en-AU-WilliamNeural": "William (Australia)",
    "en-AU-AnnetteNeural": "Annette (Australia)",
    "en-AU-CarlyNeural": "Carly (Australia)",
    "en-CA-ClaraNeural": "Clara (Canada)",
    "en-CA-LiamNeural": "Liam (Canada)",
    "en-GB-SoniaNeural": "Sonia (UK)",
    "en-GB-RyanNeural": "Ryan (UK)",
    "en-GB-LibbyNeural": "Libby (UK)",
    "en-GB-AbbiNeural": "Abbi (UK)",
    "en-HK-YanNeural": "Yan (Hong Kong)",
    "en-HK-SamNeural": "Sam (Hong Kong)",
    "en-IE-EmilyNeural": "Emily (Ireland)",
    "en-IE-ConnorNeural": "Connor (Ireland)",
    "en-IN-NeerjaNeural": "Neerja (India)",
    "en-IN-PrabhatNeural": "Prabhat (India)",
    "en-KE-AsiliaNeural": "Asilia (Kenya)",
    "en-KE-ChilembaNeural": "Chilemba (Kenya)",
    "en-NG-EzinneNeural": "Ezinne (Nigeria)",
    "en-NG-AbeoNeural": "Abeo (Nigeria)",
    "en-NZ-MollyNeural": "Molly (New Zealand)",
    "en-NZ-MitchellNeural": "Mitchell (New Zealand)",
    "en-PH-RosaNeural": "Rosa (Philippines)",
    "en-PH-JamesNeural": "James (Philippines)",
    "en-SG-LunaNeural": "Luna (Singapore)",
    "en-SG-WayneNeural": "Wayne (Singapore)",
    "en-TZ-ImaniNeural": "Imani (Tanzania)",
    "en-TZ-ElimuNeural": "Elimu (Tanzania)",
    "en-US-JennyNeural": "Jenny (US)",
    "en-US-JennyMultilingualNeural3": "Jenny Multilingual (US)",
    "en-US-GuyNeural": "Guy (US)",
    "en-US-AriaNeural": "Aria (US)",
    "en-US-DavisNeural": "Davis (US)",
    "en-US-AmberNeural": "Amber (US)",
    "en-US-AnaNeural": "Ana (US)",
    "en-US-AshleyNeural": "Ashley (US)",
    "en-US-BrandonNeural": "Brandon (US)",
    "en-US-ChristopherNeural": "Christopher (US)",
    "en-US-CoraNeural": "Cora (US)",
    "en-US-ElizabethNeural": "Elizabeth (US)",
    "en-US-EricNeural": "Eric (US)",
    "en-US-JacobNeural": "Jacob (US)",
    "en-US-JaneNeural": "Jane (US)",
    "en-US-JasonNeural": "Jason (US)",
    "en-US-MichelleNeural": "Michelle (US)",
    "en-US-MonicaNeural": "Monica (US)",
    "en-US-NancyNeural": "Nancy (US)",
    "en-US-RogerNeural": "Roger (US)",
    "en-US-SaraNeural": "Sara (US)",
    "en-US-SteffanNeural": "Steffan (US)",
    "en-US-TonyNeural": "Tony (US)",
    "en-US-AIGenerate1Neural1": "AI Generate 1 (US)",
    "en-US-AIGenerate2Neural1": "AI Generate 2 (US)",
    "en-US-EliseNeural": "Elise (US)",
    "en-US-FrancisNeural": "Francis (US)",
    "en-US-LaylaNeural": "Layla (US)",
    "en-US-RyanNeural": "Ryan (US)"
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