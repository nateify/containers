#!/usr/bin/env python3
import argparse
import os
import pathlib
import re
import sys


def extract_vars(dockerfile_path: str) -> dict[str, str]:
    variables = {}
    with open(dockerfile_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            arg_match = re.match(r"^ARG\s+([A-Za-z0-9_]+)\s*=\s*[\"']?([^\"'\s#]+)[\"']?", line)
            if arg_match:
                key, val = arg_match.groups()
                variables[key] = re.sub(r"^v", "", val)

            from_match = re.match(r"^FROM\s+([a-zA-Z0-9_\-\./]+):([a-zA-Z0-9_\-\.]+)", line)
            if from_match:
                img_name, img_tag = from_match.groups()
                clean_name = img_name.split("/")[-1].split(":")[0].upper().replace("-", "_")
                variables[clean_name] = re.sub(r"^v", "", img_tag)

    # Automatically generate *_SHORT for hyphenated build tag
    short_pattern = re.compile(r"^v?(\d+(?:\.\d+)+)(?:[-+].*)?$", re.IGNORECASE)
    for k, v in list(variables.items()):
        match = short_pattern.match(v)
        if match:
            variables[f"{k}_SHORT"] = match.group(1)

    return variables


def main():
    parser = argparse.ArgumentParser(description="Resolve container tags from a Dockerfile template.")
    parser.add_argument("--dockerfile", required=True, help="Path to the Dockerfile")
    parser.add_argument("--template", required=True, help="Template string, e.g. '{VERSION}'")
    args = parser.parse_args()

    if not pathlib.Path(args.dockerfile).exists():
        sys.exit(f"Error: Dockerfile not found at {args.dockerfile}")

    variables = extract_vars(args.dockerfile)

    try:
        tag = args.template.format(**variables)
    except KeyError as e:
        sys.exit(
            f"Error: Template requested {e}, but it was not found in {args.dockerfile}.\n"
            f"Available variables: {list(variables.keys())}"
        )

    print(tag)

    gh_output = os.getenv("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write(f"tag={tag}\n")


if __name__ == "__main__":
    main()
