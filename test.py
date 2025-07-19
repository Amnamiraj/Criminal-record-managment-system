import os

# List of all file names
files = [
    "base.html", "index.html", "criminals.html", "add_criminal.html", "edit_criminal.html",
    "crimes.html", "add_crime.html", "firs.html", "add_fir.html", "officers.html", "add_officer.html",
    "victims.html", "add_victim.html", "suspects.html", "add_suspect.html", "evidence.html",
    "add_evidence.html", "reports.html", "add_report.html", "court_cases.html", "add_court_case.html",
    "witnesses.html", "add_witness.html", "search.html"
]

# Directory to hold the templates
templates_dir = "templates"

# Create the directory if it doesn't exist
os.makedirs(templates_dir, exist_ok=True)

# Create each file inside the templates directory
for file in files:
    file_path = os.path.join(templates_dir, file)
    with open(file_path, "w") as f:
        f.write(f"<!-- {file} -->")  # Placeholder content
    print(f"Created: {file_path}")
