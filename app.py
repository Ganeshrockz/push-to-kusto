import os

def main():
    my_input = os.environ["INPUT_NAME"]

    my_output = f"Hello {my_input}"

    print(my_output)


if __name__ == "__main__":
    print("Into main")
    main()