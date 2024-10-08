class Package:

    name: str
    downloads: int

    def __init__(self, name: str, downloads: int):
        self.name = name
        self.downloads = downloads
