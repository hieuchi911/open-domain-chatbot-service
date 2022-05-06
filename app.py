from sanic import Sanic
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sanic.response import json
import time

app = Sanic("NMT-Server")

@app.before_server_start
async def load_model(app):
    global MODEL, TOKENIZER, VI_EN_MODEL, VI_EN_TOKENIZER
    # Initialize the tokenizer, model for English to Vietnamese Translation
    TOKENIZER = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
    MODEL = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")

@app.route('/open-chat', methods=['POST'])
async def en_to_vi(request):
    global MODEL, TOKENIZER
    text = request.json["text"]

    start = time.time()
    tokenized_text = TOKENIZER([text], return_tensors="pt")
    end = time.time()
    print("\n\nTOKENIZER took: ", end - start)

    # Perform translation and decode the output
    start = time.time()
    reply_ids = MODEL.generate(**tokenized_text)
    end = time.time()
    print("\nMODEL generate took: ", end - start)
    
    start = time.time()
    reply_text = TOKENIZER.batch_decode(reply_ids, skip_special_tokens=True)[0]
    end = time.time()
    print("\nTOKNEIZER batch decode took: ", end - start)

    # Print translated text
    print("\n", reply_text, "\n\n")

    return json({'text': reply_text})


if __name__ == '__main__':
    app.run()