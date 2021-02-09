# Buckinghamshire Council Wagtail Site

This is the repository for the [website of the new unitary Buckinghamshire Council](https://www.buckinghamshire.gov.uk/).

Please review the [technical documentation](docs/index.md) before working on this project.

## Technical documentation

This project contains technical documentation written in Markdown in the `/docs` folder. This covers:

- continuous integration
- deployment
- git branching
- project conventions

<!-- This link will only work once the repo is on GitHub. -->
You can find a hosted version of the [technical documentation on GitHub Pages](https://Buckinghamshire-Digital-Service.github.io/buckinghamshire-council/).

If you have a local copy of the repo, you can also view the docs with `mkdocs` by running:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

The documentation will be available at: http://localhost:8001/

## Contributing

This project is open source, but not really a collaborative project.
The features of this project are specifically developed for the needs of the Buckinghamshire Council.
Additional features are unlikely to be added, unless they are specifically requested by the council.
Bugfixes are welcome and will be reviewed.

Please read and adhere to the guidlines outlined in the [technical documentation](docs/).

The main convention for new developers to be aware of is the branching model.

- Create new feature or fix branches from the `release` branch.
- Create make merge/pull requests back to that branch.

See the [project conventions](docs/project_conventions.md) for full details.
