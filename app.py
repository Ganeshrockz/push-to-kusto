import os

def main():
    my_input = os.environ["INPUT_NAME"]

    my_output = f"Hello {my_input}"

    file_name = "sample.txt"
    file_path = os.path.join(os.environ["RUNNER_TEMP"], file_name)

    f = open(file_path, "w")
    f.write("sample")
    f.close()

    f = open(file_path, "r")
    print(f.read())
    print(my_output)


if __name__ == "__main__":
    main()