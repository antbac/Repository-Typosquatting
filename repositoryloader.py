import requests
from typing import List
from package import Package

def get_nuget_packages():
    base_url = "https://api.nuget.org/v3/index.json"
    
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()
    
    search_query_service = next(
        resource['@id'] for resource in data['resources']
        if resource['@type'] == "SearchQueryService"
    )
    
    packages: List[Package] = []
    page_size = 1000
    page: int = 0
    number_of_packages_left: int = 9999
    while number_of_packages_left > 0:
        query = f"?q=&prerelease=false&semVerLevel=2.0.0&skip={str(page * page_size)}&take={str(page_size)}"
        
        response = requests.get(search_query_service + query)
        response.raise_for_status()
        package_data = response.json()
        
        for package in package_data['data']:
            packages.append(Package(str(package['id']), int(package['totalDownloads'])))
        
        number_of_packages_left = package_data['totalHits'] - page_size * (page + 1)
        page += 1

    return packages