from bs4 import BeautifulSoup
import json
import csv
import os
import statistics
import re

def read_html_file(file_name, file_path):
    with open(f"{file_path}/{file_name}", 'r', encoding='utf-8') as file:
        return file.read()

def get_d4j_subject_classes():
    d4j_subjects = {}
    try:
        with open('./evaluation/data/class_list.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                project_name = row[0]
                class_name = row[1]
                max_cc = row[2]
                if d4j_subjects.get(project_name):
                    d4j_subjects.get(project_name)[class_name] = max_cc
                else:
                    d4j_subjects[project_name] = {class_name: max_cc}
    except Exception as e:
        print(f"Error reading class_list.csv: {e}")
    return d4j_subjects

def parse_line_branch_coverage(class_name: str, prompt_type: str, file_path, model="qwen3-coder:30b"):
    """
    parse HTML files to identify line/branch coverage
    """
    try:
        coverage = []
        html_file = f"{class_name}_{prompt_type}_test_results.html"

        # Handle the case where prompt_type might not match exactly
        # This happens with the second directory where some files have different naming
        if not os.path.exists(os.path.join(file_path, html_file)):
            # Try to find any HTML file that starts with the class name
            for file in os.listdir(file_path):
                if file.startswith(class_name) and file.endswith('.html'):
                    html_file = file
                    break
            else:
                # No file found
                return coverage

        html_content = read_html_file(html_file, file_path)
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the table in the HTML content
        table = soup.find('table')

        if not table:
            return coverage

        # Iterate over the rows of the table (skip the header row)
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 6:
                continue  # Skip rows that do not have enough columns

            # Extract details
            status = columns[0].text.strip()
            label = columns[1].text.strip()
            reason = columns[2].text.strip()
            line_coverage = float(columns[4].text.strip())
            branch_coverage = float(columns[5].text.strip())

            # Store coverage data in the dictionary
            coverage.append({
                "label": label,
                "status": status,
                "reason": reason,
                "line_coverage": line_coverage,
                "branch_coverage": branch_coverage
            })
        return coverage
    except Exception as e:
        print(f"Error parsing {class_name}: {e}")
        return []

def main():
    # Configuration
    prompt_type = "control"

    # Directory paths for the two models
    dir_model1 = "./result-files/control_ollama/qwen3-coder:30b"
    dir_model2 = "./result-files/control_ollama/qwen3-coder:30b-a3b-q8_0_constraints_mcts"

    # Model names for output
    model1_name = "qwen3-coder:30b"
    model2_name = "qwen3-coder:30b-q8_0_constraints_mcts"

    # Output CSV file
    output_csv = "qwen3_coverage_comparison.csv"

    # Get project and class information
    d4j_subject_classes = get_d4j_subject_classes()

    # Create header
    header = ["project", "class_name",
              "max_complexity",
              f"{model1_name}_last_line_coverage", f"{model1_name}_last_branch_coverage",
              f"{model2_name}_last_line_coverage", f"{model2_name}_last_branch_coverage"]

    # Create CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    # Get all HTML files from model1 directory
    model1_files = [f for f in os.listdir(dir_model1) if f.endswith('.html')]

    # Process each class
    for file in model1_files:
        # Extract class name from the filename
        match = re.match(r'^([^_]+)_control_', file)
        if match:
            class_name = match.group(1)

            # Find which project this class belongs to
            project_name = None
            max_cc = None
            for proj in d4j_subject_classes:
                if class_name in d4j_subject_classes[proj]:
                    project_name = proj
                    max_cc = d4j_subject_classes[proj][class_name]
                    break

            # If project not found, continue (it might not be a Defects4J subject)
            if not project_name:
                continue

            # Parse coverage for both models
            model1_coverage = parse_line_branch_coverage(class_name, prompt_type, dir_model1)
            model2_coverage = parse_line_branch_coverage(class_name, prompt_type, dir_model2)

            # Get last coverage values (last iteration)
            model1_last_line = model1_coverage[-1]["line_coverage"] if model1_coverage else None
            model1_last_branch = model1_coverage[-1]["branch_coverage"] if model1_coverage else None

            model2_last_line = model2_coverage[-1]["line_coverage"] if model2_coverage else None
            model2_last_branch = model2_coverage[-1]["branch_coverage"] if model2_coverage else None

            # Write to CSV
            row = [project_name, class_name, max_cc,
                   model1_last_line, model1_last_branch,
                   model2_last_line, model2_last_branch]

            with open(output_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)

    print(f"Analysis complete. Results saved to {output_csv}")

    # Optional: Calculate average coverages for both models
    calculate_averages(output_csv)

def calculate_averages(csv_file):
    """
    Calculate average line and branch coverage for both models
    """
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        # Find column indices
        model1_line_idx = header.index([col for col in header if 'qwen3-coder:30b_last_line_coverage' in col][0])
        model1_branch_idx = header.index([col for col in header if 'qwen3-coder:30b_last_branch_coverage' in col][0])
        model2_line_idx = header.index([col for col in header if 'qwen3-coder:30b-q8_0_constraints_mcts_last_line_coverage' in col][0])
        model2_branch_idx = header.index([col for col in header if 'qwen3-coder:30b-q8_0_constraints_mcts_last_branch_coverage' in col][0])

        # Collect valid coverage values
        model1_lines = []
        model1_branches = []
        model2_lines = []
        model2_branches = []

        for row in reader:
            if row[model1_line_idx]:
                model1_lines.append(float(row[model1_line_idx]))
            if row[model1_branch_idx]:
                model1_branches.append(float(row[model1_branch_idx]))
            if row[model2_line_idx]:
                model2_lines.append(float(row[model2_line_idx]))
            if row[model2_branch_idx]:
                model2_branches.append(float(row[model2_branch_idx]))

        # Calculate averages
        avg_model1_line = sum(model1_lines) / len(model1_lines) if model1_lines else 0
        avg_model1_branch = sum(model1_branches) / len(model1_branches) if model1_branches else 0
        avg_model2_line = sum(model2_lines) / len(model2_lines) if model2_lines else 0
        avg_model2_branch = sum(model2_branches) / len(model2_branches) if model2_branches else 0

        print(f"\nAverage Coverages:")
        print(f"Model: qwen3-coder:30b")
        print(f"  Average Line Coverage: {avg_model1_line:.2f}%")
        print(f"  Average Branch Coverage: {avg_model1_branch:.2f}%")
        print(f"\nModel: qwen3-coder:30b-q8_0_constraints_mcts")
        print(f"  Average Line Coverage: {avg_model2_line:.2f}%")
        print(f"  Average Branch Coverage: {avg_model2_branch:.2f}%")

        # Calculate improvement
        line_improvement = ((avg_model2_line - avg_model1_line) / avg_model1_line) * 100 if avg_model1_line != 0 else 0
        branch_improvement = ((avg_model2_branch - avg_model1_branch) / avg_model1_branch) * 100 if avg_model1_branch != 0 else 0

        print(f"\nImprovement:")
        print(f"  Line Coverage: {line_improvement:.2f}%")
        print(f"  Branch Coverage: {branch_improvement:.2f}%")

if __name__ == '__main__':
    main()