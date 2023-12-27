from lxml import html
import requests

# Base URL is hardcoded
base_url = 'https://www.srrdb.com/release/details/'

# Get base part of the episode identifier from user
base_identifier = input("Please enter the base part of the episode identifier: ").strip()

# Get season number from user
season_number = input("Please enter the season number: ").strip()

# Get episode range from user
episode_start = int(input("Please enter the start of the episode range: ").strip())
episode_end = int(input("Please enter the end of the episode range: ").strip())

# Get suffix from user
suffix = input("Please enter the suffix of the episode identifier: ").strip()

# Construct the identifiers
identifiers = [f"{base_identifier}S{season_number.zfill(2)}E{str(i).zfill(2)}.{suffix}" for i in range(episode_start, episode_end+1)]

# Construct the URLs
urls = [f"{base_url}{identifier}" for identifier in identifiers]

# Open the file in write mode
with open('Verify.sfv', 'w') as f:
    for url in urls:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        crc32 = tree.xpath('//div/table/tbody/tr[4]/td[2]/table/tbody/tr/td[3][@class=\"release-crc\"]/text()')
        name = tree.xpath('//table/tbody/tr/td[1][@title=\"2098-01-01 12:00:00\"]/text()')
        
        # Strip the \r and \n characters from the output
        crc32 = [s.strip() for s in crc32 if s.strip()]
        name = [s.strip() for s in name if s.strip()]
        
        # Join the elements of each list into a string
        crc32_str = ' '.join(crc32)
        name_str = ' '.join(name)
        
        # Write the output to the file
        f.write(f"{name_str} {crc32_str}\n")
