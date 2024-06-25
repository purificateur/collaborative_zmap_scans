def count_packets(client):
    query = """
        SELECT Count(*)
        FROM tcppackets
    """
    return execute(client, query)


def count_zmap_packets(client):
    query = """
        SELECT Count(*)
        FROM tcppackets
        WHERE IPId == '54321'
    """
    return execute(client, query)


def count_scans_per_dst(client):
    query = """
        SELECT IPv4NumToString(DstIP) AS DstIP, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY DstIP
        ORDER BY EntryCount
    """
    return execute(client, query)


def count_scans_per_port(client):
    query = """
        SELECT DstPort, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY DstPort
        ORDER BY EntryCount DESC
    """
    return execute(client, query)


def count_scans_per_port_limit(client, limit):
    query = f"""
        SELECT DstPort, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY DstPort
        ORDER BY EntryCount DESC
        LIMIT {limit}
    """
    return execute(client, query)


def count_scans_per_denoise_dst(client):
    query = """
        SELECT IPv4NumToString(DstIP) AS DstIP, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY DstIP
        HAVING EntryCount > 1000
        ORDER BY EntryCount
    """
    return execute(client, query)


def count_scans_per_denoise_dst_f_day_port(client, day_str, port):
    query = f"""
        WITH denoised_dstips AS (
            SELECT IPv4NumToString(DstIP) AS DstIP
            FROM tcppackets
            WHERE IPId = '54321'
            GROUP BY DstIP
            HAVING COUNT(*) > 1000
        )
        SELECT IPv4NumToString(DstIP) AS DstIP, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE 
            IPId = '54321' 
            AND DstPort = '{port}' 
            AND toDate(Timestamp) = '{day_str}'
            AND DstIP IN (SELECT DstIP FROM denoised_dstips)
        GROUP BY DstIP
        ORDER BY EntryCount
    """
    return execute(client, query)


def count_denoise_distinct_src_f_port(client, port):
    query = f"""
        WITH denoised_dstips AS (
            SELECT IPv4NumToString(DstIP) AS DstIP
            FROM tcppackets
            WHERE IPId = '54321'
            GROUP BY DstIP
            HAVING COUNT(*) > 1000
        )
        SELECT COUNT(DISTINCT SrcIP) AS DistinctSrcIPCount
        FROM tcppackets
        WHERE 
            IPId = '54321' 
            AND DstPort = '{port}'
            AND IPv4NumToString(DstIP) IN (SELECT DstIP FROM denoised_dstips)
    """
    return execute(client, query)


def count_order_srcip_dstips_f_day_port(client, day_str, port):
    query = f"""
        SELECT IPv4NumToString(SrcIP) AS SrcIPv4, COUNT(*) AS Count
        FROM tcppackets
        WHERE IPId == '54321' AND DstPort == '{port}' AND toDate(Timestamp) == '{day_str}'
        GROUP BY SrcIP
        ORDER BY SrcIP
    """
    return execute(client, query)


def count_denoise_order_srcip_dstips_f_day_port(client, day_str, port):
    query = f"""
        WITH denoised_dstips AS (
            SELECT IPv4NumToString(DstIP) AS DstIP
            FROM tcppackets
            WHERE IPId = '54321'
            GROUP BY DstIP
            HAVING COUNT(*) > 1000
        )
        SELECT IPv4NumToString(SrcIP) AS SrcIPv4, COUNT(*) AS Count
        FROM tcppackets
        WHERE 
            IPId = '54321' 
            AND DstPort = '{port}' 
            AND toDate(Timestamp) = '{day_str}'
            AND IPv4NumToString(DstIP) IN (SELECT DstIP FROM denoised_dstips)
        GROUP BY SrcIP
        ORDER BY SrcIP
    """
    return execute(client, query)


def order_most_zmap_packets_limit(client, limit):
    query = f"""
        SELECT IPv4NumToString(SrcIP) as SrcIP, Count(*) as EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY SrcIP
        ORDER BY EntryCount DESC
        LIMIT {limit}
    """
    return execute(client, query)


def order_days(client):
    query = """
        SELECT toDate(Timestamp) AS Date, COUNT(*) AS EntryCount
        FROM tcppackets
        WHERE IPId == '54321'
        GROUP BY Date
        ORDER BY Date
    """
    return execute(client, query)


def order_dst_ip_limit(client, limit):
    query = f"""
        SELECT DISTINCT IPv4NumToString(DstIP) AS DstIP, DstPort
        FROM tcppackets 
        WHERE IPId == '54321'
        ORDER BY DstPort, DstIP
        LIMIT {limit}
    """
    return execute(client, query)


def order_dst_port_ip_f_day(client, day_str):
    query = f"""
        SELECT DISTINCT IPv4NumToString(DstIP) AS DstIP, DstPort
        FROM tcppackets
        WHERE IPId == '54321' AND toDate(Timestamp) == '{day_str}'
        ORDER BY DstPort, DstIP
    """
    return execute(client, query)


def order_dst_port_ip_f_day_ip(client, day_str, ip_str):
    query = f"""
        SELECT DISTINCT IPv4NumToString(DstIP) AS Dst, DstPort
        FROM tcppackets
        WHERE 
            IPId == '54321' 
            AND DstIP == IPv4StringToNum('{ip_str}') 
            AND toDate(Timestamp) == '{day_str}'
        ORDER BY DstPort, DstIP
    """
    return execute(client, query)


def map_order_srcip_dstips_f_day_port(client, day_str, port):
    query = f"""
        SELECT IPv4NumToString(SrcIP) AS SrcIPv4, groupArray(IPv4NumToString(DstIP)) AS DstIPv4s
        FROM tcppackets
        WHERE IPId == '54321' AND DstPort == '{port}' AND toDate(Timestamp) == '{day_str}'
        GROUP BY SrcIP
        ORDER BY SrcIP
    """
    return execute(client, query)


def map_denoise_order_srcip_dstips_f_day_port(client, day_str, port):
    query = f"""
        WITH denoised_dstips AS (
            SELECT IPv4NumToString(DstIP) AS DstIP
            FROM tcppackets
            WHERE IPId = '54321'
            GROUP BY DstIP
            HAVING COUNT(*) > 1000
        )
        SELECT IPv4NumToString(SrcIP) AS SrcIPv4, groupArray(IPv4NumToString(DstIP)) AS DstIPv4s
        FROM tcppackets
        WHERE 
            IPId = '54321' 
            AND DstPort = '{port}' 
            AND toDate(Timestamp) = '{day_str}'
            AND IPv4NumToString(DstIP) IN (SELECT DstIP FROM denoised_dstips)
        GROUP BY SrcIP
        ORDER BY SrcIP
    """
    return execute(client, query)


def map_denoise_order_srcip_dstips_f_day_port_hour_window(
    client, day_str, port, start_hour, window_size
):
    query = f"""
        WITH denoised_dstips AS (
            SELECT IPv4NumToString(DstIP) AS DstIP
            FROM tcppackets
            WHERE IPId = '54321'
            GROUP BY DstIP
            HAVING COUNT(*) > 1000
        )
        SELECT IPv4NumToString(SrcIP) AS SrcIPv4, groupArray(IPv4NumToString(DstIP)) AS DstIPv4s
        FROM tcppackets
        WHERE 
            IPId = '54321' 
            AND DstPort = '{port}' 
            AND toDate(Timestamp) = '{day_str}'
            AND toHour(Timestamp) >= {start_hour} AND toHour(Timestamp) < {start_hour + window_size}
            AND IPv4NumToString(DstIP) IN (SELECT DstIP FROM denoised_dstips)
        GROUP BY SrcIP
        ORDER BY SrcIP
    """
    return execute(client, query)


def zmap_packets_limit(client, limit):
    query = f"""
        SELECT IPv4NumToString(SrcIP) AS SrcIP, IPv4NumToString(DstIP) as DstIP, DstPort
        FROM tcppackets
        WHERE IPId == '54321'
        LIMIT {limit}
    """
    return execute(client, query)


def zmap_packets_f_day(client, day_str):
    query = f"""
        SELECT Timestamp, IPv4NumToString(SrcIP) AS SrcIP, IPv4NumToString(DstIP) AS DstIP, DstPort
        FROM tcppackets
        WHERE IPId == '54321' AND toDate(Timestamp) == '{day_str}'
    """
    return execute(client, query)


def zmap_packets_f_port_src_limit(client, port, src, limit):
    query = f"""
        SELECT DISTINCT IPv4NumToString(DstIP) AS DstIP
        FROM tcppackets
        WHERE 
            IPId == '54321' 
            AND IPv4NumToString(SrcIP) == '{src}'
            AND DstPort == '{port}'
        LIMIT {limit}
    """
    return execute(client, query)


def execute(client, query):
    try:
        res = client.query_dataframe(query)

        return res

    except Exception as e:
        print(f"\033[1m\033[31mError: {e}\033[0m")
        return None
