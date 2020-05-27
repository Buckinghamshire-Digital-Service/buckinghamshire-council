<!-- See 'Deployment Cycle' in the documentation.  -->

# Description

---

Release process:

- [ ] Compare CHANGELOG.md with the previous release, to check nothing has got accidentally buried or merged outside of the "Unreleased" section `git diff {previous-version-tag} CHANGELOG.md`
- [ ] Change "Unreleased" on `CHANGELOG.md` to `x.x (yyyy-mm-dd)` where the date is the release date.
- [ ] Add a 'comparison' line to show the diff for this release.
- [ ] Client has done final testing on staging, with a clone of production data if necessary.

Okay, now you may merge to master and deploy.

Steps for after deploying:

- [ ] Add a new "Unreleased" section on `CHANGELOG.md`.
- [ ] Create a git tag on master `x.x`
- [ ] Merge master into staging
