# Shell tricks

There are several command line incantations that I have had to look up
at least a dozen times. I'm compiling a handy cheat sheet of them here. 

These commands all work on my Mac, in the Terminal app running the shell zsh.
I think most of them are directly portable to bash, but some will have
small differences.

To drill deeper on any of these run `man <command>`. I find the examples
section at the end most helpful.

## Finding a string in Python files

```
grep -r --include \*.py 'string I am looking for' .
```

- `grep` finds strings
- `-r` drills down into directories recursively
- `--include \*.py` only checks files whose names end in `.py`
- `'string I am looking for` is the string to look for
- `.` signals to start looking in the current directory

## Find files by name

```
find . -name '&ast;partial_name&ast;'
```

- `find` finds files and directories recursively
- `.` says to start in the current directory and work down
- `-name '&ast;partial_name&ast;'` is an instruction to find anything that has
  the string "partial_name" anywhere in its name.

## Find and replace all occurrences of a string in a directory's Python files

```
sed -i '.bak' -e 's/old string/new string/g' *.py
```

- `sed` (stream editor) is a command to modify text
- `-i '.bak'` creates a backup copy of every modified file, using the extension
   `.bak`. If you want to live dangerously you can skip backups by specitying
   `-i ''`.
- `-e` instructs it to execute the command that follows
- `'s/old string/new string/g'` says to swap (`s`) the 
    string `old string` for the string `new string` 
    everywhere in the file, even if it occurs multiple times on the same
    line (`g`)
- `*.py` says to do this for all Python files in the directory.


