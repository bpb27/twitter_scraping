## Twitter Scraper

Twitter makes it hard to get all of a user's tweets (assuming they have more than 3200). This is a way to get around that.

## Requirements

- basic knowledge on how to use a terminal
- python3
  - to check, in your terminal, enter `python3`
  - if you don't have it, check YouTube for installation instructions
- pip or pip3
  - to check, in your terminal, enter `pip` or `pip3`
  - if you don't have it, again, check YouTube for installation instructions
- selenium (3.0.1)
  - `pip3 install selenium`

## Running the scraper

- open up scrape.py and edit the user, start, and end variables (and save the file)
- run `python scrape.py`
- you'll see a browser pop up and output in the terminal
- do some fun other task until it finishes
- once it's done, it outputs all the tweet ids it found into `all_ids.json`

## Troubleshooting the scraper

- do you get a `no such file` error? you need to cd to the directory of the file
- do you get a driver error when you try and run the script?
  - open `scrape.py` and change the driver to use Chrome() or Firefox()
    - if neither work, google the error (you probably need to install a new driver)
    
## Getting the metadata

- first you'll need to get twitter API keys
  - sign up for a developer account here https://dev.twitter.com/
  - get your keys here: https://apps.twitter.com/
- fill in your keys into the `sample_api_keys.json` file
- change the name to `api_keys.json`
- run `python3 get_metadata.py`
- this will get metadata for every tweet id in `all_ids.json` and output it to `master_metadata_file.json`

## Slim down your metadata
- there's a lot of unnessary info in the metadata, so you can take this optional step to slim it down
- run `python3 minimize_metadata.py`
- you'll now have a much smaller file with `refined_master_file.json`
