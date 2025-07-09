from googleapiclient.discovery import build

def search_google(query, api_key, cse_id, num_results=20):
    service = build("customsearch", "v1", developerKey=api_key)
    results = []
    start = 1

    while len(results) < num_results:
        res = service.cse().list(q=query, cx=cse_id, start=start).execute()
        items = res.get("items", [])
        for item in items:
            results.append(item["link"])
        start += 10
        if "nextPage" not in res.get("queries", {}):
            break

    return results
