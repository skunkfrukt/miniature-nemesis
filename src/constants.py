def bitrange(n):
    for exponent in range(n):
        yield 2 ** exponent


GAME_TITLE = "Miniature Nemesis"
GAME_VERSION = "0.0"

WIN_WIDTH = 640
WIN_HEIGHT = 360
WIN_TITLE = "%s v%s" % (GAME_TITLE, GAME_VERSION)
SCREEN_MARGIN = 100

(R_GROUP_BG,
R_GROUP_PROPS,
R_GROUP_ACTORS_BACK,
R_GROUP_HERO,
R_GROUP_ACTORS_FRONT,
R_GROUP_PROJECTILES,
R_GROUP_FG) = range(7)

(EASY,
NORMAL,
HARD) = bitrange(3)

SPEED_BASE = 100

SPEED_FACTORS = {
        EASY: 0.8,
        NORMAL: 1.0,
        HARD: 1.4,
}

SPEEDS = {
        EASY: int(SPEED_BASE * SPEED_FACTORS[EASY]),
        NORMAL: int(SPEED_BASE * SPEED_FACTORS[NORMAL]),
        HARD: int(SPEED_BASE * SPEED_FACTORS[HARD])
}
