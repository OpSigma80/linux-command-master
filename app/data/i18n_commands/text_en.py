"""Traducciones EN -- categoria "text" (Lectura y Manipulacion de Texto)."""

COMMAND_EN: dict[str, dict] = {
    "cat": {
        "description": "Shows the full content of one or more files.",
        "syntax": "cat file",
        "when_to_use": "View short files or concatenate several files together.",
    },
    "less": {
        "description": "Paginated file viewer, lets you navigate and search without loading everything into memory.",
        "syntax": "less file",
        "examples": ["less file.log", "less +F file.log  # like tail -f"],
        "when_to_use": "View large files or logs interactively.",
        "options": ["/pattern (search)", "q (quit)", "+F (follow live)"],
    },
    "more": {
        "description": "Simple paginated viewer, predecessor of less.",
        "syntax": "more file",
        "when_to_use": "When less isn't available; in general, use less instead.",
    },
    "head": {
        "description": "Shows the first lines of a file.",
        "syntax": "head [-n N] file",
        "examples": ["head file.txt", "head -n 20 file.log"],
        "when_to_use": "Quickly inspect the start of a file.",
    },
    "tail": {
        "description": "Shows the last lines of a file, with the option to follow it live.",
        "syntax": "tail [-n N] [-f] file",
        "examples": ["tail -n 50 file.log", "tail -f app.log"],
        "when_to_use": "Monitor logs in real time with -f.",
        "options": ["-f (follow live)", "-n (number of lines)"],
    },
    "vim": {
        "description": "Advanced modal text editor (normal/insert/visual modes).",
        "syntax": "vim file",
        "examples": ["vim script.sh", ":wq (save and quit)", ":q! (quit without saving)"],
        "when_to_use": "Quick editing over SSH or in scripts, without a graphical environment.",
        "options": ["i (insert)", "Esc (normal mode)", ":wq", ":q!", "dd (delete line)"],
    },
    "nano": {
        "description": "Simple terminal text editor, with shortcuts shown on screen.",
        "syntax": "nano file",
        "when_to_use": "Quick edits when you don't need vim's power (or its learning curve).",
        "options": ["Ctrl+O (save)", "Ctrl+X (quit)"],
    },
    "wc": {
        "description": "Counts lines, words or characters in a file or input.",
        "syntax": "wc [-l|-w|-c] file",
        "examples": ["wc -l file.txt", "cat log.txt | wc -l"],
        "when_to_use": "Count lines in a file or in another command's output.",
        "options": ["-l (lines)", "-w (words)", "-c (bytes)"],
    },
    "sort": {
        "description": "Sorts lines of text alphabetically or numerically.",
        "syntax": "sort [options] file",
        "options": ["-n (numeric)", "-r (reverse)", "-u (unique)"],
        "when_to_use": "Sort output before applying uniq, or for reports.",
    },
    "uniq": {
        "description": "Removes or counts consecutive duplicate lines.",
        "syntax": "uniq [-c] file",
        "when_to_use": "Requires sorted input first (combine it with sort).",
        "options": ["-c (count repetitions)"],
    },
    "cut": {
        "description": "Extracts columns or fields from lines of text.",
        "syntax": "cut -d'delimiter' -fN file",
        "examples": ["cut -d',' -f1 data.csv", "cut -c1-5 file.txt"],
        "when_to_use": "Extract a specific column from a CSV or delimited text.",
    },
    "tr": {
        "description": "Translates or deletes characters from standard input.",
        "syntax": "tr 'set1' 'set2'",
        "examples": ["echo hello | tr 'a-z' 'A-Z'", "cat a.txt | tr -d ' '"],
        "when_to_use": "Simple character transformations (uppercase, removing spaces).",
    },
    "paste": {
        "description": "Merges lines from several files into columns.",
        "syntax": "paste file1 file2",
        "examples": ["paste names.txt ages.txt"],
        "when_to_use": "Join columns from different files line by line.",
    },
    "join": {
        "description": "Joins lines from two sorted files based on a common field.",
        "syntax": "join file1 file2",
        "examples": ["join users.txt roles.txt"],
        "when_to_use": "Combine data like a SQL 'JOIN' between two sorted text files.",
    },
    "column": {
        "description": "Formats text into aligned, readable columns.",
        "syntax": "column -t file",
        "examples": ["cat data.csv | column -t -s,"],
        "when_to_use": "Show tabular data legibly in the terminal.",
    },
    "awk": {
        "description": "Text-processing language oriented around columns/records.",
        "syntax": "awk 'pattern {action}' file",
        "examples": ["awk '{print $1}' file.txt", "awk -F',' '{print $2}' data.csv"],
        "when_to_use": "Structured text processing: extract, sum or transform columns.",
    },
    "sed": {
        "description": "Stream editor for finding and replacing text without opening an editor.",
        "syntax": "sed 's/find/replace/' file",
        "examples": ["sed 's/error/ERROR/g' log.txt", "sed -i 's/foo/bar/g' file.txt"],
        "when_to_use": "Automated replacements in files, useful in scripts.",
        "options": ["-i (in-place edit)", "g (global on the line)"],
        "precautions": "With -i it overwrites the original file; use -i.bak to keep a copy.",
    },
    "diff": {
        "description": "Compares two files line by line and shows the differences.",
        "syntax": "diff file1 file2",
        "examples": ["diff v1.txt v2.txt", "diff -u v1.txt v2.txt > changes.patch"],
        "when_to_use": "Compare file versions or generate a patch.",
        "options": ["-u (unified format, used by git)"],
    },
    "patch": {
        "description": "Applies a diff file (patch) generated by diff.",
        "syntax": "patch file < changes.patch",
        "examples": ["patch file.txt < changes.patch"],
        "when_to_use": "Apply changes generated with diff -u to a file.",
    },
    "grep": {
        "description": "Searches for patterns (text or regular expressions) inside files or a stream.",
        "syntax": "grep [options] pattern file",
        "examples": ["grep 'error' log.txt", "grep -i 'error' log.txt", "grep -R 'TODO' ./project"],
        "when_to_use": "Find lines that contain a pattern, in a file or in another command's output.",
        "options": ["-i (ignore case)", "-r/-R (recursive)", "-n (line number)", "-v (invert)", "-E (extended regex)"],
    },
    "tee": {
        "description": "Sends output simultaneously to the screen and to a file.",
        "syntax": "command | tee file",
        "examples": ["echo hello | tee output.txt", "command | tee -a log.txt"],
        "when_to_use": "See the result on screen while saving it to a file, useful in scripts.",
        "options": ["-a (append)"],
    },
    "xargs": {
        "description": "Builds and runs commands taking arguments from standard input.",
        "syntax": "command | xargs [command2]",
        "examples": ["find . -name '*.log' | xargs rm", "cat list.txt | xargs -I{} echo {}"],
        "when_to_use": "When a command doesn't accept input via stdin but does as arguments (e.g: find + rm).",
        "options": ["-I{} (placeholder)", "-n (n args per call)"],
        "precautions": "Combined with rm/find it can be destructive; test first with 'echo' instead of the real command.",
    },
    "redirections": {
        "name": "Redirections and pipes (>, >>, <, 2>, |)",
        "description": (
            "Shell operators to control stdin/stdout/stderr: "
            "'>' overwrites, '>>' appends, '<' reads from a file, '2>' redirects "
            "errors, '|' connects one command's output to another's input."
        ),
        "syntax": "command > file | command2",
        "examples": [
            "echo hello > output.txt",
            "echo hello >> output.txt",
            "command 2> errors.log",
            "command 2>&1",
            "ls -la | grep '.txt'",
        ],
        "when_to_use": "The foundation of all shell scripting and automation.",
    },
}
