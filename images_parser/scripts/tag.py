from images_parser.engines.tags_manager import create_parser,manager_engine

def main():  
    parser = create_parser()
    args = parser.parse_args()
    manager_engine(args.mode,args.tag)

if __name__ == "__main__":  
    main()