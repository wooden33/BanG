"""
Parse coverage results and generate statistics.
Supports configurable paths via command line arguments.
"""
import argparse
import csv
import os
import re


def parse_coverage_from_html(html_content):
    """Parse HTML to extract coverage data for all iterations using regex."""
    # Clean up HTML content
    html_content = html_content.strip()

    # Find all rows - match from <tr> to </tr> using regex
    # This handles malformed HTML with unclosed pre/code tags
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL)
    rows = row_pattern.findall(html_content)

    coverage_data = {}

    for row in rows:
        # Find all cells in this row
        cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)
        cells = cell_pattern.findall(row)

        if len(cells) < 6:
            continue

        # Extract status from first cell (may contain class attribute)
        status_cell = cells[0]
        status_match = re.search(r'status-(\w+)', status_cell)
        status = status_match.group(1) if status_match else cells[0].strip()
        if status == 'INFO':
            status = 'INFO'
        elif status == 'PASS':
            status = 'PASS'
        elif status == 'FAIL':
            status = 'FAIL'
        else:
            # Try to get text content
            status = re.sub(r'<[^>]+>', '', status_cell).strip()

        # Extract label from second cell
        label = re.sub(r'<[^>]+>', '', cells[1]).strip()

        # Extract coverage values (columns 4 and 5 are line and branch coverage)
        try:
            line_coverage = float(re.sub(r'<[^>]+>', '', cells[4]).strip())
            branch_coverage = float(re.sub(r'<[^>]+>', '', cells[5]).strip())
        except (ValueError, IndexError):
            continue

        # For g_X iterations, only keep entries with status=INFO (aggregated results)
        if label.startswith('g_') and status != 'INFO':
            continue

        # Handle empty label rows with INFO status (final results)
        if not label and status == 'INFO':
            coverage_data['final'] = {
                "line_coverage": line_coverage,
                "branch_coverage": branch_coverage
            }
            continue

        # Skip empty label rows that are not INFO
        if not label:
            continue

        coverage_data[label] = {
            "line_coverage": line_coverage,
            "branch_coverage": branch_coverage
        }

    return coverage_data


def load_complexity_data(csv_path):
    """Load cyclomatic complexity data from class_list.csv."""
    complexity = {}
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row['project']}-{row['class']}"
            complexity[key] = int(row['complexity'])
    return complexity


def get_project_from_filename(filename, prompt_type="control"):
    """Extract class name from filename."""
    # Try format: ClassName_control_ClassName_control_test_results.html
    match = re.match(rf'^(.+?)_{prompt_type}_{prompt_type}_test_results\.html$', filename)
    if match:
        return match.group(1)
    # Try format: ClassName_control_test_results.html
    match = re.match(rf'^(.+?)_{prompt_type}_test_results\.html$', filename)
    if match:
        return match.group(1)
    return None


def main():
    parser = argparse.ArgumentParser(description='Parse coverage results and generate statistics.')
    parser.add_argument('--result-dir', type=str, required=True,
                        help='Directory containing HTML result files')
    parser.add_argument('--class-list', type=str, required=True,
                        help='Path to class_list.csv with complexity data')
    parser.add_argument('--output', type=str, default='coverage_statistics.csv',
                        help='Output CSV file path (default: coverage_statistics.csv)')
    parser.add_argument('--prompt-type', type=str, default='control',
                        help='Prompt type used in filenames (default: control)')

    args = parser.parse_args()

    # Load complexity data
    complexity_data = load_complexity_data(args.class_list)

    # Find all HTML files
    html_files = [f for f in os.listdir(args.result_dir) if f.endswith('.html')]

    results = []

    for html_file in sorted(html_files):
        class_name = get_project_from_filename(html_file, args.prompt_type)
        if not class_name:
            continue

        # Determine project from complexity data
        project = None
        complexity = None
        for key, cc in complexity_data.items():
            if key.endswith(f"-{class_name}"):
                project = key.split('-')[0]
                complexity = cc
                break

        if complexity is None:
            print(f"Warning: No complexity found for {class_name}")
            continue

        # Parse HTML
        html_path = os.path.join(args.result_dir, html_file)
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            coverage_data = parse_coverage_from_html(html_content)
        except Exception as e:
            print(f"Error parsing {html_file}: {e}")
            continue

        # Extract coverage for g_0, g_1, g_2 and final iteration
        iter_0 = coverage_data.get('g_0', {})
        iter_1 = coverage_data.get('g_1', {})
        iter_2 = coverage_data.get('g_2', {})

        # Find final iteration (last g_X entry)
        # First check if there's a 'final' entry (empty label INFO row)
        final = coverage_data.get('final', {})
        final_label = 'final' if final else None
        max_iter = -1
        
        # If no 'final' entry, find the last g_X entry
        if not final:
            for label in coverage_data.keys():
                match = re.match(r'^g_(\d+)$', label)
                if match:
                    iter_num = int(match.group(1))
                    if iter_num > max_iter:
                        max_iter = iter_num
                        final_label = label
            final = coverage_data.get(final_label, {})
        else:
            # If we have a 'final' entry, find max_iter from g_X entries
            for label in coverage_data.keys():
                match = re.match(r'^g_(\d+)$', label)
                if match:
                    iter_num = int(match.group(1))
                    if iter_num > max_iter:
                        max_iter = iter_num

        results.append({
            'project': project,
            'class': class_name,
            'complexity': complexity,
            'iter_0_line': iter_0.get('line_coverage'),
            'iter_0_branch': iter_0.get('branch_coverage'),
            'iter_1_line': iter_1.get('line_coverage'),
            'iter_1_branch': iter_1.get('branch_coverage'),
            'iter_2_line': iter_2.get('line_coverage'),
            'iter_2_branch': iter_2.get('branch_coverage'),
            'final_line': final.get('line_coverage'),
            'final_branch': final.get('branch_coverage'),
            'final_iter': max_iter
        })

    # Write results to CSV
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'project', 'class', 'complexity',
            'iter_0_line', 'iter_0_branch',
            'iter_1_line', 'iter_1_branch',
            'iter_2_line', 'iter_2_branch',
            'final_line', 'final_branch', 'final_iter'
        ])
        writer.writeheader()
        writer.writerows(results)

    # Calculate and print summary statistics
    valid_results = [r for r in results if r['final_line'] is not None]

    print(f"\n=== Statistics ===")
    print(f"Result directory: {args.result_dir}")
    print(f"Total classes analyzed: {len(results)}")
    print(f"Classes with valid final coverage: {len(valid_results)}")

    if valid_results:
        avg_complexity = sum(r['complexity'] for r in valid_results) / len(valid_results)
        print(f"\nAverage Cyclomatic Complexity: {avg_complexity:.2f}")

        iter_0_lines = [r['iter_0_line'] for r in valid_results if r['iter_0_line'] is not None]
        iter_1_lines = [r['iter_1_line'] for r in valid_results if r['iter_1_line'] is not None]
        iter_2_lines = [r['iter_2_line'] for r in valid_results if r['iter_2_line'] is not None]
        final_lines = [r['final_line'] for r in valid_results if r['final_line'] is not None]

        iter_0_branches = [r['iter_0_branch'] for r in valid_results if r['iter_0_branch'] is not None]
        iter_1_branches = [r['iter_1_branch'] for r in valid_results if r['iter_1_branch'] is not None]
        iter_2_branches = [r['iter_2_branch'] for r in valid_results if r['iter_2_branch'] is not None]
        final_branches = [r['final_branch'] for r in valid_results if r['final_branch'] is not None]

        print(f"\nLine Coverage:")
        print(f"  g_0:  {sum(iter_0_lines)/len(iter_0_lines):.2f}% ({len(iter_0_lines)} samples)")
        print(f"  g_1:  {sum(iter_1_lines)/len(iter_1_lines):.2f}% ({len(iter_1_lines)} samples)")
        print(f"  g_2:  {sum(iter_2_lines)/len(iter_2_lines):.2f}% ({len(iter_2_lines)} samples)")
        print(f"  Final: {sum(final_lines)/len(final_lines):.2f}%")

        print(f"\nBranch Coverage:")
        print(f"  g_0:  {sum(iter_0_branches)/len(iter_0_branches):.2f}% ({len(iter_0_branches)} samples)")
        print(f"  g_1:  {sum(iter_1_branches)/len(iter_1_branches):.2f}% ({len(iter_1_branches)} samples)")
        print(f"  g_2:  {sum(iter_2_branches)/len(iter_2_branches):.2f}% ({len(iter_2_branches)} samples)")
        print(f"  Final: {sum(final_branches)/len(final_branches):.2f}%")

    print(f"\nResults saved to: {args.output}")


if __name__ == '__main__':
    main()
