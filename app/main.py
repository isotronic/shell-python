import os
import sys
import shutil
import subprocess

BUILTINS = ["type", "echo", "cd", "pwd", "exit"]

def handle_type(*args):
    """Handles the 'type' command to identify if a command is built-in or external."""
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
    """Handles the 'echo' command to print arguments to stdout."""
    return " ".join(args)
    
def handle_cd(args):
    """Handles the 'cd' command to change the current working directory."""
    if len(args) == 0:
        return "cd: missing argument"
    try:
        # Expand '~' to the user home directory
        target_directory = os.path.expanduser(args[0])
        os.chdir(target_directory)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        return f"cd: {args[0]}: {e.strerror}"
    except Exception as e:
        return f"cd: {args[0]}: {e}"
    return None

def handle_pwd():
    """Handles the 'pwd' command to return the current working directory."""
    return os.getcwd()

def handle_exit():
    """Handles the 'exit' command to exit the shell."""
    sys.exit("Exiting...")
    
def handle_catchall(user_command, command, *args):
    """Handles external commands by attempting to execute them."""
    try:
        subprocess.run([command, *args], check=True)
        return None
    except subprocess.CalledProcessError as e:
        return f"{user_command}: command failed with error: {e}"
    except FileNotFoundError:
        return f"{user_command}: command not found"
    except Exception as e:
        return f"{user_command}: an error occurred: {e}"
    
COMMAND_HANDLERS = {
    "type": handle_type,
    "echo": handle_echo,
    "cd": handle_cd,
    "pwd": handle_pwd,
    "exit": handle_exit
}

def handle_command(user_command):
    """Parses and dispatches the user's command to the appropriate handler."""
    command, *args = user_command.strip().split(" ")
    handler = COMMAND_HANDLERS.get(command, handle_catchall)
    return handler(user_command, command, *args) if handler == handle_catchall else handler(*args)
    

def main():
    """Main loop of the shell, continuously accepting user input."""
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            user_command = input()
            output = handle_command(user_command)
            if output is not None:
                sys.stdout.write(f"{output}\n")
        except (KeyboardInterrupt, EOFError):
            sys.exit("Exiting...")
        except Exception as e:
            sys.stdout.write(f"An unexpected error occurred: {e}\n")
    

if __name__ == "__main__":
    main()
