import time
import queries
import set_cover
from clickhouse_driver import Client


def main():
    client = Client(
        host="<redacted>",
        port=9000,
        database="<redacted>",
        user="<redacted>",
        password="<redacted>",
        client_name="<redacted>",
    )

    time_func(False, detect_collaborative_scans, client, "2024-02-29", 8728, False)


def detect_collaborative_scans(client, date_str, port, verify=False):
    if verify:
        filename = f"results/verification/{date_str} {port}.md"
    else:
        filename = f"results/{port}/{date_str} {port}.md"

    with open(filename, "w") as file:
        file.write("# Results - {} - {} \n\n".format(date_str, port))

    covers = set()
    n = 1

    for window_size in range(1, 25):
        with open(filename, "a") as file:
            file.write("## Window Size: {} hour(s)\n\n".format(window_size))

        # Shifting window
        for start_hour in range(0, 25 - window_size):
            # Query data
            result = time_func(
                False,
                queries.map_denoise_order_srcip_dstips_f_day_port_hour_window,
                client,
                date_str,
                port,
                start_hour,
                window_size,
            )

            if result is None:
                print("\033[1m\033[31mError while querying results!\n\033[0m")
                return

            # Convert the result into a dictionary mapping SrcIP to a set of DstIPs
            src_to_dst = {}

            for idx, row in result.iterrows():
                src_ip = row["SrcIPv4"]
                dst_ips = set(row["DstIPv4s"])

                src_to_dst[src_ip] = dst_ips

            verify_flag = verify and start_hour == 0

            while len(src_to_dst.keys()) > 0:
                print(f"[DEBUG] Set Cover -> ws:{window_size} w:{start_hour + 1}")

                cover = set_cover.set_cover(src_to_dst, verify_flag)

                verify_flag = False

                if cover is None:
                    break

                # Convert cover to hashable
                cover = (frozenset(cover[0]), cover[1])

                # This cover is already found in another window
                if cover in covers:
                    # Remove one of the srcs from the found cover and re-run set cover
                    print(list(cover[0])[0])
                    src_to_dst.pop(set(cover[0]).pop()[0])
                    continue

                covers.add(cover)

                with open(filename, "a") as file:
                    file.write(
                        "### Set {} - Source Count: {} - Total Cover: {} - Window: {}\n\n".format(
                            n, len(cover[0]), cover[1], start_hour + 1
                        )
                    )
                    file.write("| Source IPv4 | Covers |\n")
                    file.write("| --- | --- |\n")

                    for srcip, num_dst in cover[0]:
                        file.write("| {} | {} |\n".format(srcip, num_dst))

                    file.write("\n")

                # Remove one of the srcs from the found cover and re-run set cover
                src_to_dst.pop(set(cover[0]).pop()[0])
                n += 1

        if n == 1:
            with open(filename, "a") as file:
                file.write("No covers found!\n\n")


def time_func(write, func, *args):
    t0 = time.time()
    res = func(*args)
    t1 = time.time()
    t = t1 - t0

    if t < 60:
        print(f"\033[1m\033[32m{func.__name__} took {t1-t0:.6f} seconds\n\033[0m")
    elif t < 300:
        print(f"\033[1m\033[33m{func.__name__} took {t1-t0:.6f} seconds\n\033[0m")
    elif t < 600:
        print(f"\033[1m\033[31m{func.__name__} took {t1-t0:.6f} seconds\n\033[0m")
    else:
        print(f"\033[1m\033[35m{func.__name__} took {t1-t0:.6f} seconds\n\033[0m")

    if write and res is not None:
        write_to_md(res, f"{func.__name__}.md")

    return res


def write_to_md(results, filename="query_result.md"):
    with open(f"query_results/{filename}", "w") as file:
        file.write("# Query Results\n\n")
        file.write("| " + " | ".join(results.columns) + " |\n")
        file.write("|" + " | ".join(["---"] * len(results.columns)) + "|\n")

        for index, row in results.iterrows():
            file.write("| " + " | ".join(map(str, row)) + " |\n")


def mock_detect_collaborative_scans():
    src_to_dst = {
        "E": {"1", "2", "3", "4", "6"},
        "A": {"1", "2", "3"},
        "B": {"3", "4", "5"},
        "C": {"4", "5"},
        "D": {"6"},
    }

    cover = set_cover.set_cover(src_to_dst)

    # Print the results
    print("\033[1m\033[34mAll possible covers:")
    print(cover)
    print("\033[0m")


if __name__ == "__main__":
    main()
