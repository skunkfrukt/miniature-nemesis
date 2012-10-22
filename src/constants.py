def bitrange(n):
    for exponent in range(n):
        yield 2 ** exponent


GAME_TITLE = (
        "O accursed hunger of gold, to what dost thou not compel human hearts!")
GAME_VERSION = "0.0.1"

WIN_WIDTH = 640
WIN_HEIGHT = 360
WIN_TITLE = GAME_TITLE
SCREEN_MARGIN = 100

RENDERING_GROUPS = (R_GROUP_BG, R_GROUP_PROPS, R_GROUP_ACTORS_BACK,
        R_GROUP_HERO, R_GROUP_ACTORS_FRONT, R_GROUP_PROJECTILES,
        R_GROUP_FG) = range(7)

DIFFICULTIES = (EASY, NORMAL, HARD) = bitrange(3)
ALL_DIFFICULTIES = sum(DIFFICULTIES)

SPEED_BASE = 100

SPEED_FACTORS = {EASY: 0.8, NORMAL: 1.0, HARD: 1.4}

SPEEDS = {key: int(SPEED_BASE * SPEED_FACTORS[key]) for key in SPEED_FACTORS}

HASH_GROUND, HASH_AIR, HASH_TRIGGER = bitrange(3)

LOTS = 1024
