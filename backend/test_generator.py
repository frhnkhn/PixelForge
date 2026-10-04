from image_generator import generate_image


prompt = """
A futuristic cyberpunk city at night,
neon lights, flying cars, rain,
cinematic lighting, highly detailed
"""


print("Generating image...")
print("Please wait...")


try:
    image_data = generate_image(
        prompt=prompt,
        aspect_ratio="16:9",
        style_preset="cinematic",
        output_format="png"
    )

    with open("../generated/test.png", "wb") as file:
        file.write(image_data)

    print("SUCCESS!")
    print("Image saved to generated/test.png")

except Exception as error:
    print("ERROR:")
    print(error)