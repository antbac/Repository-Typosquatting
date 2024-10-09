import json
from typing import List
from package import Package
import requests
import string

def get_nuget_packages(cache_to: str | None, cached_source: str | None):
    def get_nuget_packages_recursive(query, search_query_service, size=1000, threshold=4000):
        all_packages = []
        
        skip = 0
        full_query = f"?q={query}&prerelease=false&semVerLevel=2.0.0&skip={skip}&take={size}"
        response = requests.get(search_query_service + full_query)
        response.raise_for_status()
        package_data = response.json()
        
        total_hits = package_data.get('totalHits', 0)
        if total_hits > threshold:
            for next_char in string.ascii_lowercase:
                if any([next_char in previous_query for previous_query in query.split('.')]):
                    continue
                all_packages.extend(get_nuget_packages_recursive(f'{query}.{next_char}', search_query_service, size, threshold))
        else:
            while True:
                all_packages.extend([
                    {
                        "id": package['id'],
                        "downloads": package.get('totalDownloads', 0)
                    }
                    for package in package_data['data']
                ])
                
                taken = skip + size
                if taken >= total_hits or taken >= threshold:
                    break

                skip = taken
                full_query = f"?q={query}&prerelease=false&semVerLevel=2.0.0&skip={skip}&take={size}"
                response = requests.get(search_query_service + full_query)
                response.raise_for_status()
                package_data = response.json()

            print(f'Downloaded {len(all_packages)} packages with queries: {query.split(".")}')

        seen = set()
        return [item for item in all_packages if item['id'] not in seen and not seen.add(item['id'])]

    if cached_source != None:
        with open(cached_source, 'rt') as f:
            return [Package(x['name'], int(x['downloads'])) for x in json.loads(f.read())]

    base_url = "https://api.nuget.org/v3/index.json"
    
    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()
    
    search_query_service = next(
        resource['@id'] for resource in data['resources']
        if resource['@type'] == "SearchQueryService"
    )
    
    from concurrent.futures import ThreadPoolExecutor
    import threading
    all_packages = []
    lock = threading.Lock()
    def process_query(query):
        result = get_nuget_packages_recursive(query, search_query_service)
        with lock:
            all_packages.extend(result)
    
    with ThreadPoolExecutor(max_workers = len(string.ascii_lowercase)) as executor:
        executor.map(process_query, [f'{a}{b}' for a in string.ascii_lowercase for b in string.ascii_lowercase])

    seen = set()
    packages = [Package(item['id'], int(item['downloads'])) for item in all_packages if item['id'] not in seen and not seen.add(item['id'])]

    if cache_to != None:
        with open(cache_to, 'wt') as f:
            f.write(json.dumps(sorted([{'name': x.name, 'downloads': x.downloads} for x in packages], key=lambda x: x['downloads'], reverse=True)))

    return packages