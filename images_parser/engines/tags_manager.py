import argparse
from pathlib import Path

current_dir = Path.cwd()
tags_path = current_dir / "images_parser" / 'quality_tags.txt'




def create_parser():  
    parser = argparse.ArgumentParser(
        prog="tags_manager",
        description="Manager for tags system"
    )
    parser.add_argument("-m", "--mode",
                         help="set mode of output", default="add")
    parser.add_argument("tag", default=argparse.SUPPRESS)
    return parser

def add_tag(tag):
    lines = []
    with open(tags_path,"r") as file:
        for line in file:
            lines.append(line)
    with open(tags_path,"w") as file:
        lines.append(f'{tag},\n')
        for line in lines:
            file.write(line)

    return print('done')

def delete_tag(tag):
    lines = []
    with open(tags_path,"r") as file:
        for line in file:
            lines.append(line)
    prep = tag+","
    for line in lines:
        if prep.lower() in line.lower():
            lines.remove(line)
            break
    with open(tags_path,"w") as file:
        for line in lines:
            file.write(line)
    return print('done')

def manager_engine(mode,tag):
    match mode:
        case "add":
            add_tag(tag)
            return
        case "delete":
            delete_tag(tag)
        case _:
            print("ты дурак?")