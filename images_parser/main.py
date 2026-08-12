from PIL import Image
import requests
import os
import pathlib
from dotenv import load_dotenv
#бля, нахуй  я ваще сел это делать? 

load_dotenv()


model_name = os.getenv('MODEL_NAME')
API_LINK = os.getenv('API_LINK')
ROOT_PATH = os.getenv('ROOT_PATH')

#Ставлю основные папки
root_dir = pathlib.Path(ROOT_PATH).resolve().parent
dirs = [x[1] for x in os.walk(root_dir)] # хавает только директории в основном файле
image_path = pathlib.Path.joinpath(root_dir,'images') # путь для картинок
image_folder = [x[2] for x in os.walk(image_path)] # перебор картинок

def check_directiry():
    if "description" not in dirs[0]:
        os.mkdir(pathlib.Path.joinpath(root_dir,"description"))
        return print('Папка с описанием создана')
    return

def clear_text(request_text):
    text = request_text.split('. ')
    return text

def write_down_text(text,name):

    desk_path = pathlib.Path.joinpath(root_dir,"description")
    desk = [x[1] for x in os.walk(desk_path)]
    filename = pathlib.Path.joinpath(desk_path,name+'.txt')
    if name in desk[0]:
        filename = pathlib.Path.joinpath(desk_path,name+'new.txt')
    with open(filename,'w') as file:
        for line in text[1:]:
            file.write(line+".\n")
    return print('готово')

def send_api_request(model_name,image_path):
    with Image.open(image_path) as img:
        metadata = img.info
        for key, value in metadata.items():
            closer = value.find('Negative prompt:')
            prompt = value[:closer]

    payload = {'model': model_name,"store": False,"input":f"{prompt}.",'system_prompt':'''You are a creative text-generation system.

You will receive a list of tags. Based on these tags, write a vivid, coherent, and engaging text consisting of exactly 4 to 6 sentences. Use the tags as the main thematic guidance and incorporate their ideas naturally into the text.'''}
    print('ожидание ответа нейронки')
    request = requests.post(F'{API_LINK}/api/v1/chat',json=payload)
    print('ответ пришёл')
    response = request.json()
    return clear_text(response['output'][0]['content'])



def generate_text_into_better_text():
    for image in image_folder[0]:
        text = send_api_request(model_name,pathlib.Path.joinpath(image_path,image))
        write_down_text(text,image.replace('.png',''))
    return
