from images_parser.engines.main import generate_text_into_better_text,check_directiries

def main():  
    check_directiries()
    generate_text_into_better_text()
    print('Все картинки обработаны без ошибок')


if __name__ == "__main__":  
    main()