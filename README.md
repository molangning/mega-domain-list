# mega-domain-list
Tracks domain lists from various sources and extract useful information from them.

The subdomain list can be used for subdomain enumeration, but it has not been optimised for efficiency,

## Wordlists
[Domain list (split, with subdomains)](lists/domains/split/domains/)
[Domain list (split, without subdomains)](lists/domains/split/domains-without-subdomains/)
[Subdomain list](lists/domains/subdomains.txt)
[Tld all levels (json)](lists/tlds/tld-all-levels.json)

## Tracked list

### Domain list

- [x] http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
- [x] https://downloads.majestic.com/majestic_million.csv
- [x] https://www.domcop.com/files/top/top10milliondomains.csv.zip
- [x] https://builtwith.com/top-sites
- [x] https://tranco-list.eu/
- [ ] https://radar.cloudflare.com/domains (STILL needs api key)
- [ ] https://statvoo.com/dl/top-1million-sites.csv.zip (Broken?)

### TLD list

- [x] https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat
- [x] http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-TLD.csv.zip