# Contributing

Contributions are welcome and are greatly appreciated! Every
little bit helps, and credit will always be given.

# Table of Contents
  * [Formatting Style](#formatting-style)
  * [Branching Model](#branching-model)
  * [Contribution Process](#contribution-process)
  * [Types of Contributions](#types-of-contributions)
      - [Report Bugs](#report-bugs)
      - [Fix Bugs](#fix-bugs)
      - [Implement Features](#implement-features)
      - [Improve Documentation](#improve-documentation)
      - [Submit Feedback](#submit-feedback)
  * [Code of Conduct](#documentation)
  * [Development and Testing](#development-and-testing)
      - [Set up a development env using Docker](#set-up-a-development-env-using-docker)

## Formatting Style

In order to have a standardised code base, we only accept code that is formatted according to PEP 8.

## Branching Model

Our branching model has one permanent branch, **main**. We aim at using `main` as the main branch, where all 
features are merged. In this sense, we also use the master branch to store the release versions of the Django Channels MUD library 
by means of git tags.

## Contribution Process

In order to contribute to the code base, we follow the next process :
1. The main branch is `master`, every developer should pull the current status of the branch before starting to develop any new feature.
`git pull`
1. Create a new branch with the following pattern "feature/[name_of_the_feature]"
`git checkout -b feature/example_feature`
3. Develop the new feature on the the new branch. It includes testing and documentation.
`git commit -a -m "Bla, Bla, Bla";  git push`
4. Open a Pull Request to merge the feature branch into `master`. Currently, a pull request has to be reviewed at least by one person.
5. Finally, delete the feature branch.
6. Move back to `master` branch.
`git checkout master`
7. Pull the latest changes.
`git pull`

## Types of Contributions

### Report Bugs

Report bugs through [GitHub issues](https://github.com/criped/mud-server/issues)

Please follow the project issue template to exhibit the problem.

### Fix Bugs

Look at GitHub issues for bugs. Anything is open to whoever wants to implement it.

### Implement Features

Look at [GitHub issues](https://github.com/criped/mud-server/issues) for feature requests. Any unassigned
"Improvement" issue is open to whoever wants to implement it.

### Improve Documentation

Django Channels MUD could always use better documentation, whether as part of the official Khiva docs, or even description of the 
methods in the different namespaces.

### Submit Feedback

The best way to send feedback is to open an issue on [GitHub issues](https://github.com/criped/mud-server/issues)

If you are proposing a feature, please follow the feature request template.

## Code of Conduct

We stick to [Django's code of conduct](https://www.djangoproject.com/conduct/)

## Development and Testing

### Set up a development env using Docker

Start docker containers.

```
# Start docker compose 
docker-compose up
```