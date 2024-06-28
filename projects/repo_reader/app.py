# app.py
from src.main import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--chat', action='store_true', help='Run the chat interface')
    parser.add_argument("-r", '--refactor', action='store_true', help='Run the refactoring AI')
    args = parser.parse_args()
    if not args.chat and not args.refactor:
        args.chat = True
    main(args.chat, args.refactor)





