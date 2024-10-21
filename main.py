import argparse
import asyncio
from dataclasses import dataclass

from hostsfile.generate import generate
from hostsfile.types import Command


parser = argparse.ArgumentParser(description="ldlac/hostfiles cli Usage")

parser.add_argument(
    "--command",
    "-c",
    choices=list(Command),
    default=Command.hosts,
    help="Which command to run",
)
parser.add_argument(
    "--target-ip",
    "-i",
    default="0.0.0.0",
    help="The target ip of the hosts file",
)
parser.add_argument(
    "--include-sleepers",
    "-is",
    action="store_true",
    default=False,
    help="Should include sleepers domains in the final output",
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--update", "-u", action="store_true", default=True, help="Should update sources"
)
group.add_argument(
    "--no-update",
    "-n",
    action="store_true",
    default=False,
    help="Should not update sources",
)
group.add_argument(
    "--update-sleepers",
    "-us",
    action="store_true",
    default=False,
    help="Update sources and resolve sleepers/parked domains",
)
group.add_argument(
    "--force-update-sleepers",
    "-fus",
    action="store_true",
    default=False,
    help="Update sources and force resolve sleepers/parked domains",
)


@dataclass
class Args:
    command: Command
    update: bool
    no_update: bool
    update_sleepers: bool
    force_update_sleepers: bool
    include_sleepers: bool
    target_ip: str

    def __post_init__(self):
        if self.no_update:
            self.update = False

        if self.update_sleepers:
            self.update = True

        if self.force_update_sleepers:
            self.update_sleepers = True
            self.update = True


_args = parser.parse_args()
args = Args(**_args.__dict__)


async def main():
    await generate(
        args.command,
        args.update,
        args.update_sleepers,
        args.force_update_sleepers,
        args.include_sleepers,
        args.target_ip,
    )


if __name__ == "__main__":
    asyncio.run(main())
