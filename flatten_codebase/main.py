import os
import argparse

def printFolderStructure(directory, output_file):
    output_file.write(f"### DIRECTORY {directory} FOLDER STRUCTURE ###\n")
    for root, directories, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output_file.write('{}{}/\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            output_file.write('{}{}\n'.format(subindent, f))
    output_file.write(f"### DIRECTORY {directory} FOLDER STRUCTURE ###\n\n")

def walkFolderTree(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

def main():
    parser = argparse.ArgumentParser(description='Flattens a codebase.')
    parser.add_argument('--folders', nargs='+', required=True, help='Base folders to process')
    
    args = parser.parse_args()
    base_folders = args.folders
    
    with open('codebase.md', 'w') as output_file:
        for base_folder in base_folders:
            printFolderStructure(base_folder, output_file)
            
            output_file.write(f"### DIRECTORY {base_folder} FLATTENED CONTENT ###\n")
            for filepath in walkFolderTree(base_folder):
                content = f"### {filepath} BEGIN ###\n"
                
                try:
                    with open(filepath, "r") as f:
                        content += f.read()
                    content += f"\n### {filepath} END ###\n\n"
                except:
                    continue
                
                output_file.write(content)
            output_file.write(f"### DIRECTORY {base_folder} FLATTENED CONTENT ###\n")

if __name__ == "__main__":
    main()