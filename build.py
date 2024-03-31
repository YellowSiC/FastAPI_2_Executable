import importlib
import pathlib
import sys


class BuildEXE:
    def __init__(self, executable_name: str, app_path: str, output_dir: str):
        self.app_path = pathlib.Path(app_path)
        self.app_name = self.app_path.stem
        self.workdir = pathlib.Path(output_dir).absolute()
        self.workdir.mkdir(exist_ok=True)
        self.pyinstallercommands = []
        self.uvicorn_packages = [
            "uvicorn.lifespan.off",
            "uvicorn.lifespan.on",
            "uvicorn.lifespan",
            "uvicorn.protocols.websockets.auto",
            "uvicorn.protocols.websockets.wsproto_impl",
            "uvicorn.protocols.websockets.websockets_impl",
            "uvicorn.protocols.http.auto",
            "uvicorn.protocols.http.h11_impl",
            "uvicorn.protocols.http.httptools_impl",
            "uvicorn.protocols.websockets",
            "uvicorn.protocols.http",
            "uvicorn.protocols",
            "uvicorn.loops.auto",
            "uvicorn.loops.asyncio",
            "uvicorn.loops.uvloop",
            "uvicorn.loops",
            "uvicorn.logging",
            "aap.server.log",
            "app",
        ]
        self.executable = executable_name

    def add_hiddenimports(self, package):
        self.pyinstallercommands.append(f"--hidden-import={package}")

    def add_data(self, folder_name):
        app_dir = self.workdir / str(folder_name)
        self.pyinstallercommands.append(
            f"--add-data={app_dir.parent.parent}\\{folder_name};{folder_name}"
        )

    def set_icon(self, icon_name):
        icon_dir = self.workdir / str(icon_name)
        self.pyinstallercommands.append(f"--icon={icon_dir.parent.parent}\\{icon_name}")

    def run_build(self):
        import PyInstaller.__main__

        for package in self.uvicorn_packages:
            self.pyinstallercommands.append(f"--hidden-import={package}")
        args = [
            str(self.app_path),
            "--distpath",
            str(self.workdir / "dist"),
            f"--name={self.executable}",
            "--onefile",
            "--windowed",
        ]

        sys.path.insert(0, str(self.workdir))
        module_path = ".".join(
            list(reversed([x.stem for x in self.app_path.parents if x.stem]))
            + [self.app_path.stem]
        )
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            print(f"No module found with this name: {e}")
            pass
        PyInstaller.__main__.run(args + self.pyinstallercommands)




config = BuildEXE("server", "main.py", "build")
config.add_data("app")
config.add_data("static")
config.add_data("templates")
config.set_icon("logo.ico")
config.run_build()
