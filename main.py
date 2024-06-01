from Connections import ScriptExecutor
import argparse


def main():
    # Creating argparse object
    parser = argparse.ArgumentParser(description="Script Executor")
    # Adding arguments to the object
    parser.add_argument("-i", required=True, help="Input script file")
    parser.add_argument("-o", required=True, help="Output result file")
    # Parsing arguments
    argument = parser.parse_args()
    # Creating object from ScriptExecutor class
    executor = ScriptExecutor("./config.json", argument.i, argument.o)
    # Begin executing commands
    executor.execute_commands()
    # Writing output results
    executor.results_writer()


if __name__ == "__main__":
    main()
