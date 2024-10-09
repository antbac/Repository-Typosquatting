class Package:

    name: str
    downloads: int

    def __init__(self, name: str, downloads: int):
        self.name = name
        self.downloads = downloads
    
    def __str__(self) -> str:
        import json
        return json.dumps({'name': self.name, 'downloads': self.downloads})
