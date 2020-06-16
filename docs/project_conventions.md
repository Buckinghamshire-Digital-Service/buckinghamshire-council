# Buckinghamshire Council project conventions

## Git branching model

We follow a loose version of the [Git flow branching model](https://nvie.com/posts/a-successful-git-branching-model/). A summary would be "like git-flow, but 'develop' is called 'release'".

- Make pull requests against: `release`
- The release prep branch is: `release`
- Start new features by branching from: `release`
- Start bug fixes by branching from: `master`
- The client QA branch is: `staging`
- The internal QA branch is: `staging`
- Do not treat the following branches as merge sources: `staging`

1. Make changes on a new branch, including a broad category and the ticket number if relevant e.g. `feature/123-extra-squiggles`, `fix/newsletter-signup`.
1. Summarise your changes in `CHANGELOG.md`. Sort lines by ticket number (this makes merge and deployment diffs simpler).
1. Push your branch to the remote.
1. Make merge requests at https://git.torchbox.com/buckinghamshire-council/bc/merge_requests/new, setting the 'Source branch' to your feature branch and the 'Target branch' to `release`. Select 'Compare branches and continue'.
1. Edit details as necessary. Use the MR templates configured in GitLab, and the checkboxes therein and project labels to illustrate the current status of the MR.

If you need to preview work on `staging`, this can be merged and deployed manually without making a merge request. You can still make the merge request as above, but add a note to say that this is on `staging`, and not yet ready to be merged to `release`.

NB The MR templates are in version control at `.gitlab/merge_request_templates/`.

## Deployment Cycle

### Versioned releases

The version number is of the form `MAJOR.PATCH`. Planned releases which add features increase the major version number. Bug fix releases increase the patch number.

1. Make merge requests to the branch `release`.
1. Add a heading `# x.x (yyyy-mm-dd)` to `CHANGELOG.md`, detailing what is in this release.
1. Add a comparison link below the `x.x` heading (see other releases for syntax; note that this will not work until the release is tagged, below)
1. Merge `release` to `master`.
1. Deploy to production (see [continuous deployment documentation](continuous-deployment.md#deploying-to-production)).
1. Tag the merge commit
   1. `git tag x.x`
   1. `git push --tags`

Tidy up: merge `master` to `staging`, and if necessary back to `release`. Check the repository graph looks sensible (https://git.torchbox.com/buckinghamshire-council/bc/-/network/master).

### Deploying bug fixes

Urgent bug fixes should be made against the latest-deployed release, i.e. x.x.

1. Pull `master`.
1. Create the bug fix branch, e.g. `hotfix/mend-squiggles`.
   1. In `CHANGELOG.md`, add a new section to `x.(x+1) (yyyy-mm-dd)` where the
      date is the release date.
   1. Add a comparison link below the `x.x` heading (see other releases for syntax; note that this will not work until the release is tagged, below)
1. If it needs client approval, or to be user-tested, deploy to staging.
1. Make a merge request from `hotfix/mend-squiggles` to `master`.
1. Once the change is approved, accept the merge request, and deploy to
   Production
1. Tag the merge commit
   1. `git tag x.(x+1)`
   1. `git push --tags`
1. Merge master into `release`.
