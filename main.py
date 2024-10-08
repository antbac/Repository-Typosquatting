from analyzer import Analyzer
from repositoryloader import get_nuget_packages

if __name__ == "__main__":
    packages = get_nuget_packages()
    analyzer = Analyzer(packages, 1_000_000, 2)
    for squatter in analyzer.get_squatters():
        print(f"Package: {squatter.name}, Downloads: {squatter.downloads}")