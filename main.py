from analyzer import Analyzer
from repositoryloader import get_nuget_packages
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--cache", type=str, help="Specify cache value.")
    group.add_argument("--cached", type=str, help="Specify cached value.")
    parser.add_argument("--output", type=str, help="Specify output file to write the result.")

    args = parser.parse_args()

    packages = get_nuget_packages(args.cache, args.cached)
    analyzer = Analyzer(packages, 1_000_000, 2)
    squatters = analyzer.get_squatters()
    if args.output != None:
        with open(args.output, 'wt') as f:
            f.writelines([f"Package: {squatter.name}, Downloads: {squatter.downloads}" for squatter in squatters])
    else:
        for squatter in squatters:
            print(f"Package: {squatter.name}, Downloads: {squatter.downloads}")