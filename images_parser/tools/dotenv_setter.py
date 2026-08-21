import pathlib

current_dir = pathlib.Path.cwd()
main_file = current_dir / "images_parser" / "engines" / "main.py"


def set_env(envpath):
    lines = []
    with open(main_file,'r') as file:
        for line in file:
            lines.append(line)
    for i,lane in enumerate(lines):
        if 'load_dotenv(dotenv_path="")' in lane:
            env = pathlib.Path(envpath)
            lines[i] = f'load_dotenv(dotenv_path="{env}")'
            break
    with open(main_file,'w') as file:
        for line in lines:
            file.write(line)
    return