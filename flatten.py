import os
import argparse
import pathlib

def should_skip_path(path, skip_folders):
    """
    Check if the path contains any folder that should be skipped.
    """
    if not skip_folders:
        return False
    
    # Convert path to normalized absolute path
    path_obj = pathlib.Path(path).resolve()
    path_parts = path_obj.parts
    
    # Check if any part of the path matches a folder to skip
    return any(skip_folder in path_parts for skip_folder in skip_folders)

def printFolderStructure(directory, output_file, skip_folders=None):
    output_file.write(f"### DIRECTORY {directory} FOLDER STRUCTURE ###\n")
    
    # Get the absolute path for the directory
    abs_directory = os.path.abspath(directory)
    
    for root, dirs, files in os.walk(directory):
        # Check if the current path should be skipped
        if should_skip_path(root, skip_folders):
            # Remove all directories to prevent further traversal
            dirs.clear()
            continue
        
        # Filter out directories that should be skipped before recursing into them
        i = 0
        while i < len(dirs):
            dir_path = os.path.join(root, dirs[i])
            if should_skip_path(dir_path, skip_folders):
                dirs.pop(i)
            else:
                i += 1
        
        # Calculate indentation level
        rel_path = os.path.relpath(root, directory)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
        indent = ' ' * 4 * level
        
        # Write directory name
        if level == 0:
            output_file.write('{}{}/\n'.format(indent, os.path.basename(directory)))
        else:
            output_file.write('{}{}/\n'.format(indent, os.path.basename(root)))
        
        # Write file names
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            output_file.write('{}{}\n'.format(subindent, f))
    
    output_file.write(f"### DIRECTORY {directory} FOLDER STRUCTURE ###\n\n")

def walkFolderTree(folder, skip_folders=None):
    for root, dirs, files in os.walk(folder):
        # Check if the current path should be skipped
        if should_skip_path(root, skip_folders):
            # Remove all directories to prevent further traversal
            dirs.clear()
            continue
        
        # Filter out directories that should be skipped before recursing into them
        i = 0
        while i < len(dirs):
            dir_path = os.path.join(root, dirs[i])
            if should_skip_path(dir_path, skip_folders):
                dirs.pop(i)
            else:
                i += 1
        
        # Yield all files in this directory
        for filename in files:
            yield os.path.join(root, filename)

def main():
    parser = argparse.ArgumentParser(description='Flattens a codebase.')
    parser.add_argument('--folders', nargs='*', help='Base folders to process')
    parser.add_argument('--skip-folders', nargs='*', default=[], help='Folders to skip during processing')
    parser.add_argument('--system_instructions', action='store_true', help='Print system instructions')
    parser.add_argument('--output', default='codebase.md', help='Output file name (default: codebase.md)')
    
    system_instructions = """## System Instructions for Language Model Assistance in Code Debugging
### Codebase Markdown File Structure:
- The codebase markdown file represents the actual codebase structure and content.
- It begins with a directory tree representation:
  ```
  ### DIRECTORY path/to/file/tree FOLDER STRUCTURE ###
  (file tree representation)
  ### DIRECTORY path/to/file/tree FOLDER STRUCTURE ###
  ```
- Following the directory tree, the contents of each file are displayed:
  ```
  ### path/to/file1 BEGIN ###
  (content of file1)
  ### path/to/file1 END ###
  
  ### path/to/file2 BEGIN ###
  (content of file2)
  ### path/to/file2 END ###
  ```
### Guidelines for Interaction:
- Respond to queries based on the explicit content provided within the markdown file.
- Avoid making assumptions about the code without clear evidence presented in the file content.
- When seeking specific implementation details, refer to the corresponding section in the markdown file, for example:
  ```
  ### folder1/folder2/myfile.ts BEGIN ###
  (specific implementation details)
  ### folder1/folder2/myfile.ts END ###
  ```
### Objective:
- The primary objective is to facilitate understanding of codebase by providing accurate information and guidance strictly adhering to the content available in the markdown file."""

    args = parser.parse_args()
    
    if args.system_instructions:
        print(system_instructions)
        if not args.folders:
            return
    
    if args.folders:
        base_folders = args.folders
        skip_folders = args.skip_folders
        
        with open(args.output, 'w', encoding='utf-8') as output_file:
            for base_folder in base_folders:
                printFolderStructure(base_folder, output_file, skip_folders)
                
                output_file.write(f"### DIRECTORY {base_folder} FLATTENED CONTENT ###\n")
                for filepath in walkFolderTree(base_folder, skip_folders):
                    content = f"### {filepath} BEGIN ###\n"
                    
                    try:
                        with open(filepath, "r", encoding='utf-8', errors='replace') as f:
                            content += f.read()
                        content += f"\n### {filepath} END ###\n\n"
                    except Exception as e:
                        # Better error handling
                        content += f"[Error reading file: {str(e)}]\n"
                        content += f"### {filepath} END ###\n\n"
                    
                    output_file.write(content)
                output_file.write(f"### DIRECTORY {base_folder} FLATTENED CONTENT ###\n")
    else:
        print("usage: main.py [-h] --folders FOLDERS [FOLDERS ...] [--skip-folders SKIP_FOLDERS [SKIP_FOLDERS ...]] [--system_instructions] [--output OUTPUT]")
        print("Error: the following arguments are required: --folders")

if __name__ == "__main__":
    main()
