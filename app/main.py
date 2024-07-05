import sys

def check_command(user_input):
    return f"{user_input}: command not found"

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_input = input()
        output = check_command(user_input)
        sys.stdout.write(f"{output}\n")
    

if __name__ == "__main__":
    main()
