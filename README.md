# GitHub User Stories Static API

This repository exposes User Stories in JSON format.

## Endpoints with GitHub Pages

After enabling GitHub Pages:

```txt
GET https://<USER>.github.io/<REPO>/data/user-stories.json
GET https://<USER>.github.io/<REPO>/data/user-stories/1.json
GET https://<USER>.github.io/<REPO>/data/user-stories/2.json
GET https://<USER>.github.io/<REPO>/data/user-stories/3.json
GET https://<USER>.github.io/<REPO>/data/user-stories/4.json
GET https://<USER>.github.io/<REPO>/data/user-stories/5.json
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
export async function getAllUserStories() {
  const response = await fetch('/data/user-stories.json');

  if (!response.ok) {
    throw new Error('Failed to load user stories');
  }

  return response.json();
}

export async function getUserStoryById(id: number) {
  const response = await fetch(`/data/user-stories/${id}.json`);

  if (!response.ok) {
    throw new Error(`User story ${id} not found`);
  }

  return response.json();
}
```
