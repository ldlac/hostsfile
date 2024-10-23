from anyio import Path


async def generate_diff_file():
    groups: dict[str, set[str]] = {}
    sources_dir = Path("sources")
    async for dir in sources_dir.iterdir():
        domains_source_file = dir.joinpath("domains")
        if await domains_source_file.exists():
            async with await domains_source_file.open() as file:
                group_domains = (await file.read()).splitlines()
                groups[dir.name] = set(group_domains)

    for iname, idomains in groups.items():
        unique_domains = idomains
        for jname, jdomains in groups.items():
            if iname != jname:
                unique_domains.difference_update(jdomains)

        sources_dir = Path(f"sources/{iname}")
        diff_source_file = sources_dir.joinpath("diff")
        async with await diff_source_file.open("w+") as diff_file:
            await diff_file.truncate()

            for domain in unique_domains:
                await diff_file.write(f"{domain}\n")
