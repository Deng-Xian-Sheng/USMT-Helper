import os

# List of directories to be traversed
directories = [
    r"D:\wim\Program Files",
    r"D:\wim\Program Files (x86)",
    r"D:\wim\Windows.old\Users\x1761\AppData\Roaming",
    r"D:\wim\Windows.old\Users\x1761\AppData\Local",
    r"D:\wim\Windows.old\Users\x1761\AppData\LocalLow"
]

# Iterate through each directory
for directory in directories:
    try:
        # List the contents of the directory
        with os.scandir(directory) as entries:
            for entry in entries:
                # Print the path of each item
                print(entry.path)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
    except PermissionError:
        print(f"Permission denied: {directory}")
