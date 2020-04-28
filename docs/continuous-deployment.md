# Buckinghamshire Council — Continuous Deployment

Deployments can be triggered through GitLab's CI/CD. Currently `.gitlab-ci.yml` has a `deploy_site` stage which is configured to deploy to Heroku on pushes and merge requests to either master or staging.

Deployments can also be done through the terminal with Git and the [heroku CLI](https://devcenter.heroku.com/articles/git), however best practice is to go through the GitLab CI/CD.

For information on hosting such as Heroku app names see [hosting documentation](hosting.md#deploying-to-production).

## Deploying to production

After the `Deploy to production` stage of the [development life cycle](project_conventions.md#deployment-cycle) wait for the pipeline to pass, click on the `Manual job` dropdown and then click `deploy_production`. This will require `maintainer` permission for the project on GitLab.

## Deploying to staging

Unlike production, deployments to staging are done automatically through GitLab CI/CD, simply push to staging.
