import argparse


def create_parser():  
    parser = argparse.ArgumentParser(
        prog="env setter",
        description="setting env"
    )
    parser.add_argument("env", default=argparse.SUPPRESS)
    return parser