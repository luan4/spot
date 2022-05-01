import sys
import json

from manager import Manager

def main():
    with open(sys.argv[1], 'r') as f:
        config = json.load(f)
    manager = Manager(**config)
    manager.run()


if __name__ == '__main__':
    main()
