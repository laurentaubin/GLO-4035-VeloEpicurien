class ReadMeResource:
    def __init__(self, readme_path: str) -> None:
        self.__readme_path = readme_path

    def get_readme(self) -> str:
        with open(self.__readme_path, "r") as readme:
            return readme.read()
