# Release History

## Unreleased

- 105 Job applications (back-end work only)
- 109 Job alert subscription
- 110 Job search alert notifications
- 111 Job alert unsubscribe
- 129 Jobs postcode search
- 133 Search by job number

## 5.0 (2020-03-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/4.0...5.0

- Enable FormPages
- Add Yandex and Bing verification strings

## 4.0 (2020-02-24)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/3.2...4.0

- Update deployment documentation
- 59 Jobs homepage
- 62 Jobs detail page
- 85 TalentLink API client, and importer commands
- 90 Jobs Category and homepage categories listing
- 92 Recruitment index page
- 94 Jobs import HTML formatting improvements
- 96 Jobs search: add category filter
- 99 Add slugs to job category
- 104 Add job subcategory

## 3.2 (2020-02-17)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/3.1...3.2

- 116 Enable StreamField Table Block
- 118 Add border to search inputs

## 3.1 (2020-02-10)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/3.0...3.1

- 82 Adjust header logo size

## 3.0 (2020-02-10)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/2.1...3.0

- Django 2.2.10
- Hotfix: Pin Redis version in requirements.txt
- Update CI pipeline stage names and order to make progress clearer
- 83 Specify border radius on inputs
- 87 Remove flag from external links
- 88 Updated IndexPage to allow it to be created under IndexPage
- Fix: Update "Home" breadcrumb link target to work with multiple sites

## 2.1 (2020-01-22)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/2.0...2.1

Temporary changes for launch

- Remove email signup form
- Remove cookie banner

## 2.0 (2020-01-21)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/1.1...2.0

- 26 Add GOV.UK Notify email backend
- 79 Redirect-to field on all pages
- 66 Update Call to Action snippet to support multiple links
- 47 Search results to display local area links where applicable
- 67 Enabled News and Events apps. Add latest news and events to homepage.
- 76 Homepage temporary banner
- 86 Amend Local Area Links postscript default text
- 84 Site wide alpha banner
- 43, 71 Inline Index page

## 1.1 (2019-12-19)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/1.0...1.1

- Django 2.2.9 security release

## 1.0 (2019-12-18)

https://git.torchbox.com/buckinghamshire-council/bc/-/tags/1.0

- 7, 27 IndexPage
  - Added child_pages, featured_pages and ordinary_pages properties
  - Updated page context and template to remove paginator and to use above properties
  - Added unit tests
- Added automatic secret detection to pre-commit hooks
- 9 Homepage hero and homepage unit tests
- 10 Information page
  - Make H2 available as a block only, not in RichTextBlocks
  - Limit rich text features
  - Local Area Links block
- 21 disable events, news, people, and forms apps as we are not using them yet.
