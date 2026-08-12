from images_parser.main import generate_text_into_better_text,check_directiry

def main():  
    check_directiry()
    generate_text_into_better_text()
    print('Все картинки обработаны без ошибок')


if __name__ == "__main__":  
    main()