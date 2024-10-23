import anyio
import dns.resolver
import dns.asyncresolver

NAMESERVERS = ["1.1.1.1", "1.0.0.1"]


async def try_resolve_domain(
    semaphore: anyio.Semaphore, file: anyio.AsyncFile[str], domain: str
):
    async with semaphore:
        try:
            resolver = dns.asyncresolver.Resolver()
            resolver.nameservers = NAMESERVERS
            result = await resolver.resolve(domain, "A", raise_on_no_answer=False)
            if len(result) > 0:
                return

            result = await resolver.resolve(domain, "AAAA", raise_on_no_answer=False)
            if len(result) > 0:
                return

            result = await resolver.resolve(domain, "CNAME", raise_on_no_answer=False)
            if len(result) > 0:
                return

            result = await resolver.resolve(domain, "NS", raise_on_no_answer=False)
            ns_records = [str(r) for r in result]
            if any("parking" in ns.lower() for ns in ns_records):
                await file.write(f"{domain} PARKED\n")
        except (dns.resolver.NoNameservers, dns.resolver.LifetimeTimeout):
            pass
        except dns.resolver.NXDOMAIN:
            await file.write(f"{domain} NXDOMAIN\n")
