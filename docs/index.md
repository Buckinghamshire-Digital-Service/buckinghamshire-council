# Buckinghamshire Council Technical Documentation

## Project overview

Buckinghamshire Council is a new unitary council formed from the five previous county and district councils in Buckinghamshire.

This project is primarily a CMS. During the initial phase, when the council is first inaugurated, it will serve a mixture of content written specially for the new council, and links to the previous councils' pages where services differ on a local basis.

Other features include:

- a job listings portal,
- a live chat client,
- an integration for complaints and request forms.

## Setting Up a Local Build

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

## Front-end Assets

After any change to the CSS or Javascript, you will need to run the build command, either in the VM or on your host machine. See the [Front-end tooling docs](./front-end-tooling.md) for further details.

## Adding documentation

The navigational index of the documentation files is defined in the `mkdocs.yml` file. Add any new markdown files to that index. You can also link directly to files where necessary, using markdown formatting and relative URLs.

## External Integrations

<!-- List here any external services this project uses. Preferably link to a separate documentation page for each. -->

- The jobs portal will work with Lumesse. Please see the [recruitment site documentation](./recruitment_site.md) for details.
- The [live chat client](./live-chat-client.md) is provided by Client4Access.
- [Complaints and request forms](complaints-and-requests.md) features is based on the Aptean Respond case management platform.

## Contributing

To contribute to this project, please review the [notes on contributing](./contributing.md).
