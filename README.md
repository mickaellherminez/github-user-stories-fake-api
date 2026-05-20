# GitHub User Stories Static API

This repository exposes User Stories in JSON format.

No GitHub Pages setup is required.

## API Endpoints

### Get all user stories

```http
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories.json
```

### Get user story by id

```http
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/1.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/2.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/3.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/4.json
GET https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data/user-stories/5.json
```

## Structure

```txt
data/
  user-stories.json
  user-stories/
    1.json
    2.json
    3.json
    4.json
    5.json
```

## Fetch example

```ts
const BASE_URL =
  'https://raw.githubusercontent.com/mickaellherminez/github-user-stories-fake-api/main/data';

export async function getAllUserStories() {
  const response = await fetch(`${BASE_URL}/user-stories.json`);

  if (!response.ok) {
    throw new Error('Failed to fetch user stories');
  }

  return response.json();
}

export async function getUserStoryById(id: number) {
  const response = await fetch(`${BASE_URL}/user-stories/${id}.json`);

  if (!response.ok) {
    throw new Error(`Failed to fetch user story with id ${id}`);
  }

  return response.json();
}
```
