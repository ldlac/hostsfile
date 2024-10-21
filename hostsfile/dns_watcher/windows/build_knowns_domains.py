# Here is how you enable DNS logging on Windows:
# 1. Use Windows-R to open the run box on the system.
# 2. Type eventvwr.msc and tap on the Enter-key to load the Event Viewer.
# 3. Navigate the following path: Applications and Service Logs > Microsoft > Windows > DNS Client Events > Operational
# 4. Right-click on Operational, and select Enable Log.
###
# To export
# 1. Select Operational
# 2. In the right menu, Select All Events As ...
# 3. Save the file as a cvs `dns.csv`
# 4. Place the file at the root of the repository

import csv
import io
from anyio import Path

from hostsfile.update_sources.is_domain_valid import is_domain_valid


async def build_knowns_domains(dns_log_filepath: Path):
    known_domains: set[str] = set()
    async with await dns_log_filepath.open("r") as dns_log_file:
        buffer = io.StringIO()
        buffer.write(await dns_log_file.read())
        buffer.seek(0)
        reader = csv.reader(buffer, delimiter=",")

        index = 0
        for row in reader:
            if index == 0:
                assert "Level" in row[0]
                assert "Date and Time" in row[1]
                assert "Source" in row[2]
                assert "Event ID" in row[3]
                assert "Task Category" in row[4]
                index += 1
            else:
                assert "Microsoft-Windows-DNS-Client" in row[2]

            if len(row) >= 6:
                line_with_domains = row[5]
                for domain in line_with_domains.split(" "):
                    if "." in domain and is_domain_valid(domain):
                        known_domains.update([domain])
    return known_domains
