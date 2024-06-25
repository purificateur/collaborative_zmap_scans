import os
import re
from collections import defaultdict


def extract_data_from_file(file_path):
    # Regular expressions to match relevant lines
    source_count_pattern = re.compile(
        r"^### Set (\d+) - Source Count: (\d+) - Total Cover: (\d+) - Window: \d+$"
    )
    source_ip_pattern = re.compile(
        r"^\| (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \| (\d+) \|"
    )

    current_source_count = None
    current_total_cover = None
    data = defaultdict(set)  # Use set to automatically handle duplicates

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Check for source count and total cover
            match = source_count_pattern.match(line)
            if match:
                current_source_count = int(match.group(2))
                current_total_cover = int(match.group(3))
                continue

            # Check for source IP and covers
            match = source_ip_pattern.match(line)
            if match:
                source_ip = match.group(1)
                covers = int(match.group(2))
                data[(current_source_count, current_total_cover, covers)].add(
                    source_ip
                )  # Use set to avoid duplicates

    return data


def write_grouped_data_to_file(port, grouped_data):
    output_file_path = f"./src_grouper_results/{port}.md"

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for (source_count, total_cover, covers), ips in grouped_data.items():
            output_file.write(
                f"## Source Count {source_count} - Total Cover {total_cover} - Covers {covers}\n"
            )
            output_file.write("| Source IPv4 |\n")
            output_file.write("| --- |\n")
            sorted_ips = sorted(ips)  # Sort IPs alphabetically
            for ip in sorted_ips:
                output_file.write(f"| {ip} |\n")
            output_file.write("\n")


def main():
    port = 80
    source_counts_to_include = [2, 3]  # Replace with desired source counts
    directory = f"../results/{port}/"
    grouped_data = defaultdict(set)  # Use set to automatically handle duplicates

    # Step 1: Locate all Markdown files and extract data
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            file_data = extract_data_from_file(file_path)
            for key, value in file_data.items():
                if (
                    source_counts_to_include is None
                    or key[0] in source_counts_to_include
                ):
                    grouped_data[key].update(
                        value
                    )  # Update with new IPs, automatically handles duplicates

    # Step 2: Write grouped data to output Markdown file
    write_grouped_data_to_file(port, grouped_data)


if __name__ == "__main__":
    main()
