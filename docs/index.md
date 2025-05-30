# Buckinghamshire Council Technical Documentation

## Project overview

Buckinghamshire Council is a new unitary council formed from the five previous county and district councils in Buckinghamshire.

This project is primarily a CMS. During the initial phase, when the council is first inaugurated, it will serve a mixture of content written specially for the new council, and links to the previous councils' pages where services differ on a local basis.

Other features include:

- a job listings portal,
- a live chat client,
- an integration for complaints and request forms.

## Setting up a local build

This repository includes `docker-compose` configuration for running the project in local Docker containers,
and a fabfile for provisioning and managing this.

There are a number of other commands to help with development using the fabric script. To see them all, run:

```bash
fab -l
```

## Dependencies

The following are required to run the local environment. The minimum versions specified are confirmed to be working:
if you have older versions already installed they _may_ work, but are not guaranteed to do so.

- [Docker](https://www.docker.com/), version 19.0.0 or up
  - [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) installer
  - [Docker Engine for Linux](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc&operating_system=linux) installers
- [Docker Compose](https://docs.docker.com/compose/), version 1.24.0 or up
  - [Install instructions](https://docs.docker.com/compose/install/) (Linux-only: Compose is already installed for Mac users as part of Docker Desktop.)
- [Fabric](https://www.fabfile.org/), version 2.4.0 or up
  - [Install instructions](https://www.fabfile.org/installing.html)
- Python, version 3.6.9 or up

Note that on Mac OS, if you have an older version of fabric installed, you may need to uninstall the old one and then install the new version with pip3:

```bash
pip uninstall fabric
pip3 install fabric
```

You can manage different python versions by setting up `pyenv`: <https://realpython.com/intro-to-pyenv/>

Additionally, for interacting with production / staging environments, you'll need:

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

## Running the local build for the first time

If you are using Docker Desktop, ensure the Resources:File Sharing settings allow the cloned directory to be mounted in the web container (avoiding `mounting` OCI runtime failures at the end of the build step).

Starting a local build can be done by running:

```bash
git clone git@git.torchbox.com:buckinghamshire-council/bc.git
cd bc
fab build
fab migrate
fab start
```

This will start the containers in the background, but not Django. To do this, connect to the web container with `fab sh` and run `honcho start` to start both Django and the Webpack dev server in the foreground.

Then, connect to the running container again (`fab sh`) and:

```bash
dj createcachetable
dj createsuperuser
```

The site should be available on the host machine at: <http://127.0.0.1:8000/>

If you only wish to run the frontend or backend tooling, the commands `honcho` runs are in `docker/Procfile`.

Upon first starting the container, the static files may not exist, or may be out of date. To resolve this, simply run `npm run build`.

## Front-end Assets

After any change to the CSS or Javascript, you will need to run the build command, either in the VM or on your host machine. See the [Front-end tooling docs](./front-end-tooling.md) for further details.

## Adding documentation

The navigational index of the documentation files is defined in the `mkdocs.yml` file. Add any new markdown files to that index. You can also link directly to files where necessary, using markdown formatting and relative URLs.

## External Integrations

<!-- List here any external services this project uses. Preferably link to a separate documentation page for each. -->

- The jobs portal will work with Lumesse. Please see the [recruitment site documentation](./recruitment-site.md) for details.
- The [live chat client](./live-chat-client.md) is provided by Client4Access.
- [Complaints and request forms](complaints-and-requests.md) features is based on the Aptean Respond case management platform.
- [Location maps widget](location-maps-widget.md) is based on the Google Maps API.

## Unique features

- This project uses a custom implementation of [Wagtail's form builder](https://docs.wagtail.org/en/stable/reference/contrib/forms/index.html), located in the `bc.forms` app. It adds a new management command called `stale_submissions` which is meant to be run daily on the server (with its `--delete` flag). This command will delete submissions for forms which are configured for it.

- It also comes with a custom `EmbeddedFormBlock` streamfield block that lets editors embed forms from a `FormPage` inside another page.

## Contributing

To contribute to this project, please review the [notes on contributing](./contributing.md).
