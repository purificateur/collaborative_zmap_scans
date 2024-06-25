import random


def set_cover(src_to_dsts, verify=False):
    # Get the universal set as all dsts scanned
    all_dstips = set.union(*src_to_dsts.values())

    ############################### VERIFICATION CODE ################################
    if verify:
        # Generate random sources
        generated_sources = generate_sources(random.randint(2, 256))

        # Distribute destination addresses among the generated sources
        generated_src_to_dsts = distribute_dsts_to_sources(
            generated_sources, all_dstips
        )

        print(f"[DEBUG] Verify injected {len(generated_sources)} sources")

        # Integrate generated sources into the original src_to_dsts map
        for src, dsts in generated_src_to_dsts.items():
            if src in src_to_dsts:
                src_to_dsts[src].update(dsts)
            else:
                src_to_dsts[src] = dsts
    ############################## END VERIFICATION CODE ##############################

    # Sort srcs based on the number of dst they scan (in descending order)
    sorted_srcs = sorted(
        src_to_dsts.keys(), key=lambda src_ip: -len(src_to_dsts[src_ip])
    )

    # Initialize an empty set to store the selected srcs
    selected_srcs = set()

    # Initialize a set to keep track of covered dsts
    covered_dsts = set()

    while len(sorted_srcs) > 0:
        # Iterate through the sorted srcs
        for srcip in sorted_srcs:
            # Check if srcip has any dstips that are already covered
            if any(dstip in covered_dsts for dstip in src_to_dsts[srcip]):
                continue

            # Determine the dsts that are not covered by previously selected srcs
            uncovered_dstips = src_to_dsts[srcip] - covered_dsts

            # If src has uncovered dsts, add it to the selected set and update the list of covered dsts
            if uncovered_dstips:
                selected_srcs.add((srcip, len(src_to_dsts[srcip])))
                covered_dsts.update(uncovered_dstips)

                # If all dsts are covered with more than 1 src, return the selected srcs
                if covered_dsts == all_dstips and len(selected_srcs) > 1:
                    return (selected_srcs, len(all_dstips))

        # First element is not included in a cover, remove it and reset results
        sorted_srcs.pop(0)
        selected_srcs = set()
        covered_dsts = set()

    # If no srcs can cover all dsts without overlap, return None
    return None


def generate_sources(n):
    return {f"0.0.0.{i}" for i in range(n)}


def distribute_dsts_to_sources(sources, all_dsts):
    src_to_dsts = {src: set() for src in sources}
    dst_list = list(all_dsts)
    random.shuffle(dst_list)

    # Ensure each source gets at least one destination
    for src in sources:
        dst = dst_list.pop()
        src_to_dsts[src].add(dst)

    # Distribute remaining destinations randomly
    for dst in dst_list:
        src = random.choice(list(sources))
        src_to_dsts[src].add(dst)

    return src_to_dsts
