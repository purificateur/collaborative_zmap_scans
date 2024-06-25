import re
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta


def count_sets_in_file(file_path):
    """Count the number of sets in a given markdown file."""
    file = Path(file_path)
    if not file.exists():
        return 0
    content = file.read_text()
    set_pattern = re.compile(r"### Set \d+ - Source Count:")
    return len(set_pattern.findall(content))


def generate_date_range(start_date, end_date):
    """Generate a list of dates from start_date to end_date."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)
    dates = []
    while start < end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += delta
    return dates


def main():
    start_date = "2024-02-01"
    end_date = "2024-02-29"
    port = 8728
    date_range = generate_date_range(start_date, end_date)

    counts = []
    for date in date_range:
        file_path = f"../results/{port}/{date} {port}.md"
        count = count_sets_in_file(file_path)
        counts.append((date, count))

    # Convert to DataFrame for easier plotting
    df = pd.DataFrame(counts, columns=["Date", "Set Count"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Number of Groups Found per Day in February 2024 (Port {port})
    plt.figure(figsize=(12, 6))
    # plt.plot(df.index, df["Set Count"], marker="o")
    plt.bar(df.index, df["Set Count"])
    plt.xlabel("Date", fontsize=17)
    plt.ylabel("Number of Groups", fontsize=17)
    # plt.grid(True)
    plt.xticks(rotation=45)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    # Save the plot
    output_dir = Path("./set_counter_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / f"set_count_{port}.png")
    plt.show()


if __name__ == "__main__":
    main()
