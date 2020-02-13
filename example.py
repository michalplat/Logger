import Logger


logger = Logger.Logger(log_file="output.txt")
with Logger.context_logger(logger):  # redirect stdout to logger object
	print("output from main process")
	Logger.run_subprocess(["python3", "example_to_subprocess.py"])
