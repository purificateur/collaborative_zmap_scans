import re
from pathlib import Path


def ip_key(ip):
    """Convert IP address to a key that can be sorted numerically."""
    return tuple(map(int, ip.split(".")))


def reorder_ipv4s(input_file_path, output_file_path):
    # Read the file content
    input_file = Path(input_file_path)
    content = input_file.read_text()

    # Regular expression to match the sets with IPs and covers
    set_pattern = re.compile(
        r"(### Set \d+ - Source Count: \d+ - Total Cover: \d+ - Window: \d+\n\n\| Source IPv4 \| Covers \|\n\| --- \| --- \|\n)([\s\S]*?)(?=\n\n### Set|\n\n## Window Size|\Z)",
        re.MULTILINE,
    )

    def reorder_set(match):
        header = match.group(1)
        body = match.group(2).strip()

        # Split the body into lines, sort by IP address, and join them back
        lines = body.split("\n")
        lines.sort(key=lambda line: ip_key(line.split("|")[1].strip()))
        sorted_body = "\n".join(lines)

        return header + sorted_body

    # Reorder the IPs in all matched sets
    new_content = set_pattern.sub(reorder_set, content)

    # Ensure the output directory exists
    output_file = Path(output_file_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the new content to the output file
    output_file.write_text(new_content)


if __name__ == "__main__":
    port = 8728

    # input_file_path = f"../results/{port}/2024-02-03 {port}.md"
    # output_file_path = f"./src_sort_results/{port}/2024-02-03 {port}.md"
    # reorder_ipv4s(input_file_path, output_file_path)

    for day in range(1, 10):
        input_file_path = f"../results/{port}/2024-02-0{day} {port}.md"
        output_file_path = f"./src_sort_results/{port}/2024-02-0{day} {port}.md"
        reorder_ipv4s(input_file_path, output_file_path)

    for day in range(10, 30):
        input_file_path = f"../results/{port}/2024-02-{day} {port}.md"
        output_file_path = f"./src_sort_results/{port}/2024-02-{day} {port}.md"
        reorder_ipv4s(input_file_path, output_file_path)
