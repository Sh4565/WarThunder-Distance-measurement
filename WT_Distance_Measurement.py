
import gettext

from src.utils.path_setup import setup_paths


gettext.bindtextdomain('messages', 'locales')
gettext.textdomain('messages')
_ = gettext.gettext


def main():
    import cli
    import settings

    print(_('heloo'))
    @settings.logger.catch()
    def run():
        cli.main_menu()

    run()


if __name__ == '__main__':
    setup_paths()
    main()
