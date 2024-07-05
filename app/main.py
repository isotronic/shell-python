import sys
import shutil

AVAILABLE_COMMANDS = ["type", "echo", "exit"]

def check_command(user_command):
    command = user_command.split(" ", 1)[0]
    argument = user_command.split(" ", 1)[1] if " " in user_command else None
    match command:
        case "type":
            path = shutil.which(argument)
            if argument in AVAILABLE_COMMANDS:
                return f"{argument} is a shell builtin"
            elif path is None:
                return f"{argument}: not found"
            else:
                return f"{argument} is {path}"
        case "echo":
            return argument
        case "exit":
            sys.exit()
        case _:
            return f"{user_command}: command not found"
    

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_command = input()
        output = check_command(user_command)
        sys.stdout.write(f"{output}\n")
    

if __name__ == "__main__":
    main()
