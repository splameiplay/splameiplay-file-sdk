
Hey there! This file is so you know what you expect when you contribute towards this project and what you should and shouldn't do. It's a bit long but hopefully self-explanatory

## DCO Sign off

When making a commit, they must be signed off and agree to our DCO (you can find it in the `DCO.md` file) otherwise your Pull/Merge Request will be rejected. You can do this by appending `-s` when making commits using the command line, or enabling the `Always sign off` setting in VSCode or other IDEs. If you forget to sign off your commits, you can still sign them off by rebasing your commits with the `--signoff` argument and reopening your Pull/Merge request or re-requesting a review.

## Licence agreement

All contributions made towards this project will be licenced under the Apache License 2.0. You agree that you have the rights to licence your code under this licence as mentioned within the DCO (found in `DCO.md` and mentioned above). Please don't contribute if you do not wish to agree with the DCO!

## Code of Conduct

When contributing, whether that be issues, Pull/Merge Requests or other means of contributing, you agree to our Code of Conduct which can be read in the `CODE_OF_CONDUCT.md` file.

## Trademark and copyright notice

Remember that contributing to this project does **not grant you trademark rights or copyright** for use of any kind such as logos, names, brands, or identities for use in your own products. More information can be found in the ending of the `README.md` file with the heading 'Branding Rights'

## AI Usage

You can use Generative Artificial Intelligence (GenAI) to assist with your contributions but it'll need to follow these rules:

- The GenAI tool used within the contribution (regardless of how it was used) must be disclosed:
  - Within the commits it was used in via a Co-authored-by commit message tag if the AI has a dedicated GitHub account, otherwise just 'Modified/Assisted by <AI_NAME> (AI)' at the end of the commit message
  - And a 'Modified/Assisted by <AI_NAME> (AI)' message at the end of your Pull/Merge Request
- Contributions that count as GenAI Made are not allowed, regardless of how it was handled
- Contributions that count as GenAI Modified may be allowed, but are genuinely not permitted
- Contributions can only use GenAI for sample data, testing or coding. Other uses, like generating images or videos, are not allowed

We may reject contributions even when they follow all these rules, simply because AI is constantly evolving so we can't always update these rules in time. We'll always let you know why a contribution was rejected.

The terms Modified, Assisted and Made follow the definitions set by SplameiPlay's AI documentation - [https://docs.veemo.uk/splameiplay/ai-disclosures/](https://docs.veemo.uk/splameiplay/ai-disclosures/)

## PR Requests

When making a Pull/Merge Request, you should always request a merge to the `main` branch, you'll also need at least one maintainer to review your request before merging. If your merge gets rejected, but the request stays open, feel free to make any changes asked to be made then request for another review.

## Protected branches

Please only make Pull/Merge Requests to `main` branch as the other branches each serve their own purposes:

- `release/x.x.x` - Used for storing changes for a specific release (i.e. 1.2.3)
  - Sometimes ` - lts` is added to the end for long term support versions

## Coding conventions

Please keep the coding conventions used be the C# Microsoft Code Convention (you can use camelCase for function names!) or the conventions used for that specific programming language

# Thank you for you interest towards this project and helping it grow!
