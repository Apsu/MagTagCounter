import time
import terminalio
from adafruit_magtag.magtag import MagTag
from buttons import Buttons

magtag = MagTag()

magtag.peripherals.speaker_disable = True
magtag.peripherals.neopixel_disable = True
brightness = magtag.peripherals.neopixels.brightness = 0.5

rows = 0
stitches = 0

midx = magtag.graphics.display.width // 2 - 1

magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(10, 0),
    text_anchor_point=(0, 0),
    text_scale=3,
    is_data=False
)

magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(midx, 0),
    text_anchor_point=(0, 0),
    text_scale=3,
    is_data=False
)

magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(10, 30),
    text_anchor_point=(0, 0),
    text_scale=5,
    is_data=False
)

magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(175, 30),
    text_anchor_point=(0, 0),
    text_scale=5,
    is_data=False
)

magtag.add_text(
    text_font=terminalio.FONT,
    text_position=(245, 100),
    text_anchor_point=(0, 0),
    text_scale=1,
    is_data=False
)

def battery():
    return f"BAT {magtag.peripherals.battery / 4.2 * 100.0:.0f}%"

magtag.set_text("Rows", index=0, auto_refresh=False)
magtag.set_text("Stitches", index=1, auto_refresh=False)
magtag.set_text(f"{rows:4}", index=2, auto_refresh=False)
magtag.set_text(f"{stitches:4}", index=3, auto_refresh=False)
magtag.set_text(f"{battery()}", index=4, auto_refresh=False)
magtag.refresh()

# buttons = [False] * 4
battery_timer = time.monotonic()

# Initialize button list
buttons = Buttons(magtag.peripherals.buttons)

while True:
    # Update button states
    buttons.poll()

    # If any were pressed/released
    if buttons.pressed:
        # Update timestamp and battery status so it doesn't refresh during button presses
        battery_timer = time.monotonic()
        magtag.set_text(f"{battery()}", index=4, auto_refresh=False)

        # If A down
        if buttons[0].down:
            # Latch so A doesn't count this as a press when released
            buttons[0].latch()
            # And B pressed
            if buttons[1].pressed:
                # Decrease brightness
                magtag.peripherals.neopixels.brightness = brightness = max(brightness - 0.1, 0.1)
            # Or C pressed
            elif buttons[2].pressed:
                # Increase brightness
                magtag.peripherals.neopixels.brightness = brightness = min(brightness + 0.1, 1.0)
            # Or D pressed
            elif buttons[3].pressed:
                # Toggle lights
                magtag.peripherals.neopixel_disable = not magtag.peripherals.neopixel_disable
                # Pink!
                magtag.peripherals.neopixels.fill((255, 50, 200))
        # Otherwise just a press
        else:
            # A was pressed
            if buttons[0].pressed:
                rows = (rows - 1) % 10000
                magtag.set_text(f"{rows:4}", index=2, auto_refresh=False)
            # B was pressed
            elif buttons[1].pressed:
                rows = (rows + 1) % 10000
                magtag.set_text(f"{rows:4}", index=2, auto_refresh=False)
            # C was pressed
            elif buttons[2].pressed:
                stitches = (stitches - 1) % 10000
                magtag.set_text(f"{stitches:4}", index=3, auto_refresh=False)
            # D was pressed
            elif buttons[3].pressed:
                stitches = (stitches + 1) % 10000
                magtag.set_text(f"{stitches:4}", index=3, auto_refresh=False)

            # Refresh with updates
            magtag.refresh()
    # If timeout has elapsed since last battery update
    elif time.monotonic() - battery_timer >= 60.0:
        # Advance timestamp
        battery_timer = time.monotonic()
        # Update battery meter and force refresh
        magtag.set_text(f"{battery()}", index=4, auto_refresh=True)
    # No buttons pressed or some still held
    else:
        # Sleep 100ms
        time.sleep(0.1)
