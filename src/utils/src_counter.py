import re
from pathlib import Path
from datetime import datetime, timedelta


def count_sources_in_file(file_path):
    """Count the number of sources clustered into groups in a given markdown file."""
    file = Path(file_path)
    if not file.exists():
        return {}
    content = file.read_text()
    # Regular expression to match the number of sources in each group
    set_pattern = re.compile(r"### Set \d+ - Source Count: (\d+)")
    matches = set_pattern.findall(content)
    total_sources = sum(int(match) for match in matches)
    distinct_sources = len(
        set(re.findall(r"\| ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+) \|", content))
    )
    return total_sources, distinct_sources


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

    total_sources = 0
    distinct_sources = set()
    for date in date_range:
        file_path = f"../results/{port}/{date} {port}.md"
        sources_in_group, distinct_sources_in_group = count_sources_in_file(file_path)
        total_sources += sources_in_group
        distinct_sources.update(range(distinct_sources_in_group))

    # Writing the markdown table to a file
    output_dir = Path("./src_counter_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"source_counts_{port}.md"

    with open(output_file, "w") as f:
        f.write(f"# Source Counts Port {port}\n\n")
        f.write("| Distinct Sources | Number of Sources |\n")
        f.write("|------------------|-------------------|\n")
        f.write(f"| {len(distinct_sources)} | {total_sources} |\n")

    print(f"Markdown table written to {output_file}")


if __name__ == "__main__":
    main()
