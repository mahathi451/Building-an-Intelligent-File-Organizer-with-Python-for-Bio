from organizer.core import FileOrganizer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Directory to organize")
args = parser.parse_args()

organizer = FileOrganizer(args.path)
organizer.organize()

print("Organization complete. Actions taken:")
for entry in organizer.log:
    print(f"- {entry}")
