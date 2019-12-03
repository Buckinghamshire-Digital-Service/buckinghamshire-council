# Buckinghamshire Council Wagtail site

## Technical documentation

This project contains technical documentation written in Markdown in the `/docs` folder. This covers:

- continuous integration
- deployment
- git branching
- project conventions

You can view it using `mkdocs` by running:

```bash
mkdocs serve
```

The documentation will be available at: http://localhost:8001/

# Setting up a local build

This repository includes a Vagrantfile for running the project in a Debian VM and
a fabfile for running common commands with Fabric.

To set up a new build:

```bash
git clone [URL TO GIT REMOTE]
cd bc
vagrant up
vagrant ssh
```

Then within the SSH session:

```bash
dj migrate
dj createcachetable
dj createsuperuser
djrun
```

This will make the site available on the host machine at: http://127.0.0.1:8000/

## Front-end assets

After any change to the CSS or Javascript, you will need to run the build command, either in the VM or on your host machine. See the [Front-end tooling docs](docs/front-end-tooling.md) for further details.
