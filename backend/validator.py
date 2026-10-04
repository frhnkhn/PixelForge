# =========================================================
# PIXELFORGE VALIDATOR
# =========================================================


MAX_PROMPT_LENGTH = 10000

MAX_NEGATIVE_PROMPT_LENGTH = 5000


# =========================================================
# ALLOWED SETTINGS
# =========================================================

ALLOWED_ASPECT_RATIOS = {

    "16:9",
    "1:1",
    "21:9",
    "2:3",
    "3:2",
    "4:5",
    "5:4",
    "9:16",
    "9:21"

}


ALLOWED_FORMATS = {

    "png",
    "jpeg",
    "webp"

}


ALLOWED_STYLES = {

    "3d-model",
    "analog-film",
    "anime",
    "cinematic",
    "comic-book",
    "digital-art",
    "enhance",
    "fantasy-art",
    "isometric",
    "line-art",
    "low-poly",
    "modeling-compound",
    "neon-punk",
    "origami",
    "photographic",
    "pixel-art",
    "tile-texture"

}


# =========================================================
# PROMPT VALIDATION
# =========================================================

def validate_prompt(prompt):

    if not prompt:

        return (
            False,
            "Prompt cannot be empty."
        )


    if len(prompt) > MAX_PROMPT_LENGTH:

        return (
            False,
            "Prompt is too long."
        )


    return (
        True,
        None
    )


# =========================================================
# NEGATIVE PROMPT VALIDATION
# =========================================================

def validate_negative_prompt(
    negative_prompt
):

    if not negative_prompt:

        return (
            True,
            None
        )


    if len(negative_prompt) > MAX_NEGATIVE_PROMPT_LENGTH:

        return (
            False,
            "Negative prompt is too long."
        )


    return (
        True,
        None
    )


# =========================================================
# SETTINGS VALIDATION
# =========================================================

def validate_settings(
    aspect_ratio,
    style_preset,
    output_format
):

    if aspect_ratio not in ALLOWED_ASPECT_RATIOS:

        return (
            False,
            "Invalid aspect ratio."
        )


    if style_preset not in ALLOWED_STYLES:

        return (
            False,
            "Invalid style preset."
        )


    if output_format not in ALLOWED_FORMATS:

        return (
            False,
            "Invalid output format."
        )


    return (
        True,
        None
    )


# =========================================================
# SEED VALIDATION
# =========================================================

def validate_seed(seed):

    try:

        seed = int(seed)


    except (
        ValueError,
        TypeError
    ):

        return (
            False,
            "Seed must be a number."
        )


    if seed < 0:

        return (
            False,
            "Seed cannot be negative."
        )


    if seed > 4294967295:

        return (
            False,
            "Seed is too large."
        )


    return (
        True,
        None
    )