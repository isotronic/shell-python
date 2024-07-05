import sys

def check_command(user_command):
    match user_command:
        case s if s.startswith("exit"):
            exit()
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
