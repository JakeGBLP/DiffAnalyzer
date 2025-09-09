import subprocess
import json
import tempfile
import os
import stat
import shutil

def _handle_readonly(func, path, execution_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run_git(command, cwd=None):
    output = subprocess.check_output(command, shell=True, text=True, cwd=cwd)
    return output.strip().splitlines()


SKIP_KEYWORDS = ("dev", "pre", "alpha", "beta")

def is_valid_tag(version: str) -> bool:
    version_lower = version.lower()
    for keyword in SKIP_KEYWORDS:
        if keyword in version_lower:
            return False
    return True

def is_valid_file(filename: str) -> bool:
    return not filename.startswith(".")


def process_repo(repo_url: str, output_file: str = "result.json"):
    temp_folder = tempfile.mkdtemp(prefix="repo_clone_")
    print(f"Cloning repository {repo_url} into {temp_folder}...")

    try:
        subprocess.run(f"git clone --mirror {repo_url} {temp_folder}", shell=True, check=True)
        print("Clone complete.")

        all_tags = run_git("git tag --sort=creatordate", cwd=temp_folder)
        tags = [tag for tag in all_tags if is_valid_tag(tag)]
        print(f"Found {len(tags)} stable tags to process.")

        result = {}

        for i, tag in enumerate(tags):
            print(f"Processing tag {tag} (index {i})", end="")
            if i == 0:
                print()
                files = run_git(f"git ls-tree -r --name-only {tag}", cwd=temp_folder)
                for f in files:
                    if not is_valid_file(f):
                        continue
                    result.setdefault(f, {"added": tag, "removed": None, "modified": []})
                continue

            prev_tag = tags[i - 1]
            print(f" and previous tag: {prev_tag}")

            changes = run_git(f"git diff --name-status {prev_tag} {tag}", cwd=temp_folder)
            for line in changes:
                if "\t" not in line:
                    continue
                status, path = line.split("\t", 1)
                if not is_valid_file(path):
                    continue

                if status == "A":
                    result.setdefault(path, {"added": tag, "removed": None, "modified": []})
                elif status == "D":
                    if path in result:
                        result[path]["removed"] = tag
                elif status == "M":
                    if path in result:
                        result[path]["modified"].append(tag)

        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result successfully saved to {output_file}.")

    finally:
        print(f"Removing temporary folder {temp_folder}...")
        shutil.rmtree(temp_folder, onerror=_handle_readonly)
        print("Temporary folder cleaned up.")

# Usage example:
process_repo("https://github.com/SkriptLang/Skript")
