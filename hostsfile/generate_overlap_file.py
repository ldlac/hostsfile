from anyio import Path


async def generate_overlap_file():
    groups: dict[str, set[str]] = {}
    sources_dir = Path("sources")
    async for dir in sources_dir.iterdir():
        domains_source_file = dir.joinpath("domains")
        if await domains_source_file.exists():
            async with await domains_source_file.open() as file:
                group_domains = (await file.read()).splitlines()
                groups[dir.name] = set(group_domains)

    for iname, idomains in groups.items():
        for jname, jdomains in groups.items():
            if iname != jname:
                ratio = len(idomains.intersection(jdomains)) / len(idomains)
                if ratio > 0.10:
                    print(f"{iname} vs {jname} | {ratio:.0%}")
