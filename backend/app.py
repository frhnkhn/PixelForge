import os
import uuid
import time

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    send_file
)

from PIL import Image
from io import BytesIO

from validator import (
    validate_prompt,
    validate_settings,
    validate_negative_prompt,
    validate_seed
)

from image_generator import generate_image


app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

GENERATED_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "generated"
    )
)

os.makedirs(
    GENERATED_FOLDER,
    exist_ok=True
)


# =========================================================
# FRONTEND
# =========================================================

@app.route("/")
def home():

    frontend_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "frontend",
            "index.html"
        )
    )

    return send_file(frontend_path)


@app.route("/style.css")
def stylesheet():

    css_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "frontend",
            "style.css"
        )
    )

    return send_file(css_path)


@app.route("/script.js")
def javascript():

    js_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "frontend",
            "script.js"
        )
    )

    return send_file(js_path)


# =========================================================
# GENERATE IMAGE
# =========================================================

@app.route(
    "/api/generate",
    methods=["POST"]
)
def generate():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        # -------------------------------------------------
        # INPUTS
        # -------------------------------------------------

        prompt = data.get(
            "prompt",
            ""
        ).strip()


        aspect_ratio = data.get(
            "aspect_ratio",
            "1:1"
        )


        negative_prompt = data.get(
            "negative_prompt",
            ""
        ).strip()


        style_preset = data.get(
            "style_preset",
            "photographic"
        )


        output_format = data.get(
            "output_format",
            "png"
        )


        seed = data.get(
            "seed",
            0
        )


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        valid, error = validate_prompt(
            prompt
        )

        if not valid:

            return jsonify({
                "success": False,
                "error": error
            }), 400


        valid, error = validate_negative_prompt(
            negative_prompt
        )

        if not valid:

            return jsonify({
                "success": False,
                "error": error
            }), 400


        valid, error = validate_settings(
            aspect_ratio,
            style_preset,
            output_format
        )

        if not valid:

            return jsonify({
                "success": False,
                "error": error
            }), 400


        valid, error = validate_seed(
            seed
        )

        if not valid:

            return jsonify({
                "success": False,
                "error": error
            }), 400


        # -------------------------------------------------
        # DISPLAY REQUEST
        # -------------------------------------------------

        print("")
        print("================================")
        print("       NEW IMAGE REQUEST")
        print("================================")
        print("Prompt:", prompt)
        print("Aspect Ratio:", aspect_ratio)
        print("Style:", style_preset)
        print("Format:", output_format)
        print("Seed:", seed)
        print("================================")
        print("Generating image...")
        print("")


        # -------------------------------------------------
        # GENERATE
        # -------------------------------------------------

        start_time = time.time()


        image_bytes = generate_image(

            prompt=prompt,

            aspect_ratio=aspect_ratio,

            negative_prompt=negative_prompt,

            style_preset=style_preset,

            output_format=output_format,

            seed=seed

        )


        generation_time = round(
            time.time() - start_time,
            2
        )


        # -------------------------------------------------
        # CHECK DATA
        # -------------------------------------------------

        if not image_bytes:

            return jsonify({
                "success": False,
                "error": "The AI service returned empty image data."
            }), 500


        # -------------------------------------------------
        # VERIFY IMAGE
        # -------------------------------------------------

        try:

            image_stream = BytesIO(
                image_bytes
            )

            image = Image.open(
                image_stream
            )

            image.verify()


            image_stream = BytesIO(
                image_bytes
            )

            image = Image.open(
                image_stream
            )

            image.load()


            width, height = image.size


            detected_format = (
                image.format or
                output_format.upper()
            )


        except Exception as image_error:

            print(
                "Image integrity error:",
                image_error
            )

            return jsonify({
                "success": False,
                "error": "Generated image is corrupted or invalid."
            }), 500


        # -------------------------------------------------
        # SAVE IMAGE
        # -------------------------------------------------

        image_id = str(
            uuid.uuid4()
        )


        filename = (
            f"{image_id}.{output_format}"
        )


        filepath = os.path.join(
            GENERATED_FOLDER,
            filename
        )


        with open(
            filepath,
            "wb"
        ) as file:

            file.write(
                image_bytes
            )


        file_size = os.path.getsize(
            filepath
        )


        created_time = os.path.getmtime(
            filepath
        )


        print("")
        print("Image generated successfully.")
        print("Resolution:", width, "x", height)
        print("Format:", detected_format)
        print("Generation time:", generation_time, "seconds")
        print("Saved:", filename)
        print("")


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "image":
                f"/generated/{filename}",

            "filename":
                filename,

            "prompt":
                prompt,

            "aspect_ratio":
                aspect_ratio,

            "style_preset":
                style_preset,

            "output_format":
                output_format,

            "seed":
                seed,

            "width":
                width,

            "height":
                height,

            "resolution":
                f"{width} × {height}",

            "size":
                file_size,

            "created":
                created_time,

            "generation_time":
                generation_time

        })


    except Exception as error:

        print("")
        print("================================")
        print("             ERROR")
        print("================================")
        print(error)
        print("================================")
        print("")


        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# GENERATION HISTORY
# =========================================================

@app.route(
    "/api/history"
)
def history():

    try:

        images = []


        for filename in os.listdir(
            GENERATED_FOLDER
        ):

            if not filename.lower().endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp"
                )
            ):

                continue


            filepath = os.path.join(
                GENERATED_FOLDER,
                filename
            )


            if not os.path.isfile(
                filepath
            ):

                continue


            try:

                file_size = os.path.getsize(
                    filepath
                )

                created_time = os.path.getmtime(
                    filepath
                )


                with Image.open(
                    filepath
                ) as image:

                    width, height = image.size

                    detected_format = (
                        image.format or
                        filename.split(".")[-1].upper()
                    )


                images.append({

                    "filename":
                        filename,

                    "image":
                        f"/generated/{filename}",

                    "created":
                        created_time,

                    "size":
                        file_size,

                    "width":
                        width,

                    "height":
                        height,

                    "resolution":
                        f"{width} × {height}",

                    "format":
                        detected_format

                })


            except Exception as error:

                print(
                    f"Could not read {filename}:",
                    error
                )


        images.sort(
            key=lambda item: item["created"],
            reverse=True
        )


        return jsonify({

            "success": True,

            "images":
                images

        })


    except Exception as error:

        print("")
        print("================================")
        print("       HISTORY ERROR")
        print("================================")
        print(error)
        print("================================")
        print("")


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# CLEAR HISTORY
# =========================================================

@app.route(
    "/api/history/clear",
    methods=["DELETE"]
)
def clear_history():

    try:

        deleted = 0


        for filename in os.listdir(
            GENERATED_FOLDER
        ):

            if not filename.lower().endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp"
                )
            ):

                continue


            filepath = os.path.join(
                GENERATED_FOLDER,
                filename
            )


            if os.path.isfile(
                filepath
            ):

                os.remove(
                    filepath
                )

                deleted += 1


        print(
            f"History cleared. Deleted {deleted} images."
        )


        return jsonify({

            "success": True,

            "deleted":
                deleted,

            "message":
                f"Deleted {deleted} generated images."

        })


    except Exception as error:

        print(
            "Clear history error:",
            error
        )


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# SERVE GENERATED IMAGES
# =========================================================

@app.route(
    "/generated/<filename>"
)
def generated_image(
    filename
):

    return send_from_directory(
        GENERATED_FOLDER,
        filename
    )


# =========================================================
# FAVICON
# =========================================================

@app.route(
    "/favicon.ico"
)
def favicon():

    return (
        "",
        204
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    "/api/health"
)
def health():

    return jsonify({

        "status":
            "online",

        "service":
            "PixelForge",

        "message":
            "PixelForge API is running."

    })


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("")
    print("================================")
    print("       PIXELFORGE SERVER")
    print("================================")
    print("")
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print("")
    print("Health check:")
    print("http://127.0.0.1:5000/api/health")
    print("")
    print("Generation history:")
    print("http://127.0.0.1:5000/api/history")
    print("")
    print("================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )