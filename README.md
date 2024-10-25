# bpscraper

Scrapes baseball prospectus for injury data, requires csv from https://legacy.baseballprospectus.com/sortable/playerid_list.php for player ids. Creates new csvs with each one containing the number of injuries for a certain body part. I set it to wait 8 seconds in between requests, you might be able to squeeze out more, but I didn't go any further. Uses playwright-python to scrape the site, you will need to install it to use this program.
