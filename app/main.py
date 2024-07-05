import os
import sys
import shutil
import subprocess

BUILTINS = ["type", "echo", "cd", "pwd", "exit"]

def handle_type(*args):
    if not args:
        return "type: missing argument"
    path = shutil.which(*args)
    if args[0] in BUILTINS:
        return f"{args[0]} is a shell builtin"
    elif path is None:
        return f"{args[0]}: not found"
    else:
        return f"{args[0]} is {path}"
    
def handle_echo(args):
    return " ".join(args)
    
def handle_cd(args):
    if len(args) == 0:
        return "cd: missing argument"
    try:
        if args[0] == "~":
            os.chdir(os.path.expanduser(args[0]))
        else:
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

def handle_pwd():
    return os.getcwd()

def handle_exit():
    sys.exit()
    
def handle_catchall(user_command, command, *args):
    try:
        subprocess.run([command, *args], check=True)
        return None
    except subprocess.CalledProcessError as e:
        return f"{user_command}: command failed with error: {e}"
    except FileNotFoundError:
        return f"{user_command}: command not found"
    except Exception as e:
        return f"{user_command}: an error occurred: {e}"

def handle_command(user_command):
    command, *args = user_command.split(" ")
    match command:
        case "type":
            return handle_type(*args)
        case "echo":
            return handle_echo(args)
        case "cd":
            return handle_cd(args)
        case "pwd":
            return handle_pwd()
        case "exit":
            handle_exit()
        case _:
            return handle_catchall(user_command, command, *args)
    

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_command = input()
        output = handle_command(user_command)
        if output is not None:
            sys.stdout.write(f"{output}\n")
    

if __name__ == "__main__":
    main()
