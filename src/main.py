
import cli
import settings


def main():
    @settings.logger.catch()
    def run():
        cli.main_menu()

    run()


if __name__ == '__main__':
    main()
