def asset_modifier(criticality_level):
    return 1 + (criticality_level - 3) * 0.15


def network_modifier(outbound, unique_ips, unusual_port):
    score = 1.0

    if outbound > 500:
        score += 0.2

    if unique_ips > 10:
        score += 0.2

    if unusual_port == 1:
        score += 0.2

    return score


def security_modifier(privilege, config, av, failed_auth):
    score = 1.0

    if privilege == 1:
        score += 0.25

    if config == 1:
        score += 0.1

    if av == 1:
        score += 0.3

    if failed_auth > 5:
        score += 0.2

    return score