import requests

# 🔑 Your credentials from Adzuna
APP_ID = "203ab5d1"
APP_KEY = "16313d52c5a65cdd7e4eefbf0975309b"

# Change country if needed: "in" = India, "us" = USA, "uk" = United Kingdom
COUNTRY = "in"

def fetch_jobs(query, location="India", results_per_page=5):
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        jobs = response.json().get("results", [])
        return [
            {
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "url": job.get("redirect_url")
            }
            for job in jobs
        ]
    else:
        return []
