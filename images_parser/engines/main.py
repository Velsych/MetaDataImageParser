from PIL import Image
import requests
import os
import pathlib
from images_parser.tools import parsers
from dotenv import load_dotenv
import logging



# config = dotenv_values(".env")
current_dir = pathlib.Path.cwd()
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

logging.basicConfig( format = u'%(filename)s# %(levelname)-8s [%(asctime)s]  %(message)s',level=logging.INFO)

#бля, нахуй  я ваще сел это делать? 

 #сюда добавить дотенв из винды


model_name = os.getenv('MODEL_NAME')
API_LINK = os.getenv('API_LINK')
ROOT_PATH = os.getenv('ROOT_PATH')

timeout_process = []
timeout_connect = []
faulty_pics = []

#Ставлю основные папки

root_dir = current_dir / "images_parser"
dirs = [x[1] for x in os.walk(root_dir)] # хавает только директории в основном файле
image_path = pathlib.Path.joinpath(root_dir,'images') # путь для картинок
image_folder = [x[2] for x in os.walk(image_path)] # перебор картинок
quality_tags_file = pathlib.Path.joinpath(root_dir,'quality_tags.txt')
QUALITY_TAGS = parsers.get_quality_tags(quality_tags_file)

def check_directiries():
    needed_directories = ['description',"description tags"]
    logging.info("Checkong existing derictories")
    for dir in needed_directories:
        if dir not in dirs[0]:
            os.mkdir(pathlib.Path.joinpath(root_dir,dir))
            logging.info("All needed derictories created!")
    logging.info("All directories founded!")
    return

def clear_text(request_text):
    logging.info('Cleaning text')
    text = request_text.split('. ')
    return text

def write_down_readable_file(text,name):
    desk_path = pathlib.Path.joinpath(root_dir,"description")
    desk = [x[1] for x in os.walk(desk_path)]
    filename = pathlib.Path.joinpath(desk_path,name+'.txt')
    if name in desk[0]:
        filename = pathlib.Path.joinpath(desk_path,name+'new.txt')
    with open(filename,'w') as file:
        for line in text[1:]:
            file.write(line+".\n")
    logging.info(f'File {name}.txt created')
    return
def write_down_text_file(text,name):
    desk_path = pathlib.Path.joinpath(root_dir,"description tags")
    desk = [x[1] for x in os.walk(desk_path)]
    filename = pathlib.Path.joinpath(desk_path,name+'.txt')
    if name in desk[0]:
        filename = pathlib.Path.joinpath(desk_path,name+'new.txt')
    with open(filename,'w') as file:
            file.write(text+".\n")
    logging.info(f'File {name}.txt created')
    return
def send_api_request(model_name,prompt,name):
    try:
        payload = {'model': model_name,"store": False,"input":f"{prompt}.",'system_prompt':'''You are a creative text-generation system.You will receive a list of tags. Based on these tags, write a vivid, coherent, and engaging text consisting of exactly 4 to 6 sentences. Use the tags as the main thematic guidance and incorporate their ideas naturally into the text.'''}
        request = requests.post(F'{API_LINK}/api/v1/chat',json=payload,timeout=(3.05,360))
    except (requests.exceptions.ConnectionError,requests.exceptions.ConnectTimeout) as e:
        logging.warning(f"Cannot to recieve answer from LLM server. Error{e}")
        logging.warning("Skipping sequence")
        timeout_connect.append(name)
        return '',True
    except (requests.exceptions.ReadTimeout,requests.exceptions.Timeout) as e:
        logging.warning("LLM model processing answer too long, skipping")
        timeout_process.append(name)
        return "",True
    else:
        logging.info('Got answer, parsing...')
        response = request.json()
        return clear_text(response['output'][0]['content']),False

def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info
            for _, value in metadata.items():
                closer = value.find('Negative prompt:')
                prompt = value[:closer]
    except OSError as e:
        logging.critical(f'An error has occured, cannot process image')
        return "", True
    else:
        e = False
    return prompt,e

def tags_cleaner(not_cleaned_tags: str) -> str:
    text = not_cleaned_tags
    for tag in QUALITY_TAGS:
        if tag == "":
            continue
        text = text.lower().replace(tag.lower(),'')
    logging.info("Purge complete")
    return text

def generate_text_into_better_text():
    for image in image_folder[0]:
        if image.endswith('.png'):
            logging.info(f'Processing: {image}')
            tags,e = get_image_metadata(pathlib.Path.joinpath(image_path,image))
            if e != False:
                logging.warning("Error occured, but i'm still working")
                logging.info("Skipping malfunctioning part...")
                continue
            logging.info("Start clearing quality tags.")
            cleared_tags = tags_cleaner(tags)
            logging.info('Sending api request')
            ai_text,e = send_api_request(model_name,cleared_tags,image)
            if e != False:
                logging.warning("Error occured, but i'm still working")
                logging.info("Skipping malfunctioning part...")
                continue
            logging.info("Creating txt files")
            write_down_readable_file(ai_text,image.replace('.png',''))
            write_down_text_file(cleared_tags,image.replace('.png',''))
        else:
            logging.warning(f"Founded not png image, adjust! {image}")
            faulty_pics.append(image)
            continue
    if faulty_pics:
        logging.warning(f"Faulty pics: {faulty_pics}")
    if timeout_process:
        logging.warning(f"Timeout_process: {timeout_process}")
    if timeout_connect:
        logging.warning(f"Timeout connect: {timeout_connect}")
    logging.info('All images processed accordingly.')
    return
