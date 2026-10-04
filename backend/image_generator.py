import os
import time
import requests

from dotenv import load_dotenv


# =========================================
# ENVIRONMENT
# =========================================

load_dotenv()

API_KEY = os.getenv("STABILITY_API_KEY")

API_URL = (
    "https://api.stability.ai/v2beta/"
    "stable-image/generate/core"
)


# =========================================
# CONSTANTS
# =========================================

MAX_RETRIES = 3

CONNECT_TIMEOUT = 5

READ_TIMEOUT = 60


# =========================================
# GENERATE IMAGE
# =========================================

def generate_image(
    prompt,
    aspect_ratio="1:1",
    negative_prompt="",
    style_preset="photographic",
    output_format="png",
    seed=0
):

    """
    Generate an image using Stability AI.

    Returns:
        bytes: Generated image data

    Raises:
        Exception: If generation fails
    """


    # -------------------------------------
    # API KEY CHECK
    # -------------------------------------

    if not API_KEY:

        raise Exception(
            "STABILITY_API_KEY is missing."
        )


    # -------------------------------------
    # HEADERS
    # -------------------------------------

    headers = {

        "authorization":
            f"Bearer {API_KEY}",

        "accept":
            "image/*"

    }


    # -------------------------------------
    # REQUEST DATA
    # -------------------------------------

    data = {

        "prompt":
            prompt,

        "aspect_ratio":
            aspect_ratio,

        "output_format":
            output_format,

        "style_preset":
            style_preset

    }


    if negative_prompt:

        data["negative_prompt"] = (
            negative_prompt
        )


    if seed:

        data["seed"] = seed


    # =====================================
    # RETRY LOOP
    # =====================================

    last_error = None


    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):

        try:

            print(
                f"Generation attempt "
                f"{attempt}/{MAX_RETRIES}"
            )


            # ---------------------------------
            # API REQUEST
            # ---------------------------------

            response = requests.post(

                API_URL,

                headers=headers,

                files={
                    "none": ""
                },

                data=data,

                timeout=(
                    CONNECT_TIMEOUT,
                    READ_TIMEOUT
                )

            )


            # =================================
            # SUCCESS
            # =================================

            if response.status_code == 200:

                print(
                    "Image generated successfully."
                )

                return response.content


            # =================================
            # RATE LIMIT
            # =================================

            if response.status_code == 429:

                last_error = (
                    "The AI service is "
                    "temporarily rate-limited."
                )

                print(last_error)

                if attempt < MAX_RETRIES:

                    wait_time = (
                        2 ** attempt
                    )

                    print(
                        f"Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(
                        wait_time
                    )

                    continue


                break


            # =================================
            # AUTHENTICATION
            # =================================

            if response.status_code in (
                401,
                403
            ):

                raise Exception(
                    "The Stability API key is "
                    "invalid or the request "
                    "was not authorized."
                )


            # =================================
            # INVALID REQUEST
            # =================================

            if response.status_code in (
                400,
                422
            ):

                try:

                    error_data = (
                        response.json()
                    )

                    raise Exception(
                        str(error_data)
                    )

                except ValueError:

                    raise Exception(
                        "The AI service rejected "
                        "the request."
                    )


            # =================================
            # SERVER ERROR
            # =================================

            if response.status_code >= 500:

                last_error = (
                    "The AI service encountered "
                    "a temporary server error."
                )

                print(last_error)

                if attempt < MAX_RETRIES:

                    wait_time = (
                        2 ** attempt
                    )

                    time.sleep(
                        wait_time
                    )

                    continue


                break


            # =================================
            # OTHER ERROR
            # =================================

            last_error = (
                f"API request failed "
                f"with status "
                f"{response.status_code}."
            )

            break


        # =====================================
        # TIMEOUT
        # =====================================

        except requests.exceptions.Timeout:

            last_error = (
                "The image generation "
                "request timed out."
            )

            print(last_error)

            if attempt < MAX_RETRIES:

                wait_time = (
                    2 ** attempt
                )

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(
                    wait_time
                )

                continue


        # =====================================
        # CONNECTION ERROR
        # =====================================

        except requests.exceptions.ConnectionError:

            last_error = (
                "Could not connect to "
                "the AI service."
            )

            print(last_error)

            if attempt < MAX_RETRIES:

                wait_time = (
                    2 ** attempt
                )

                time.sleep(
                    wait_time
                )

                continue


    # =====================================
    # FINAL FAILURE
    # =====================================

    raise Exception(
        last_error or
        "Image generation failed."
    )