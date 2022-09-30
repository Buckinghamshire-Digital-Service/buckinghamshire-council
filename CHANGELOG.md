# Release History

## Unreleased

- Synchronise docker-compose file version numbers
- Add list_creatable_pages management command

## 63.1 (2022-10-03)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/63.1...63.0>

- Add configurable timeout to Python client for maps.buckscc.gov.uk API

## 63.0 (2022-09-27)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/63.0...62.0>

- **A11y**: Add `overflow-wrap` & `word-break` CSS properties to `<ul>` & `<ol>` elements to prevent text from overflowing its line box, causing problems particularly on smaller devices.
- **A11y**: Fix accessibility on Blog Home Page template by adding `listitem` role to `<span>` elements in unordered lists
- **A11y**: Add `<h2>` headings to the `introduction` RichTextField in the StepByStepPage model, thus allowing for creation of an accessible heading order.

## 62.0 (2022-08-30)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/-/merge_requests/574/diffs>

- [Wagtail 3.0 upgrade](https://git.torchbox.com/buckinghamshire-council/bc/-/merge_requests/548)
- [Support/birdbath flightpath](https://git.torchbox.com/buckinghamshire-council/bc/-/merge_requests/573)

## 61.0 (2022-08-09)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/60.1...61.0>

- Add `BlogAboutPage`
- Prevent more `InformationPage`s from being added to the `BlogHomePage`
- Allow the use of formatted table blocks and plain text table blocks in most pages

## 60.1 (2022-07-27)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/60.0...60.1>

- Change dbs field label on jobs sidebar

## 60.0 (2022-07-26)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/59.0...60.0>

- Remove bottom border from last section on sidebar
- Add button to decline cookies
- Change dbs_check from booleanfield to a textfield
- Add categories to blogs
- Add subscriptions to blogs
- Add Blog global homepage

## 59.0 (2022-07-19)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/58.0...59.0>

- Add safe spaces banner to site footer

## 58.0 (2022-07-04)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/57.0...58.0>

- Docker for development work https://git.torchbox.com/buckinghamshire-council/bc/-/merge_requests/522

## 57.0 (2022-06-30)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/56.0...57.0>

- Add placeholder blog global homepage

## 56.0 (2022-06-28)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/55.0...56.0>

- Add beacons for different steps throughout a job application

## 55.0 (2022-06-28)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/54.2...55.0>

- Add model for `BlogHomePage` and corresponding template
- Add model and UI for `BlogPostPage`
- Add backend for blogs search
- Add recent posts block to blog sidebar
- Add social media links to blog sidebars
- Add search bar for the blog site
- Add blogs list UI component
- Add filtered view - search results
- Add pagination on blog homepage
- Add featured blog post UI
- Fix blog listing border
- Add intro text to be displayed in blog home page listings

## 54.2 (2022-06-28)

Compare: <https://git.torchbox.com/buckinghamshire-council/bc/compare/54.1...54.2>

- Fix aria labels of buttons in pagination and local area link blocks

## 54.1 (2022-05-23)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/54.0...54.1

- Fix tables not showing horizontal lines between rows
- Add rich text and numeric options to typedtable

## 54.0 (2022-05-12)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/53.0...54.0

- Update Black to a newer version to fix \_unicodefun linting issue. Also applied formatting on existing files.
- Add aligned columns to typedtable
- Add intro text field to several page types
- Make alert length 255 characters long (text only)
- Fix issues with hidden content being focusable
- Fix issues with form field not being labelled
- Migrate to heroku-deploy

## 53.0 (2022-01-31)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/52.1...53.0

- Prefix Sentry release variable with environment name, for easier debugging
- Add inset text component to StoryBlock
- Fix issues with job sitemap displaying jobs from other domains

## 52.1 (2022-01-25)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/52.0...52.1

- Fix location page referencing deleted sidebar template

## 52.0 (2022-01-24)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/51.0...52.0

- Add LocationIndex and Location pages
- Update documentation to summarise use of wagtail-geo-widget for maps

## 51.0 (2022-01-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/50.3...51.0

- Add 'Part of' section to sidebar for pages referenced by StepByStepPage
- Fix event datetime formats
- Add contents section with 'Scroll to top' feature for InformationPage

## 50.3 (2022-01-11)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/50.2...50.3

- Fix: Treat 'table' block values as TableBlock instances when nested in Accordion

## 50.2 (2022-01-11)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/50.1...50.2

- Fix alignment issue for tables where first column is a header

## 50.1 (2022-01-07)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/50.0...50.1

- Fix an issue with job searches by postcode, due to a query expression change in Django 3.2

## 50.0 (2022-01-07)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/49.0...50.0

- Upgrade Wagtail to 2.15.1, Django to 3.2.9, django-pattern-library to 0.5,
  django-redis to 4.11.0, factory-boy to 3.2.1, freezegun to 1.1.0, responses to 0.16.0,
  wagtail-factories to 2.0.1, and whitenoise to 5.0; and replace deprecated & removed
  functions & fields
- Upgrade TableBlock to TypedTableBlock
- Update data protection docs with an extra table to anonymise

## 49.0 (2021-12-17)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/48.0...49.0

- StepByStepPage — Change body of each step to a RichTextField

## 48.0 (2021-12-14)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/47.0...48.0

- Add TIDE winners logo to Jobs site header

## 47.0 (2021-12-01)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/46.0...47.0

- Postcode Lookup — Update the area links block UI to permit only querying by postcode
- Postcode Lookup — Remove local area links lists from search results
- Postcode Lookup — Use the internal Buckinghamshire maps API
- Postcode Lookup — Query additional address data for border postcodes
- Postcode Lookup — Update documentation

## 46.0 (2021-11-29)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/45.1...46.0

- Add Step-by-Step page type
- Add accordion block to long-form content pages
- Fix process_block_numbers to consider non-heading numbers
- Change search result label & date colour to meet WCAG AA standard
- Change paragraph number to meet WCAG AA standard

## 45.1 (2021-11-05)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/45.0...45.1

- Fix accordion element IDs and aria roles mismatch

## 45.0 (2021-10-12)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/44.1...45.0

- No longer set CSRF cookies for FormPage forms and derivatives, or job search form
- Update job category and subcategory filtering documentation
- Use RoutablePageMixin and redirects to show Aptean Respond instruction, form, and success pages

## 44.1 (2021-10-06)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/44.0...44.1

- Upgrade Wagtail Transfer to 0.8.2

## 44.0 (2021-10-04)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/43.0...44.0

- 333 Fix to accordion alignment
- Accessibility 321 Fix job search results validation issues
- Relabel heading blocks on longform pages, and add H4 block

## 43.1 (2021-09-27)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/43.0...43.1

- Make settings.DATA_UPLOAD_MAX_NUMBER_FIELDS configurable

## 43.0 (2021-09-17)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/42.0...43.0

- Accessibility 250 Fix HTML validation: element style not allowed as child of element main
- Accessibility 250 Fix job search input placeholder text contrast
- Remove unused call to action StreamField block template
- Use "or" search operator
- Use Longform Page chapter headings in the table of contents and pagination

## 42.0 (2021-08-25)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/41.0...42.0

- 15: Add campaign page type
- Permit configuring some host names never to be indexed by external search engines

## 41.0 (2021-08-19)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/40.0...41.0

- Add "DBS check" field to TalentLink jobs and display the information in the sidebar

## 40.0 (2021-07-19)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/39.1...40.0

- Add chart StreamField blocks to long-form content pages
- Stop using CSRF tokens for feedback widget

## 39.1 (2021-07-07)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/39.0...39.1

- Upgrade Django to 2.2.24

## 39.0 (2021-07-01)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/38.0...39.0

- Add CI job to deploy the master branch to Content Prep server
- Enable content transfer between Wagtail instances using https://github.com/wagtail/wagtail-transfer
- Upgrade Wagtail to version 2.13.2

## 38.0 (2021-06-28)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/37.3...38.0

- Add feature flags to disable page feedback and job alert forms
- Add validation of duplicate responses to LookupPage admin
- Fix 128: Use inline index subtitle in table of contents and pagination
- Use PostgreSQL 13.3 in Vagrant box and CI

## 37.3 (2021-06-11)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/37.2...37.3

- Fix: Field label typo in page feedback form

## 37.2 (2021-06-10)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/37.1...37.2

- Fix: Handle URLs longer than 200 characters in page feedback form

## 37.1 (2021-06-09)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/37.0...37.1

- Fix (Accessibility): Duplicate HTML element IDs in feedback form
- Fix (Accessibility): Prevent duplicate h2 element IDs in alerts
- Fix: StreamField typo causing missing block types in editor in Wagtail 2.13
- Upgrade Wagtail to version 2.13.1

## 37.0 (2021-06-07)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/36.1...37.0

- 40: Feedback forms and reports
- Accessibility improvements
- Add multiple severity levels to sitewide alert
- Fix: StreamField typo causing RecursionError in Wagtail 2.13
- Upgrade Wagtail to version 2.13
- Use the newly released django-gov-notify library for GOV.UK Notify integration

## 36.1 (2021-05-25)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/36.0...36.1

- Fix: Include attachments in FOI form data

## 36.0 (2021-05-20)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/35.2...36.0

- Add ENEI logo to Jobs site header
- Update CI config to use the cache to store artefacts
- Upgrade Django to 2.2.21

## 35.2 (2021-04-21)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/35.1...35.2

- Fix: XSS vulnerability in "no search results" page

## 35.1 (2021-02-24)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/35.0...35.1

- Upgrade Django to 2.2.19

## 35.0 (2021-02-18)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/34.1...35.0

- 498: Reduce news boost in search results
- 513: Allow second FIS homepage for Care Advice microsite
- 517: Fix: Preview behind basic auth with new `baipw` version
- 518: Include FIS pages in search results
- 519: Fix: OGL below links and typo
- 520: Fix: Add `search_input_help_text` setting to allow directory link for FIS
- 521: Fix: Upgrade Wagtail 2.12.2 to prevent migration issue in CI

## 34.1 (2021-02-15)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/33.0...34.1

- Fix: Update GitHub Pages workflow to ensure publication of docs

## 34.0 (2021-02-15)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/33.0...34.0

- 239: Prepare repository for open sourcing
- 508: Upgrade Wagtail to version 2.12
- Fix: Check page exists before calling pageurl in footer

## 33.0 (2021-02-02)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/32.1...33.0

- 466: [longform 9] Prepare base template for long-form content pages
- 466: [longform 14] Add hero image to long-form content pages
- 466: [longform 10] Add numbered headings for long-form content pages
- 489: Allow information page under FIS home page.
- Upgrade `django-basic-auth-ip-whitelist` to avoid caching of 401 resonses.

## 32.1 (2021-01-28)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/32.0...32.1

- 335: Fix so that component images aren't overwritten

## 32.0 (2021-01-27)

Compare: https://git.torchbox.com/buckinghamshire-council/bc/compare/31.0...32.0

- 335: Responsive images for mobile
- 366: Annotate search results with section or site name
- 392: Use default sharing text if no sharing text set on page
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
