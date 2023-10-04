import os, sys, re
# Create by Joe, Simon, and ChatGPT

def search_and_sort_files(directory_path, search_string):
    # List all files in the directory that start with the search string
    matching_files = [f for f in os.listdir(directory_path) if f.startswith(search_string) and os.path.isfile(os.path.join(directory_path, f))]
    
    # Sort the files based on the counter suffix
    sorted_files = sorted(matching_files, key=lambda x: int(re.search(r'(\d+)', x).group(1)) if re.search(r'(\d+)', x) else 0)
    
    return sorted_files

def rename_files_in_directory(input_structure, directory_path, padding=4, start_int=0, search=""):
    if not isinstance(input_structure, str):
        raise ValueError('input_structure must be a string')
        
    if not os.path.isdir(directory_path):
        raise ValueError('directory_path must be a valid directory')

    renamed_files = []
    all_files = []
    if search != "":
        all_files = search_and_sort_files(directory_path, search)
    else:
        all_files = os.listdir(directory_path)
    

    for file_name in all_files:
        if os.path.isfile(os.path.join(directory_path, file_name)): # check if it's a file
            name_parts = file_name.split('.')
            if len(name_parts) < 2:
                continue # skip files without extensions
                
            base_name, extension = '.'.join(name_parts[:-1]), name_parts[-1]
            new_file_name = "{0}_{1}.{2}".format(input_structure, str(start_int).zfill(padding), extension)
            os.rename(
                os.path.join(directory_path, file_name), 
                os.path.join(directory_path, new_file_name)
            ) # ensure that necessary permissions are available

            renamed_files.append(new_file_name)
            start_int += 1
            
    return renamed_files

def print_usage():
    print("Usage: python script_name.py input_structure directory_path [counter] [padding]")
    print("\nParameters:")
    print("  input_structure: The prefix for the renamed files.")
    print("  directory_path: The path to the directory containing files to be renamed.")
    print("  counter: (Optional) The starting counter for renaming. Default is 0.")
    print("  padding: (Optional) The number of digits for padding the counter. Default is 4.")
    print("  search: (Optional) The prefix string of filenames to filter/search for within the directory.")
    print("\nExample usage: Renamer.exe \"NewFileName\" \"Direcory\\Path\"")
    print("\nFlags:")
    print("  -h, --help: Display this help message and exit.")

if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print_usage()
        sys.exit(0)
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    input_structure = sys.argv[1]
    directory_path = sys.argv[2]
    padding = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    start_int = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    search = sys.argv[5] if len(sys.argv) > 5 else ""

    renamed_files = rename_files_in_directory(input_structure, directory_path, padding, start_int, search)
    print(f"Renamed files: {renamed_files}")
