# Release History

## Unreleased

- 335: Responsive images for mobile
- 366: Annotate search results with section or site name
- 467: Enable automatic creation of redirects for moving pages and slug changes.
- 483: Add date to news pages in search results

## 31.0 (2021-01-19)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/30.3...31.0

- 381: Wagtail number list in the editor shouldn't be partially hidden for double digits+
- 450: Prevent draft `InlineIndexChild` pages from being listed in index and navigation on live pages
- 477: Upgrade Wagtail to 2.11

## 30.3 (2021-01-14)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/30.2...30.3

- 490: Bump `notifications-python-client` to version 5.7.1 for `PyJWT` 2.0.0 compatibility (fix email send errors)

## 30.2 (2021-01-13)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/30.1...30.2

- 464: Remove footer columns requirement in navigation settings

## 30.1 (2020-12-14)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/30.0...30.1

- 478: Exclude FIS pages from search (temporary fix until FIS content is ready)

## 30.0 (2020-12-14)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/29.0...30.0

- 402: Add anchor links for streamfield heading blocks
- 472: Upgrade Wagtail to 2.10
- 475: FIS Allow `IndexPage` as child page of `CategoryTypeOnePage` and `CategoryTypeTwoPage`
- 476: FISAllow `InformationPage` as child page of `CategoryTypeOnePage` and `CategoryTypeTwoPage`

## 29.0 (2020-11-30)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/28.0...29.0

- Add support for Elasticsearch backend
- Add configurable search synonyms
- Use Porter stemming algorithm search filter, for English grammar
- Add an English stop words search filter
- Prevent password-protected pages from appearing in search results
- Add StreamField ImageBlock alt text field

## 28.0 (2020-11-25)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/27.0...28.0

- FIS Homepage: Style page and components
- FIS Category Type 1 / SEND Page: Style page and components
- FIS Category Type 2 / Regular Page: Style page and components
- FIS Inline Index Page: Hide sidebar
- FIS Footer: Style footer
- FIS Header: Style header
- Update margins between paragraphs in accordion blocks
- Add an editable body that will show when there's no results in the Search page
- Add schema.org Organization markup to home page
- Add new 'Am I in lockdown?' streamfields - FE styling
- Add new Highlight StreamField block
- Add LookupPage type to search for information about postcodes
- Accessibility 12 Fix HTML validation error for duplicated IDs when searching
- Fix edge-case failure with middleware is_recruitment_site check
- Fix form errors in pattern library

## 27.0 (2020-10-15)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/26.0...27.0

- Add Wagtail admin report of pages missing SEO metadata, and those with unpublished changes
- Accessibility 89 Form error handling - add explanatory text and supporting aria-labels for required fields
- Accessibility 91 Add in missing fieldsets for radio input groups
- Add schema.org markup to job detail page

## 26.0 (2020-09-22)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/25.0...26.0

- Add an 'OGL' logo, statement and link to the footer
- Accessibility 17 Add subpages to the Jobs sitemap
- Accessibility 76 Improve accordion markup & styles (including job filters)
- Accessibility 93 Add meaningful link text for pagination
- Accessibility 94 Add aria-labels to social links
- Accessibility 87 Improve markup of feedback widget buttons and add aria-labels
- Silently ignore SQL injection attempts in job search

## 25.0 (2020-09-14)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/24.0...25.0

- Fix string spacing issue in Aptean forms help text
- Change complaints form contact fields

## 24.0 (2020-08-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/23.0...24.0

- Refactor Aptean Respond API integration to give more control over form presentation
- Add file field support to Aptean Respond forms
- Custom sizes for input fields
- Sitewide alert messages
- Always show application forms front end component, even if the job ID is not imported

## 23.0 (2020-07-27)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/22.0...23.0

- Accessibility 77 Further changes to prevent horizontal scrolling on smaller mobile devices
- Add social media text & new icon/links to footer
- Fix for bottom of homepage displaying incorrectly on IE11

## 22.0 (2020-07-23)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/21.0...22.0

- Upgrade Wagtail to 2.9.3
- Configure Wagtail's Cloudflare front end cache invalidation
- Add to documentation about caching infrastructure
- Jobs: Add Restless logo to header
- Jobs 166 set up reuse application button
- Accessibility 47 Increase contrast of form help text
- Accessibility 80 Improve landmark aria labelling
- Accessibility 81 Content not included in landmarks

## 21.0 (2020-07-09)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/20.0...21.0

- Accessibility 79 Hide sidebar aria-labelledby attribute when there are no related pages
- Add page feedback widget

## 20.0 (2020-07-02)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/19.1...20.0

- Add cookie banner to recruitment / jobs site
- Make max-width larger on main wrapper
- Adjust line height of headings
- Progressive disclosure details (BE)
- Update newsletter signup URL
- Add favicon to recruitment site
- Reinstate display of promoted search results
- Fix 'no results found' message when there is no search query
- Enable embedding YouTube videos without using cookies and without showing
  unrelated video links
- Make the homepage child sections 'menu' respect the 'show_in_menus' property
- Mobile-friendly tables
- Accessibility 77 Remove horizontal scrolling for smaller mobile devices
- Accessibility 78 Improve pagination link text (Silktide improvement)
- Improve the method for returning a formatted Aptean Respond case reference number

## 19.1 (2020-06-23)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/19.0...19.1

- Add cache prevention headers to Aptean Respond form pages

## 19.0 (2020-06-11)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/18.0...19.0

- Upgrade Wagtail to 2.9
- 404 page
- Styling of label text on checkboxes and radio buttons
- Remove current page from breadcrumbs
- Adjust margins before / after buttons and other elements
- Fix search results font sizes / styling
- Fix incorrect heading levels for body text headings and subheadings

## 18.0 (2020-06-04)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/17.0...18.0

- Upgrade Django to 2.2.13
- Permit subdomain sites to have different base templates, depending on homepage type
- Sign up to council newsletter(s) from the homepage
- Update cookie notice
- Fix job alert emails
- Make the job application page return 404 status for bad IDs
- Update job search salary filter to use searchable salary instead of salary range
- Add documentation about CI deployments
- Update documentation about personally-identifying data
- Add documentation about the procedure for resetting the staging branch/server/db

## 17.0 (2020-05-21)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/16.1...17.0

- Change GitLab HTML syntax highlighter
- Accessibility 37 Improve aria role of alert panel
- Accessibility 53 Hide footer links landmark if there are none
- Accessibility 55 Email alert subscription form improvements
- Accessibility 56 Remove extra role="search" form from header on search page
- Accessibility 57 Label complementary landmarks
- Accessibility 61 Remove alt text for decorative images

## 16.1 (2020-05-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/16.0...16.1

- Enable a job board-dependent template variable for the application page. This
  fixes internal job applications.
- Fix an error when job application URL query is badly formatted

## 16.0 (2020-05-07)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/15.1...16.0

- Fix for employer logo sizes (FE)
- Add active checkbox counter & reset filters button for job search (FE)
- Progressive accordion styling update (including postcode search fix)
- Accessibility 14 Increase contrast of Highlighted Content heading
- Accessibility 16 Fix Jobs filter fieldset legends
- Accessibility 18 Page content should be in a landmark
- Accessibility 19 Remove nesting for landmarks
- Accessibility 44 & 75 Pagination improvements
- Accessibility 58 Add screen-reader-only text to filters’ item count
- Accessibility 60 Fix typo in location field placeholder
- Accessibility 62 Hide "Find out more" for screen reader users (Jobs benefits)

## 15.1 (2020-05-01)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/15.0...15.1

- Fix for breadcrumbs

## 15.0 (2020-05-01)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/14.0...15.0

- Add tests for job categories import fix
- Add unit tests for Aptean Respond integration
- Subheading block (BE)
- Styling fix for links to local areas
- Fix spacing in breadcrumb navigation
- Fix spacing on job detail template
- Fix for multiple form submissions
- 142 Internal jobs site
- Alert panel and Aptean Form Page confirmation page template update
- Reformat Aptean Respond submitted case reference numbers for display to users
- Accessibility 1 Remove redundant/inappropriate ARIA role overrides
- Accessibility 8 Hide all site icons for screen reader users
- Accessibility 9 Improvements to screen reader only navigational content
- Accessibility 11 Fix HTML validation errors on the main site
- Accessibility 13 Fix jobs search filters HTML validation errors on IDs
- Accessibility 9 & 13 Breadcrumb improvements
- Accessibility 22 Switch unnecessary heading tag to link in Jobs header
- Accessibility 23 Increase contrast of jobs filter help text
- Accessibility 28 Update language attribute on all templates
- Accessibility 36 Update homepage table of contents & add aria-labelledby

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
