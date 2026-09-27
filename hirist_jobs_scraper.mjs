#!/usr/bin/env node
// Node.js client for the themineworks/hirist-jobs-scraper actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/hirist-jobs-scraper/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/hirist-jobs-scraper';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['keyword'] !== undefined) runInput.keyword = String(args['keyword']);
if (args['category-slug'] !== undefined) runInput.categorySlug = String(args['category-slug']);
if (args['locations'] !== undefined) runInput.locations = String(args['locations']).split(',').map((s) => s.trim());
if (args['max-jobs'] !== undefined) runInput.maxJobs = parseInt(args['max-jobs'], 10);
if (args['include-job-description'] !== undefined) runInput.includeJobDescription = args['include-job-description'] === true || args['include-job-description'] === 'true';
if (args['experience-min-years'] !== undefined) runInput.experienceMinYears = parseInt(args['experience-min-years'], 10);
if (args['experience-max-years'] !== undefined) runInput.experienceMaxYears = parseInt(args['experience-max-years'], 10);
if (args['posted-within-days'] !== undefined) runInput.postedWithinDays = parseInt(args['posted-within-days'], 10);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
