# GitHub User Stories Fake API (Static JSON)

[![Validate data](https://github.com/mickaellherminez/github-user-stories-fake-api/actions/workflows/validate-data.yml/badge.svg)](https://github.com/mickaellherminez/github-user-stories-fake-api/actions/workflows/validate-data.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Free static JSON API for user stories (agile format) hosted directly on GitHub via `raw.githubusercontent.com`.

This repository is useful for frontend demos, tests, mock backends, workshops, and API integration exercises.

## Keywords

`fake api`, `mock api`, `json api`, `user stories`, `agile`, `frontend testing`, `raw github api`, `static dataset`

## Base URL

```txt
https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data
```

## API Endpoints

### Get all user stories

```http
GET /user-stories.json
```

Full URL:

```http
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories.json
```

### Get one user story by id

```http
GET /user-stories/{id}.json
```

Examples:

```http
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/1.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/2.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/3.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/4.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/5.json
... up to
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/30.json
```

## Data Model

Each user story contains:

- `id` and `index` (`US-001`, `US-002`, ...)
- `title` and `description`
- `constraints` (business rules)
- `acceptanceCriteria` (Given/When/Then format)
- `priority` (`low` | `medium` | `high`)
- `status` (`draft` | `ready` | `in-progress` | `done`)
- `images` (mockup URLs)

## Machine-Readable Specs

- OpenAPI spec: [`openapi.yaml`](./openapi.yaml)
- JSON Schema: [`data/user-story.schema.json`](./data/user-story.schema.json)

## Fetch Example (TypeScript)

```ts
const BASE_URL =
  'https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data';

export async function getAllUserStories() {
  const response = await fetch(`${BASE_URL}/user-stories.json`);
  if (!response.ok) throw new Error('Failed to fetch user stories');
  return response.json();
}

export async function getUserStoryById(id: number) {
  const response = await fetch(`${BASE_URL}/user-stories/${id}.json`);
  if (!response.ok) throw new Error(`Failed to fetch user story with id ${id}`);
  return response.json();
}
```

## Stability Note

If you need immutable URLs for production demos, use a commit SHA in the URL instead of `main`.

## Repository Structure

```txt
data/
  user-story.schema.json
  user-stories.json
  user-stories/
    1.json
    ...
    30.json
  img/
openapi.yaml
scripts/
  validate_data.py
.github/
  workflows/
    validate-data.yml
```

## Quality Checks

Data consistency is validated in CI:

- every `data/user-stories/{id}.json` entry must match `data/user-stories.json`
- required fields and enums are validated
- ids, indexes, and image URLs are validated
- the repository currently ships 30 user stories

## License

MIT. See [`LICENSE`](./LICENSE).
