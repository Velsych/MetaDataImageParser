from functools import lru_cache
import logging
import sys
logging.basicConfig( format = u'%(filename)s# %(levelname)-8s [%(asctime)s]  %(message)s',level=logging.INFO)

@lru_cache
def get_quality_tags(quality_tags_path) -> tuple:
    tags = []
    logging.info(f'Parsing... {quality_tags_path}')
    try:
        with open(quality_tags_path,'r') as file:
            for line in file:
                if line.startswith("#"):
                    continue
                tags.append(line.strip("\n"))
    except OSError as e:
        logging.error(f'An error in parsing tags file has occured! Check it and fix it pls Error: {e}')
        logging.warning("Application can't work fully without tags, stopping application")
        sys.exit()
    finally:
        return tuple(tags)