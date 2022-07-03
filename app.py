from sanic import Sanic
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sanic.response import json
import time

app = Sanic("BBOT-Server")

@app.before_server_start
async def load_model(app):
    global MODEL, TOKENIZER
    # Initialize the tokenizer, model for Blender Bot
    # TOKENIZER = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill",
    #                                         cache_dir="models/blenderbot-400M-distill")
    # MODEL = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill",
    #                                         cache_dir="models/blenderbot-400M-distill")

    TOKENIZER = AutoTokenizer.from_pretrained("facebook/blenderbot_small-90M",
                                            cache_dir="models/blenderbot_small-90M")
    MODEL = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot_small-90M",
                                            cache_dir="models/blenderbot_small-90M")

@app.route('/open-chat', methods=['POST'])
async def en_to_vi(request):
    global MODEL, TOKENIZER
    text = request.json["text"]

    tokenized_text = TOKENIZER([text], return_tensors="pt")

    # Perform translation and decode the output
    reply_ids = MODEL.generate(**tokenized_text)
    reply_text = TOKENIZER.batch_decode(reply_ids, skip_special_tokens=True)[0]

    return json({'text': reply_text})


if __name__ == '__main__':
    app.run()