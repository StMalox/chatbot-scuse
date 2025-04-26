from dotenv import load_dotenv
from openai import OpenAI
import os
# questo è per fare girare il chatbot su Render
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inizializzo istanza OpenAI e set la Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

# Commento la versione meno lineare
# os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
# client = OpenAI()
# client.api_key = os.environ['OPENAI_API_KEY']

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if question.lower() in ['esci', 'exit']:
            return jsonify({"answer": "Ciao ciao! Ricordati di leggere il mio ultimo articolo!"})

    if not question:
            return jsonify({"answer": "Non hai scritto nessuna domanda!"})
# Adesso creo il chatbot
# questo era rimasto da prima: def chatbot(question):
   
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei uno studente che arriva sempre in ritardo. Inventa straordinarie e distopiche scuse per giustificare il ritardo. Rispondi in inglese anche se la domanda è in altre lingue"}
            ,{"role": "user", "content": question}
        ],
        max_tokens=100,
        temperature=0.9
    )
#    story = completion.choices[0].message.content
#    return story
    return jsonify({"answer": completion.choices[0].message.content})    

# E adesso scrivo la main function
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    print("Benvenuto al tuo contaballe! Dimmi per quale lezione sei in ritardo. Scrivi 'esci' per terminare")

    while True:
        question = input("\n Che balla ti devo inventare?: ")

        if question.lower() in ['esci', 'exit']:
            print("Ciao ciao!")
            break
        story = chatbot(question)
        print(story)
