import requests
import json
import os

URL = "https://portail-portal.otc-cta.gc.ca/api/code-share-notifications-applications"

DATA_FILE = "data.json"

def fetch_data():
    r = requests.get(URL)
    r.raise_for_status()
    return r.json()

def load_old():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_new(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def find_new(old, new):
    old_ids = {item.get("id") for item in old if isinstance(item, dict)}
    return [item for item in new if item.get("id") not in old_ids]

def main():
    print("Checking CTA portal...")

    new_data = fetch_data()
    old_data = load_old()

    new_items = find_new(old_data, new_data)

    if new_items:
        print(f"Found {len(new_items)} new applications!")

        for item in new_items:
            print(json.dumps(item, indent=2))

    else:
        print("No new applications.")

    save_new(new_data)

if __name__ == "__main__":
    main()
    