import os

def main():
    my_input = os.environ["INPUT_NAME"]

    my_output = f"Hello {my_input}"

    print(os.environ["RUNNER_TEMP"])
    print(my_output)


if __name__ == "__main__":
    main()