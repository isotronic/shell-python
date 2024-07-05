import sys

available_command = ["type", "echo", "exit"]

def check_command(user_command):
    command = user_command.split(" ", 1)[0]
    argument = user_command.split(" ", 1)[1] if " " in user_command else None
    match command:
        case "type":
            if argument in available_command:
                return f"{argument} is a shell builtin"
            else:
                return f"{argument}: not found"
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
