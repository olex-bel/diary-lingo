from config.loader import load_config
from application import Application


def main():
    config = load_config('config.toml')
    app = Application(config=config)
    app.mainloop()

if __name__ == "__main__":
    main()
