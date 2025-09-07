# DiffAnalyzer
This tool clones a repo, analyzes its tags based on your preference (customizable), and stores all the differences per-file in `result.json` which is created in the same folder as the main python file: `analyzer.py`.

---
## How to use:
At the bottom of the script is a function call commented out, simply uncomment it and pass the wanted GitHub repository link as a string.

---
## Features:
- `is_valid_tag`: validates the tags, by default it avoids betas, alphas, prereleases and dev releases.
- `is_valid_file`: validates the file, by default it avoids files starting with a period ('.').
---
## Notes:
- This script clones the provided repository locally, in windows that's `C:\Users\<USER>\AppData\Local\Temp\repo_clone_...`, if an exception occurs while the script is running, this folder might not be removed accordingly.
- This script was made to help me figure when things were added and what was added after each update; though it works for me, I cannot guarantee that it won't cause problems on your end, if you have any doubts about the code, just read it, it's pretty straightforward and fast.