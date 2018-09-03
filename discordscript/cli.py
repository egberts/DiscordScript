import argparse
from discordscript import Client


def main():
    argparser = argparse.ArgumentParser(description="Run a DiscordScript file")
    argparser.add_argument("file", metavar="file", type=argparse.FileType('r'),
                           help="The file to execute")

    args = argparser.parse_args()
    client = Client(args.file)
    client.listen()

if __name__ == '__main__':
    main()