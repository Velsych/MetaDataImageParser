from images_parser.engines.setter_args import create_parser
from images_parser.tools.dotenv_setter import set_env




def main():  
    parser = create_parser()
    args = parser.parse_args()
    set_env(args.env)

if __name__ == "__main__":  
    main()