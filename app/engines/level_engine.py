def calculate_level(total_xp: int) -> int:
    if total_xp < 100:
        return 1
    elif total_xp < 250:
        return 2
    elif total_xp < 450:
        return 3
    elif total_xp < 700:
        return 4
    elif total_xp < 1000:
        return 5
    else:
        extra = total_xp - 1000
        return 6 + (extra // 400)


def get_level_progress(total_xp: int):
    if total_xp < 100:
        return (1, total_xp, 0, 100)
    elif total_xp < 250:
        return (2, total_xp, 100, 250)
    elif total_xp < 450:
        return (3, total_xp, 250, 450)
    elif total_xp < 700:
        return (4, total_xp, 450, 700)
    elif total_xp < 1000:
        return (5, total_xp, 700, 1000)
    else:
        extra = total_xp - 1000
        level = 6 + (extra // 400)
        level_min = 1000 + (extra // 400) * 400
        level_max = level_min + 400
        return (level, total_xp, level_min, level_max)