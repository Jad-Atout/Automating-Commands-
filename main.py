from Connections import ScriptExecutor
import argparse
def main():
    parser = argparse.ArgumentParser(description="Script Executor")
    parser.add_argument("-i", required=True, help="Input script file")
    parser.add_argument("-o", required=True, help="Output result file")
    argument = parser.parse_args()
    executor = ScriptExecutor("./config.json",argument.i,argument.o)
    executor.execute_commands()
    executor.results_writer()

if __name__ == "__main__":

    main()
