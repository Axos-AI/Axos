# app.py
from src.main import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--chat', action='store_true', help='Run the chat interface')
    parser.add_argument("-r", '--refactor', action='store_true', help='Run the refactoring AI')
    parser.add_argument("-e", '--entry_point', type=str, help='The entry point file to start the refactoring from the root of the repository.')
    args = parser.parse_args()
    if args.entry_point:
        args.refactor = True
    if not args.entry_point and args.refactor:
        print("Please provide an entry point file to start the refactoring.")
        exit()
    if not args.chat and not args.refactor:
        args.chat = True
    main(args.chat, args.refactor)





