import re
from pathlib import Path
from datetime import datetime, timedelta


def count_group_sizes_in_file(file_path):
    """Count the number of groups by size in a given markdown file."""
    file = Path(file_path)
    if not file.exists():
        return {}
    content = file.read_text()
    # Regular expression to match the group size
    set_pattern = re.compile(r"### Set \d+ - Source Count: (\d+)")
    matches = set_pattern.findall(content)
    size_counts = {}
    for match in matches:
        size = int(match)
        if size in size_counts:
            size_counts[size] += 1
        else:
            size_counts[size] = 1
    return size_counts


def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)
    dates = []
    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += delta
    return dates


def main():
    start_date = "2024-02-01"
    end_date = "2024-02-29"
    port = 8728
    date_range = generate_date_range(start_date, end_date)

    total_counts = {}
    total_count = 0
    for date in date_range:
        file_path = f"../results/{port}/{date} {port}.md"
        size_counts = count_group_sizes_in_file(file_path)
        for size, count in size_counts.items():
            if size in total_counts:
                total_counts[size] += count
                total_count += count
            else:
                total_counts[size] = count
                total_count += count

    # Prepare data for the markdown table
    sizes = list(total_counts.keys())
    counts = list(total_counts.values())
    table_data = list(zip(sizes, counts))
    table_data.sort(key=lambda x: x[0])

    # Writing the markdown table to a file
    output_dir = Path("./size_counter_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"group_sizes_total_{port}.md"

    with open(output_file, "w") as f:
        f.write(f"# Total Number of Groups by Size in February 2024 (Port {port})\n\n")
        f.write("| Group Size | Total Number of Groups |\n")
        f.write("|------------|-------------------------|\n")
        for size, count in table_data:
            f.write(f"| {size} | {count} |\n")
        f.write(f"| Total | {total_count} |\n")

    print(f"Markdown table written to {output_file}")


if __name__ == "__main__":
    main()
