# hostsfile

This repository provides a powerful and customizable hosts file aimed at improving your browsing experience and security.
Unlike conventional hosts files, this project uniquely focuses on filtering out sleepers and parked domains, which are often used to bloat hosts files.

By analyzing DNS traffic, this solution identifies unnecessary domains, helping you create a tailored hosts file that minimizes the number of entries without compromising effectiveness.
Whether you're looking to block ads, trackers, or simply clean up your network traffic, this approach ensures that your hosts file remains optimized and relevant.

This repository combines multiple trusted hosts files into a single, unified file, ensuring that duplicates are eliminated.

## Aiming at

I agree with the maintainer of https://oisd.nl/ that the hosts/domains syntax is insufficient. I’m currently experimenting with CoreDNS to explore alternatives.

## Sources

Updated `hosts` files from the following sources are always unified and
included:

| Source          | Homepage                                                  | License                         |
| --------------- | --------------------------------------------------------- | ------------------------------- |
| AdAway          | [link](https://adaway.org/)                               | CC BY 3.0                       |
| add.2o7Net      | [link](https://github.com/FadeMind/hosts.extras)          | MIT                             |
| add.Dead        | [link](https://github.com/FadeMind/hosts.extras)          | MIT                             |
| add.Risk        | [link](https://github.com/FadeMind/hosts.extras)          | MIT                             |
| add.Spam        | [link](https://github.com/FadeMind/hosts.extras)          | MIT                             |
| Badd Boyz Hosts | [link](https://github.com/mitchellkrogza/Badd-Boyz-Hosts) | MIT                             |
| hostsVN         | [link](https://github.com/bigdargon/hostsVN)              | MIT                             |
| mvps            | [link](https://winhelp2002.mvps.org/)                     | CC BY-NC-SA 4.0                 |
| oisd            | [link](https://oisd.nl/)                                  |                                 |
| someonewhocares | [link](https://someonewhocares.org/hosts/)                | non-commercial with attribution |
| StevenBlack     | [link](https://github.com/StevenBlack/hosts/)             | MIT                             |
| tiuxo           | [link](https://github.com/tiuxo/hosts)                    | CC BY 4.0                       |
| UncheckyAds     | [link](https://github.com/FadeMind/hosts.extras)          | MIT                             |
| URLHaus         | [link](https://urlhaus.abuse.ch/)                         | CC0                             |
| yoyo            | [link](https://pgl.yoyo.org/adservers/)                   |                                 |

## Command line options

`--command <mode>` or `-c <mode>`

      The 3 possible file outputs, `hosts` is the default one.

      - `hosts` An hosts file, an unified hosts file
      - `domains` A domains file, an unified list of domains
      - `custom_hosts` A custom hosts file, an unified hosts file based on your dns traffic
      - `diff` Generates a list of the unique domains that the source has compared to others

`--target-ip <ip>` or `-i <ip>`

      the IP address to use as the target. The default is set to 0.0.0.0.

      We recommend using 0.0.0.0 instead of 127.0.0.1.
      Traditionally, most hosts files use 127.0.0.1, the loopback address, to route traffic back to the local machine.
      However, we prefer 0.0.0.0, which is a non-routable meta-address that indicates an invalid or non-existent target.
      Using 0.0.0.0 is generally faster, likely because it avoids the delay caused by timeout resolution. Additionally, it won’t interfere with any web server that may be running on your local machine.

`--include-sleepers` or `-is`

      If you want to keep the domains flagged as sleepers/parked. The default is set to False.

`--update` or `-u`

      If you want to update all domains sources. The default is set to True.

`--no-update` or `-n`

      If you don't want to update all domains sources. The default is set to False.

`--update-sleepers` or `-us`

      If you want to update the sleepers domains source list, it will only refresh the sleepers list for new domains. The default is set to False.

`--force-update-sleepers` or `-fus`

      If you want to force an update of the sleepers domains source list, it will refresh the sleepers list from all sources. The default is set to False.
