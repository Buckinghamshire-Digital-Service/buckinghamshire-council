# Buckinghamshire Council Wagtail Site

This is the repository for the [new website of the joint Buckinghamshire Council](https://www.buckinghamshire.gov.uk/). 

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

## Setting up a local build

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

## Contributing

This project is open source, but not really a collaborative project.
The features of this project are specifically developed for the needs of the Buckinghamshire Council. 
Additional features are unlikely to be added, unless they are specifically requested by the council. 
Bugfixes are welcome and will be reviewed. 

Please read and adhere to the guidlines outlined in the [technical documentation](docs/).

The main convention for new developers to be aware of is the branching model.
- Create new feature or fix branches from the `release` branch. 
- Create  make merge/pull requests back to that branch. 

See the [project conventions](docs/project_conventions.md) for full details.
