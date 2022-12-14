# Blender-Bot-Service

## I. Notebook `test-blender-bot-model.ipynb`:
contains code for:
- loading and testing several open domain chatbot models (Facebook BlenderBot 90M params and 400M params). Once load model from huggingface, pretrained models will be downloaded and cached in host machine at `models/` folder in this project
- testing sanic apps that serve open domain chatbot models

## II. Other python files:
contain sanic apps that serve open domain chatbot models:
- `app.py` serves Facebook BlenderBot 90M params model (400M params model consumes a lot resource so it's commented out)

To host these sanic services on host machine, execute following command:
  >```
  >python -m sanic <name of file that stores sanic app, e.g if file named app_opus.py, type 'app_opus'>:<name of Sanic object defined in python file> -H <host address> -p <listening port>
  >```

## III. Docker:
- docker image: hieuchi911/open-domain-kit:without-ckpts. Only 2 files needed to build this image: dockerfile and `requirements.txt` (both at repo [Translate-Service](https://gitlab.com/ct_group1/chatbot/other-services/Translate-Service)). `requirements.txt` in this repo is only used for this bot model, not used for open-domain-kit image.
- to run docker services for translate service:
  - run the image, binding the container's working directory with directory containing sanic app file (e.g in this repo, `app.py` or `app_opus.py`) and `models/` folder for translate service (similarly for open-domain-chatbot service).
  - run sanic service in the container (either via `CMD` in dockerfile or provide command at `container run`)
  - these steps is shown in following example:
    >```
    > sudo docker run --name blender-bot-service -p 8002:8001 -v ".>/actions/Blender-Bot-Service/:/python-docker/" hieuchi911/open-domain-kit:without-ckpts python -m sanic app:app -H 0.0.0.0 -p 8001
    >```
    ,where:
    - `-v "./actions/Blender-Bot-Service/:/python-docker/"` maps host machine's directory that stores sanic app and `models/` folder (`./actions/Blender-Bot-Service/`) with the container's working directory (`/python-docker/`)
    - `python -m sanic app:app -H 0.0.0.0 -p 8001` is the command that run sanic service to listen at port 8000 in the container at container startup. This command is optional since the defined dockerfile already defines this at `CMD` instruction, port specified is 5351 instead of 8000 (the python command in dockerfile wont run since it's overwritten by the python command defined at `docker run`, according to https://docs.docker.com/engine/reference/run/#cmd-default-command-or-options)
    - `-p 8002:8001` maps port `8001` in container to port `8002` in local machine, so requests from outside should be sent to port `8002`
  - Example above corresponds to following docker-compose service block:
    >```
    >blender-bot-service:
    >    image: "hieuchi911/open-domain-kit:without-ckpts"
    >    expose:
    >       - 8002
    >    volumes:
    >       - ./actions/Blender-Bot-Service:/python-docker
    >    command: ["python", "-m", "sanic", "app:app", "-H", "0.0.0.0", "-p", "8001"]
    >```