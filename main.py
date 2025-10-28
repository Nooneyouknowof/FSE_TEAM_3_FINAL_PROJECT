import os
import sys
import cv2
import time
import base64
import RPi.GPIO as GPIO
from openai import OpenAI
from dotenv import load_dotenv

settings = {
    "Model": "gpt-5-nano-2025-08-07",
    "Camera_Index": 0, # The specific Camera you want to use
    "Resolution": [640, 480]
}

pi_board = {
    "GPIO17": 17
}

# Apply Settings
load_dotenv()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pi_board["GPIO17"], GPIO.OUT) # GPIO17
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, settings["Resolution"][0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, settings["Resolution"][1])
print(os.getenv("OPEN_AI_KEY"))
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


def take_picture():
    (img_success, frame) = cam.read() # tuple[bool, MatLike]
    cam.release()
    if img_success:
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')
    else:
        print("Error: The camera failed to read?", file=sys.stderr)


def read_image(base64_image):
    System_prompt = (
        "Reply with EXACTLY ONE short sentence (<= 15 words) "
        "describing the main visible objects. Do not read text."
    )

    data_responce = client.responses.create(
        model = settings["Model"],
        reasoning = {"effort": "low"},     # minimize hidden reasoning for speed
        max_output_tokens = 1024,          # big headroom -> no practical cap
        input = [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": System_prompt},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ]
        }],
    ).model_dump()

    return data_responce["output"][1]["content"][0]["text"]

def vibrate(pin_name, t):
    pin = pi_board[pin_name]
    print(pin_name, pin)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(t)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(t)

def main():
    print("Starting Program")
    while True:
        vibrate("GPIO17", 1)
    # image = take_picture()
    # image_desc = read_image(image)
    # print(image_desc)


if __name__ == "__main__":
    main()