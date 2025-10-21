import subprocess
import base64
import sys
from openai import OpenAI


client = OpenAI(api_key="sk-REPLACE_WITH_NEW_KEY")

MODEL = "gpt-5-nano-2025-08-07"
IMAGE_PATH = "captured_image.jpg"
RESOLUTION = "640x480"             

def capture_image(path: str):
    # -S 2 skips a couple frames so exposure settles faster
    subprocess.run(["fswebcam", "-r", RESOLUTION, "-S", "2", "--no-banner", path], check=True)

def to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

def extract_text(resp):
    text = getattr(resp, "output_text", None)
    if text:
        return text.strip()
    try:
        for item in getattr(resp, "output", []):
            for part in getattr(item, "content", []):
                if getattr(part, "type", None) in ("output_text", "text") and getattr(part, "text", None):
                    return part.text.strip()
    except Exception:
        pass
    try:
        return resp.model_dump_json(indent=2)
    except Exception:
        return str(resp)

def main():
    try:
        capture_image(IMAGE_PATH)
        data_url = to_data_url(IMAGE_PATH)

        prompt = (
            "Reply with EXACTLY ONE short sentence (<= 15 words) "
            "describing the main visible objects. Do not read text."
        )

        resp = client.responses.create(
            model=MODEL,
            reasoning={"effort": "low"},     # minimize hidden reasoning for speed
            max_output_tokens=1024,           # big headroom -> no practical cap
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url}
                ]
            }],
        )

        print(extract_text(resp))

    except Exception as e:
        print("ERROR:", repr(e), file=sys.stderr)
        raise

if __name__ == "__main__":
    main()


# !/usr/bin/env python3
# import RPi.GPIO as GPIO
# import time
# Buzzer = 11 # pin11
# def setup(pin):
# global BuzzerPin
# BuzzerPin = pin
# GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
# GPIO.setup(BuzzerPin, GPIO.OUT)
# GPIO.output(BuzzerPin, GPIO.HIGH)
# def on():
# GPIO.output(BuzzerPin, GPIO.LOW)
# def off():
# GPIO.output(BuzzerPin, GPIO.HIGH)
# def beep(x):
# on()
# time.sleep(x)
# off()
# time.sleep(x)
# def loop():
# while True:
# beep(0.5)
# def destroy():
# GPIO.output(BuzzerPin, GPIO.HIGH)
# GPIO.cleanup() # Release resource
# if __name__ == '__main__': # Program start from here
# setup(Buzzer)
# try:
# loop()
# except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
# destroy()
