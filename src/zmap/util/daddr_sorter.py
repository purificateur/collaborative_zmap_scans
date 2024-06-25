import re


# Function to extract daddr field from the IP section
def extract_daddr(line):
    match = re.search(r"daddr: (\d+\.\d+\.\d+\.\d+)", line)
    if match:
        return match.group(1)
    else:
        return None


# Function to convert IP address string to a tuple of integers
def ip_to_tuple(ip):
    return tuple(map(int, ip.split(".")))


# Read the input file and extract daddr field
data = []
with open("output3.txt", "r") as file:
    current_entry = {}
    for line in file:
        if line.strip() == "------------------------------------------------------":
            data.append(current_entry)
            current_entry = {}
        else:
            if "ip" in line:
                daddr = extract_daddr(line)
                current_entry["daddr"] = daddr

# Sort data based on daddr field
sorted_data = sorted(data, key=lambda x: ip_to_tuple(x["daddr"]))

# Write sorted data to a text file
with open("sorted_output3.txt", "w") as file:
    for entry in sorted_data:
        file.write(str(entry) + "\n")
