
from cli import main_menu
from settings import logger


@logger.catch()
def main():
    main_menu()


if __name__ == '__main__':
    main()
