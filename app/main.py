import os
import sys
import shutil
import subprocess

BUILTINS = ["type", "echo", "cd", "pwd", "exit"]

def check_command(user_command):
    command, *args = user_command.split(" ")
    match command:
        case "type":
            path = shutil.which(*args)
            if args[0] in BUILTINS:
                return f"{args[0]} is a shell builtin"
            elif path is None:
                return f"{args[0]}: not found"
            else:
                return f"{args[0]} is {path}"
        case "echo":
            return " ".join(args)
        case "cd":
            if len(args) == 0:
                return "cd: missing argument"
            try:
                os.chdir(args[0])
            except FileNotFoundError:
                return f"cd: {args[0]}: No such file or directory"
            except NotADirectoryError:
                return f"cd: {args[0]}: Not a directory"
            except PermissionError:
                return f"cd: {args[0]}: Permission denied"
            except Exception as e:
                return f"cd: {args[0]}: {e}"
            return None
        case "pwd":
            return os.getcwd()
        case "exit":
            sys.exit()
        case _:
            if shutil.which(command):
                subprocess.run([command, *args])
                return None
            return f"{user_command}: command not found"
    

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_command = input()
        output = check_command(user_command)
        if output is not None:
            sys.stdout.write(f"{output}\n")
    

if __name__ == "__main__":
    main()
