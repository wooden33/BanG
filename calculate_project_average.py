import csv
import os

def calculate_project_averages(input_csv):
    """
    Calculate per-project average line and branch coverage for both models
    """
    project_data = {}

    # Read input CSV
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        # Get column indices
        project_idx = header.index('project')
        model1_line_idx = header.index([col for col in header if 'qwen3-coder:30b_last_line_coverage' in col][0])
        model1_branch_idx = header.index([col for col in header if 'qwen3-coder:30b_last_branch_coverage' in col][0])
        model2_line_idx = header.index([col for col in header if 'qwen3-coder:30b-q8_0_constraints_mcts_last_line_coverage' in col][0])
        model2_branch_idx = header.index([col for col in header if 'qwen3-coder:30b-q8_0_constraints_mcts_last_branch_coverage' in col][0])

        # Process each row
        for row in reader:
            project = row[project_idx]

            # Get coverage values, converting to float if not empty
            model1_line = float(row[model1_line_idx]) if row[model1_line_idx] else None
            model1_branch = float(row[model1_branch_idx]) if row[model1_branch_idx] else None
            model2_line = float(row[model2_line_idx]) if row[model2_line_idx] else None
            model2_branch = float(row[model2_branch_idx]) if row[model2_branch_idx] else None

            # Initialize project data if not exists
            if project not in project_data:
                project_data[project] = {
                    'model1_lines': [],
                    'model1_branches': [],
                    'model2_lines': [],
                    'model2_branches': [],
                    'class_count': 0
                }

            # Add coverage values to project data if they exist
            if model1_line is not None:
                project_data[project]['model1_lines'].append(model1_line)
            if model1_branch is not None:
                project_data[project]['model1_branches'].append(model1_branch)
            if model2_line is not None:
                project_data[project]['model2_lines'].append(model2_line)
            if model2_branch is not None:
                project_data[project]['model2_branches'].append(model2_branch)

            # Increment class count
            project_data[project]['class_count'] += 1

    # Output results
    output_csv = 'qwen3_project_average_coverage.csv'

    # Create output header
    output_header = ['project', 'class_count',
                   'qwen3-coder:30b_avg_line_coverage', 'qwen3-coder:30b_avg_branch_coverage',
                   'qwen3-coder:30b-q8_0_constraints_mcts_avg_line_coverage', 'qwen3-coder:30b-q8_0_constraints_mcts_avg_branch_coverage',
                   'line_coverage_improvement', 'branch_coverage_improvement']

    # Write to output CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(output_header)

        # Calculate averages for each project
        for project, data in sorted(project_data.items()):
            # Calculate averages
            avg_model1_line = sum(data['model1_lines']) / len(data['model1_lines']) if data['model1_lines'] else 0
            avg_model1_branch = sum(data['model1_branches']) / len(data['model1_branches']) if data['model1_branches'] else 0
            avg_model2_line = sum(data['model2_lines']) / len(data['model2_lines']) if data['model2_lines'] else 0
            avg_model2_branch = sum(data['model2_branches']) / len(data['model2_branches']) if data['model2_branches'] else 0

            # Calculate improvement percentages
            line_improvement = ((avg_model2_line - avg_model1_line) / avg_model1_line) * 100 if avg_model1_line != 0 else 0
            branch_improvement = ((avg_model2_branch - avg_model1_branch) / avg_model1_branch) * 100 if avg_model1_branch != 0 else 0

            # Write to CSV
            row = [
                project,
                data['class_count'],
                round(avg_model1_line, 2),
                round(avg_model1_branch, 2),
                round(avg_model2_line, 2),
                round(avg_model2_branch, 2),
                round(line_improvement, 2),
                round(branch_improvement, 2)
            ]
            writer.writerow(row)

    return output_csv

def main():
    # Input CSV (result from previous analysis)
    input_csv = 'qwen3_coverage_comparison.csv'

    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found! Please run the evaluate_qwen3.py script first.")
        return

    # Calculate project averages
    output_csv = calculate_project_averages(input_csv)

    print(f"Per-project average coverages calculated successfully.")
    print(f"Results saved to {output_csv}")

    # Display the results
    print("\n" + "-" * 80)
    print(f"{'Project':<25} {'Classes':<10} {'Model1 Line':<15} {'Model1 Branch':<15} {'Model2 Line':<15} {'Model2 Branch':<15} {'Line Impr.':<12} {'Branch Impr.':<15}")
    print("-" * 110)

    with open(output_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            project = row[0]
            classes = row[1]
            m1_line = row[2]
            m1_branch = row[3]
            m2_line = row[4]
            m2_branch = row[5]
            line_impr = f"{row[6]}%"
            branch_impr = f"{row[7]}%"

            print(f"{project:<25} {classes:<10} {m1_line:<15} {m1_branch:<15} {m2_line:<15} {m2_branch:<15} {line_impr:<12} {branch_impr:<15}")

    print("-" * 110)

if __name__ == '__main__':
    main()