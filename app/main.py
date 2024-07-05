import sys
import shutil
import subprocess

AVAILABLE_COMMANDS = ["type", "echo", "exit"]

def check_command(user_command):
    command, *args = user_command.split(" ")
    match command:
        case "type":
            path = shutil.which(*args)
            if args[0] in AVAILABLE_COMMANDS:
                return f"{args[0]} is a shell builtin"
            elif path is None:
                return f"{args[0]}: not found"
            else:
                return f"{args[0]} is {path}"
        case "echo":
            return " ".join(args)
        case "exit":
            sys.exit()
        case _:
            if shutil.which(command):
                subprocess.run([command, *args])
                return
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
