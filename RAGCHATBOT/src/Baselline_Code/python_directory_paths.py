import os
from pathlib import Path


# Get the current working directory as a string
current_directory = os.getcwd()

# Print the result
print("Current working directory:", current_directory)



script_directory = os.path.dirname(os.path.abspath(__file__))
print("Script file directory:", script_directory)





# Using os module
script_directory_os = os.path.dirname(os.path.abspath(__file__))
print("Script directory (os):", script_directory_os)

# Using pathlib module (Python 3.9+ consistently provides absolute paths)
script_directory_pathlib = Path(__file__).parent.resolve()
print("Script directory (pathlib):", script_directory_pathlib)

# Using os module
data_directory_path = os.path.dirname(os.path.abspath(__file__))
print("data directory (data):", data_directory_path)

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the directory name from the script path
script_dir = os.path.dirname(script_path)

# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))

print(f"Script path: {script_path}")
print("=="*20)
print(f"Parent directory: {parent_directory}")
print("=="*20)
data_directory_path = os.path.join(parent_directory, "data")
print(f"Data directory path: {data_directory_path}")
print("=="*20)
