#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
AGGREGATE_FILE = DATA_DIR / "user-stories.json"
DETAILS_DIR = DATA_DIR / "user-stories"

ALLOWED_PRIORITIES = {"low", "medium", "high"}
ALLOWED_STATUSES = {"draft", "ready", "in-progress", "done"}
INDEX_PATTERN = re.compile(r"^US-\d{3}$")
RAW_IMAGE_PREFIX = (
    "https://raw.githubusercontent.com/"
    "mickaellherminez/github-user-stories-fake-api/main/data/img/"
)

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def read_json(file_path: Path) -> Any:
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Invalid JSON file: {file_path.relative_to(ROOT_DIR)} ({exc})")
        return None


def validate_non_empty_string_array(value: Any, field_name: str, context: str) -> None:
    if not isinstance(value, list) or len(value) == 0:
        fail(f'{context}: "{field_name}" must be a non-empty string array')
        return

    for idx, entry in enumerate(value):
        if not isinstance(entry, str) or len(entry.strip()) == 0:
            fail(f'{context}: "{field_name}[{idx}]" must be a non-empty string')


def validate_user_story(story: Any, context: str) -> None:
    if not isinstance(story, dict):
        fail(f"{context}: item must be an object")
        return

    required_keys = [
        "id",
        "index",
        "title",
        "description",
        "constraints",
        "acceptanceCriteria",
        "priority",
        "status",
        "images",
    ]

    extra_keys = [key for key in story.keys() if key not in required_keys]
    if extra_keys:
        fail(f'{context}: unsupported keys detected ({", ".join(extra_keys)})')

    for key in required_keys:
        if key not in story:
            fail(f'{context}: missing required key "{key}"')

    story_id = story.get("id")
    if not isinstance(story_id, int) or story_id < 1:
        fail(f'{context}: "id" must be an integer >= 1')

    story_index = story.get("index")
    if not isinstance(story_index, str) or not INDEX_PATTERN.match(story_index):
        fail(f'{context}: "index" must match US-XXX')
    elif isinstance(story_id, int):
        expected_index = f"US-{story_id:03d}"
        if story_index != expected_index:
            fail(f'{context}: "index" should be "{expected_index}" for id {story_id}')

    if not isinstance(story.get("title"), str) or len(story["title"].strip()) == 0:
        fail(f'{context}: "title" must be a non-empty string')

    if not isinstance(story.get("description"), str) or len(story["description"].strip()) == 0:
        fail(f'{context}: "description" must be a non-empty string')

    validate_non_empty_string_array(story.get("constraints"), "constraints", context)
    validate_non_empty_string_array(
        story.get("acceptanceCriteria"), "acceptanceCriteria", context
    )

    if story.get("priority") not in ALLOWED_PRIORITIES:
        fail(
            f'{context}: "priority" must be one of '
            f'{", ".join(sorted(ALLOWED_PRIORITIES))}'
        )

    if story.get("status") not in ALLOWED_STATUSES:
        fail(
            f'{context}: "status" must be one of '
            f'{", ".join(sorted(ALLOWED_STATUSES))}'
        )

    images = story.get("images")
    if not isinstance(images, list) or len(images) == 0:
        fail(f'{context}: "images" must be a non-empty array')
    else:
        for idx, image_url in enumerate(images):
            if not isinstance(image_url, str) or not image_url.startswith(RAW_IMAGE_PREFIX):
                fail(
                    f'{context}: "images[{idx}]" must start with "{RAW_IMAGE_PREFIX}"'
                )
                continue

            relative_path = image_url.replace(
                "https://raw.githubusercontent.com/"
                "mickaellherminez/github-user-stories-fake-api/main/",
                "",
            )
            local_path = ROOT_DIR / relative_path
            if not local_path.is_file():
                fail(f"{context}: image file not found ({relative_path})")


def validate() -> int:
    aggregate_stories = read_json(AGGREGATE_FILE)
    if not isinstance(aggregate_stories, list):
        fail("data/user-stories.json must be a JSON array")
        aggregate_stories = []

    seen_ids: set[int] = set()

    for idx, story in enumerate(aggregate_stories):
        context = f"data/user-stories.json[{idx}]"
        validate_user_story(story, context)
        story_id = story.get("id") if isinstance(story, dict) else None
        if isinstance(story_id, int):
            if story_id in seen_ids:
                fail(f"{context}: duplicate id {story_id}")
            seen_ids.add(story_id)

    detail_files: list[Path] = []
    for file in DETAILS_DIR.glob("*.json"):
        if not file.is_file():
            continue
        if not file.stem.isdigit():
            fail(
                f"data/user-stories/{file.name}: filename must be numeric (example: 1.json)"
            )
            continue
        detail_files.append(file)

    detail_files.sort(key=lambda file: int(file.stem))

    if len(detail_files) != len(aggregate_stories):
        fail(
            "data/user-stories has "
            f"{len(detail_files)} file(s) but aggregate contains "
            f"{len(aggregate_stories)} item(s)"
        )

    stories_by_id = {}
    for story in aggregate_stories:
        if isinstance(story, dict):
            story_id = story.get("id")
            if isinstance(story_id, int):
                stories_by_id[story_id] = story

    for detail_file in detail_files:
        detail_id = int(detail_file.stem)
        detail_story = read_json(detail_file)
        context = f"data/user-stories/{detail_file.name}"

        validate_user_story(detail_story, context)

        if detail_id not in stories_by_id:
            fail(f"{context}: id {detail_id} does not exist in data/user-stories.json")
            continue

        aggregate_story = stories_by_id[detail_id]
        if detail_story != aggregate_story:
            fail(f"{context}: content mismatch with aggregate entry for id {detail_id}")

    if errors:
        print("Data validation failed:")
        for entry in errors:
            print(f"- {entry}")
        return 1

    print("Data validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
