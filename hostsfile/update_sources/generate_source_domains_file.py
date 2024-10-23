import anyio

from hostsfile.update_sources.is_domain_valid import is_domain_valid


async def generate_source_domains_file(
    domains_source_file: anyio.Path, source_hosts_content: bytes
) -> list[str]:
    domains: list[str] = []

    async with await domains_source_file.open("+w") as domains_file:
        await domains_file.truncate()

        for line in source_hosts_content.decode().splitlines():
            try:
                if not line.startswith("#") and line:
                    if "#" in line:
                        new_line = f"{line.split('#')[0]}\n"
                    else:
                        new_line: str = f"{line}\n"

                    new_line = new_line.replace("\t", " ")
                    if " " in new_line:
                        domain = new_line.split(" ")[1].rstrip()
                    elif new_line.startswith("||"):
                        domain = new_line.split("||")[1].split("^")[0].rstrip()
                    else:
                        domain = new_line.rstrip()
                    if is_domain_valid(domain):
                        await domains_file.write(f"{domain}\n")
                        domains.append(domain)
            except IndexError:
                print(f"error while parsing line {line}")
                raise

    return domains
