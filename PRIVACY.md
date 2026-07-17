# Privacy

Nightshift Foundry is designed as a static, low-data website and an inspectable
plugin repository.

## The website

The project does not use analytics, advertising, tracking pixels, cookies,
remote fonts, third-party scripts, browser storage, accounts, or forms. Choosing
a coding-agent host is in-memory page state and disappears when the page closes.
The page refreshes its public catalog from same-origin `data.json`; it makes no
cross-origin request until you choose to follow an external link.

The site is hosted on GitHub Pages. GitHub necessarily receives ordinary web
request information such as an IP address and user agent under
[GitHub's Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
Nightshift Foundry does not receive or retain a copy of Pages access logs.

## Downloads and plugins

Plugin ZIPs are static, same-origin downloads. The Foundry does not learn which
host or plugin you choose. Shipped hooks make no network calls and receive no
Foundry credential. Your coding-agent host may process plugin behavior under its
own privacy policy and permission model.

## Public contributions

Issues, pull requests, votes, and commission requests are public GitHub content.
Do not include secrets, private code, customer data, or unnecessary personal
information. Report sensitive security matters through
[GitHub's private vulnerability channel](https://github.com/GhostlyGawd/plugin-foundry/security/advisories/new).

## Changes

Any future analytics, account, form, remote asset, network-enabled plugin, or
material data collection requires an explicit reviewed change to this policy
and a prominent disclosure before activation.

Last updated: 2026-07-17.
