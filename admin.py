import os, time
from subprocess import run
from app import App

modules = ["serial", "pygame", "keyboard"]

class Admin:
    def __init__(self):
        self.app = None

    def module_install(self):
        try:
            for module_name in modules:
                import module_name # type: ignore
        except ModuleNotFoundError:
            if not os.path.exists("requirements.txt"):
                f = open("requirements.txt", "w")
                f.write("serial\npygame\nkeyboard\n")
            run(f"sudo python -m pip install -r requirements.txt --break-system-packages", shell=True)

    def init_app(self):
        if self.app is None: self.app = App()

    def app_run(self):
        if self.app is not None: self.app.run()

    def app_stop(self):
        if self.app is not None: self.app.stop()

if __name__ == "__main__":
    admin = Admin()
    try:
        admin.module_install()
        time.sleep(0.5)
        admin.init_app()
        while True: admin.app_run()
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print('\nProgram interrupted by user.')
        else:
            print(f"An error occurred: {e}")
    finally:
        admin.app_stop()
        