# legal_resource_scanner.py

import requests
from geopy.distance import geodesic
from semptify_core import get_user_location, store_results, render_gui_list

SEARCH_RADIUS_MILES = 250
RESOURCE_KEYWORDS = [
    "tenant legal aid", "housing court help", "eviction defense",
    "renters rights", "low-income legal services", "tenant advocacy"
]

def scan_legal_resources():
    user_location = get_user_location()  # e.g., ("Eagan, MN", (44.833, -93.166))
    results = []

    for keyword in RESOURCE_KEYWORDS:
        query = f"{keyword} near {user_location[0]}"
        response = requests.get("https://api.searchengine.com/search", params={"q": query})
        for item in response.json().get("results", []):
            place_coords = item.get("coordinates")
            if place_coords:
                distance = geodesic(user_location[1], place_coords).miles
                if distance <= SEARCH_RADIUS_MILES:
                    results.append({
                        "name": item["title"],
                        "link": item["url"],
                        "distance": round(distance, 1),
                        "summary": item.get("snippet", "")
                    })

    store_results("legal_resources", results)
    return render_gui_list(results, title="Legal Aid Near You")


# Optional: GUI button wiring
HELP_POPUP_TEXT = "Use this tool to find legal aid and tenant advocacy resources near you. Click the button, review the list, and follow the links for more info."

def register_module():
    return {
        "button_label": "Find Legal Help Near Me",
        "action": scan_legal_resources,
        "category": "Library",
        "help_file": "legal_resource_scanner_help.txt",
        "help_popup": HELP_POPUP_TEXT
    }
