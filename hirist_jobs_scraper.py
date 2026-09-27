#!/usr/bin/env python3
"""India IT jobs across 147 locations, 19 fields. Python, Node.js and cURL clients for the Hirist Jobs Scraper on Apify, pay per result.

Command-line client for the themineworks/hirist-jobs-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/hirist-jobs-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/hirist-jobs-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--keyword", help="Free-text job search, for example 'java developer' or 'react native'")
    ap.add_argument("--category-slug", help="Browse a Hirist job category")
    ap.add_argument("--locations", help="Comma-separated. City, state or country names to filter by, for example 'Bangalore', 'Hyderabad', 'Remote'")
    ap.add_argument("--max-jobs", type=int, help="Maximum jobs to return across all pages")
    ap.add_argument("--include-job-description", action=argparse.BooleanOptionalAction, help="Fetch the full HTML job description for every job (one extra request per job, slower and…")
    ap.add_argument("--experience-min-years", type=int, help="Only return jobs whose experience band overlaps this minimum")
    ap.add_argument("--experience-max-years", type=int, help="Only return jobs whose experience band overlaps this maximum")
    ap.add_argument("--posted-within-days", type=int, help="Only return jobs posted within the last N days")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.keyword is not None: run_input["keyword"] = a.keyword
    if a.category_slug is not None: run_input["categorySlug"] = a.category_slug
    if a.locations: run_input["locations"] = [s.strip() for s in a.locations.split(",") if s.strip()]
    if a.max_jobs is not None: run_input["maxJobs"] = a.max_jobs
    if a.include_job_description is not None: run_input["includeJobDescription"] = a.include_job_description
    if a.experience_min_years is not None: run_input["experienceMinYears"] = a.experience_min_years
    if a.experience_max_years is not None: run_input["experienceMaxYears"] = a.experience_max_years
    if a.posted_within_days is not None: run_input["postedWithinDays"] = a.posted_within_days

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
