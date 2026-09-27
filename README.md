# Hirist Jobs Scraper: India Tech Roles & Salary

Scrape Hirist.tech IT job listings by keyword, category, location, and experience: title, company, salary, skills array, and live AmbitionBox rating per employer. No login, no cookies. Reads Hirist's own public JSON API directly.

**Run it on Apify:** [apify.com/themineworks/hirist-jobs-scraper](https://apify.com/themineworks/hirist-jobs-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/hirist-jobs-scraper](https://themineworks.com/actors/hirist-jobs-scraper/)

**Price:** $5.00 per 1,000 jobs on Apify's free plan, down to $3.00 on higher plans, plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Keyword search or browse across 12 tech categories
* 147 India + Gulf locations resolved from plain city names
* Live AmbitionBox company rating and review count per job
* Skills returned as a structured array, not free text
* No login, no browser. Reads Hirist's own JSON API

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/hirist-jobs-scraper").call(run_input={
    "keyword": "java developer",
    "categorySlug": "backend-development-jobs",
    "locations": [
        "Bangalore"
    ],
    "maxJobs": 10
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/hirist-jobs-scraper').call({
    "keyword": "java developer",
    "categorySlug": "backend-development-jobs",
    "locations": [
        "Bangalore"
    ],
    "maxJobs": 10
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~hirist-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "java developer", "categorySlug": "backend-development-jobs", "locations": ["Bangalore"], "maxJobs": 10}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 hirist_jobs_scraper.py --token YOUR_APIFY_TOKEN --keyword "java developer" --category-slug "backend-development-jobs" --locations "Bangalore" --max-jobs "10"
node hirist_jobs_scraper.mjs --token YOUR_APIFY_TOKEN --keyword "java developer" --category-slug "backend-development-jobs" --locations "Bangalore" --max-jobs "10"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `keyword` | string |  | Free-text job search, for example 'java developer' or 'react native' |
| `categorySlug` | string | `""` | Browse a Hirist job category |
| `locations` | array |  | City, state or country names to filter by, for example 'Bangalore', 'Hyderabad', 'Remote' |
| `maxJobs` | integer | `30` | Maximum jobs to return across all pages |
| `includeJobDescription` | boolean | `false` | Fetch the full HTML job description for every job (one extra request per job, slower and costs more compute… |
| `experienceMinYears` | integer |  | Only return jobs whose experience band overlaps this minimum |
| `experienceMaxYears` | integer |  | Only return jobs whose experience band overlaps this maximum |
| `postedWithinDays` | integer |  | Only return jobs posted within the last N days |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `job_id` | string |  |
| `title` | string |  |
| `company` | string |  |
| `company_rating` | number |  |
| `locations` | array |  |
| `remote` | boolean |  |
| `skills` | array |  |
| `experience_min_years` | integer |  |
| `experience_max_years` | integer |  |
| `salary_min_lpa` | number |  |
| `salary_max_lpa` | number |  |
| `apply_count` | integer |  |
| `posted_at` | string |  |
| `url` | string |  |
| `scraped_at` | string |  |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/hirist-jobs-scraper
```

## FAQ

### Is this scraping HTML?

No. It calls the same public JSON API (gladiator.hirist.tech) the site's own React front end calls. No browser needed.

### Does Hirist require login to see this data?

No. Hirist's job search results and listing pages are fully public. A separate, personalised "my job feed" does require login; this actor doesn't use it.

### Can I search by keyword AND category AND location at once?

Yes. All three combine in a single request, layered with experience range and posted-within-days recency.

### Is salary always present?

No. Many listings hide it. When hidden, the salary fields are simply absent rather than shown as zero.

### What does it cost?

Pay per event: one job-scraped event per delivered record, charged only after validation. Empty results and duplicates are never charged.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON
* [Shine.com Jobs Scraper](https://themineworks.com/actors/shine-jobs-scraper/): Times Group India job board, 22 fields, monitor mode

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
