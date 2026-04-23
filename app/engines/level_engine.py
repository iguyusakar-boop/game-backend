def get_level_info(xp: int) -> dict:
    level = (xp // 100) + 1
    level_min_xp = (level - 1) * 100
    level_max_xp = level * 100
    xp_to_next_level = level_max_xp - xp

    total_range = level_max_xp - level_min_xp
    if total_range == 0:
        progress_percent = 0
    else:
        progress_percent = int(((xp - level_min_xp) / total_range) * 100)

    return {
        "level": level,
        "current_xp": xp,
        "level_min_xp": level_min_xp,
        "level_max_xp": level_max_xp,
        "xp_to_next_level": xp_to_next_level,
        "progress_percent": progress_percent
    }