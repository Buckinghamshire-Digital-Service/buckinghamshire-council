# Release History

## Unreleased

- Add tests for job categories import fix
- Add unit tests for Aptean Respond integration
- Subheading block (BE)

## 14.0 (2020-04-22)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/13.0...14.0

- 135 Employer logos (BE)
- 176 Jobs fix import location
- 204 Jobs fix salary imports (BE)

## 13.0 (2020-04-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/12.0...13.0

- Upgrade Wagtail to 2.7.2 and Django to 2.2.12
- Add documentation about Aptean Respond cases backend, and cookies
- Make the separate forms on the jobs search page cooperate
- Styling tweaks on recruitment index page ('benefits' page)
- Add favicon
- 140 Job site breadcrumbs on all pages
- 142 Internal jobs site
- 155 Jobs extra filters (BE)
- 161 Update job search filter styles and add custom select form field
- 173 Search local council area by postcode
- 179 Jobs additional fields BE

## 12.0 (2020-04-02)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/11.0...12.0

- 136 Employer logos (FE)
- 172 Add live chat support feature
- 174 Fix button padding
- 175 Remove hard coded Bucks logo from job detail pages
- 193 Fix issue with duplicate JobSubcategory titles

## 11.0 (2020-04-01)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/10.0...11.0

- Improve page 'Promote' tab SEO field labels
- 100 Job categories (FE)
- 158 Job application form styling

## 10.0 (2020-03-31)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/9.0...10.0

- 114 StreamField Button Link block (BE)
- 125 Job attachments
- 138 Additional job sidebar fields (FE)
- 139 Additional job sidebar fields (BE)
- 148 Delete outdated jobs when running import command

## 9.0 (2020-03-31)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/8.0...9.0

- 129 Jobs postcode search
- 169 Adjust position of form field help text
- Forms integration with Aptean Respond API
- Fix an issue with CI deployments

## 8.0 (2020-03-30)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/7.0...8.0

- Update documentation to reflect change in git workflow.
- 108 Search alert (FE)
- 112 Unsubscribe from alerts (FE)
- 115 StreamField Button Link block
- 117 StreamField Table styles
- 121 Progressive disclosure accordion
- 122 General formatting improvements
- 123 Subheading block
- 163 Add Fathom Analytics
- 201 additional components

## 7.0 (2020-03-25)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/6.0...7.0

- 51 Events Page front end
- 68 News Page front end
- 105 Job applications back-end
- 106 Job applications front-end
- 109 Job alert subscription
- 110 Job search alert notifications
- 111 Job alert unsubscribe
- 130 Add a Schools and Early years search filter, and enable Job Category to be tagged as such.
- 133 Search by job number

## 6.0 (2020-03-24)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/5.0...6.0

- Added image and embed blocks to StoryBlock

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
