from package import Package
from typing import List

class Analyzer:
    
    packages: List[Package]
    legitimacy_minimum_downloads: int
    required_similarity: int
    
    def __init__(self, packages: List[Package], legitimacy_minimum_downloads: int, required_similarity: int):
        self.packages = packages
        self.legitimacy_minimum_downloads = legitimacy_minimum_downloads
        self.required_similarity = required_similarity
    
    def get_squatters(self):
        automatically_legit_packages = list(filter(lambda x: x.downloads >= self.legitimacy_minimum_downloads, self.packages))
        packages_to_evaluate = list(filter(lambda x: x.downloads < self.legitimacy_minimum_downloads, self.packages))

        potential_squatters: List[Package] = []
        for package_to_evaluate in packages_to_evaluate:
            for legit_package in automatically_legit_packages:
                if self.__is_within_edit_distance(package_to_evaluate, legit_package):
                    potential_squatters.append(package_to_evaluate)
                    break
        
        return potential_squatters

    def __is_within_edit_distance(self, package1: Package, package2: Package):
        m, k = len(package1.name), len(package2.name)

        if abs(m - k) > self.required_similarity:
            return False
        
        previous_row = list(range(k + 1))
        for i in range(1, m + 1):
            current_row = [i] + [0] * k
            min_in_row = float('inf')
            for j in range(1, k + 1):
                if package1.name[i - 1] == package2.name[j - 1]:
                    current_row[j] = previous_row[j - 1]
                else:
                    current_row[j] = min(
                        previous_row[j],
                        current_row[j - 1],
                        previous_row[j - 1]
                    ) + 1
                min_in_row = min(min_in_row, current_row[j])
            
            if min_in_row > self.required_similarity:
                return False
            
            previous_row = current_row
        
        return previous_row[-1] <= self.required_similarity