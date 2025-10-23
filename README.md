# SCT-80 Vintage Tape Deck Plexamp Build

This project converts a 1980s Realistic SCT-80 cassette deck into a modern streaming player using a Raspberry Pi running Plexamp Headless. The goal is to keep the original look and front-panel controls while replacing the tape mechanism with digital audio and GPIO control. Buttons and LEDs work like they did on the deck, but now drive Plexamp over its local API.

The build adds LED feedback, a relay-controlled display behind the cassette window, and simple Python scripts to translate button presses into Plexamp actions. State and metadata are read from the local Plexamp port for quick updates without depending on the Plex Media Server.

---

## What it does

- Raspberry Pi 3 installed in the SCT-80 chassis
- Plexamp running in headless mode (installed via odinb guide)
- Original front-panel buttons and LEDs repurposed over GPIO
- USB DAC to the deck’s original RCA outputs
- 4" HDMI display behind the cassette window showing album art and status
- Physical buttons for play/pause, next/previous, star, repeat (placeholder), shuffle (placeholder), random album radio, and display backlight control
- LED feedback for player state
- Display backlight powered through a relay tied to the deck’s power switch
- Playback state and metadata read from Plexamp’s local port (localhost) to reduce latency

---

## Control mapping and GPIO reference

These diagrams show how the SCT-80 front panel maps to Raspberry Pi GPIO:

- Front panel mapping: `images/front_gpio.png`
- Switch and LED matrix: `images/wiring_buttons_leds.png`

Build photos are in `images/` (before, wiring, final).

---

## Folder structure

```plaintext
├── config/
│   └── user_settings.json
├── images/
│   ├── IMG_6209.jpeg
│   ├── IMG_6398.jpeg
│   └── IMG_6402.jpeg
├── shared/
│   └── temp.json
├── user_scripts/
│   ├── backlight_test.py
│   ├── button_matrix_test.py
│   ├── end_pointer.py
│   ├── led_tester.py
│   ├── play_button_test.py
│   └── status_test.py
├── actions.py
├── button_config.py
├── env.example          # template for .env
├── gpio_config.py
├── led_control.py
├── main.py              # starts GPIO listeners and state loop
├── plexamp_api.py       # local Plexamp API controller
├── README.md
└── state_manager.py
```

---

## How it works (details)

- Local API integration: real-time state and metadata come from the Plexamp local endpoint `/player/timeline/poll`, which avoids server delays.
- Physical controls: each original button is mapped via a switch matrix. Actions include play/pause, next/previous, star (rating), random album radio, repeat/shuffle placeholders, and backlight toggle.
- LED feedback: original LEDs indicate player state (for example, Play LED on when playing; Pause LED on when paused/stopped). Extra LEDs can be tied to metadata such as genre or mood.
- Display control: the HDMI display powers on only when the deck’s power switch is on, via a relay.
- Extensibility: actions and LED mappings are configured in `button_config.py` and `led_control.py`.

---

## Setup and configuration

1. Hardware
   - Remove the tape mechanism and mount the Raspberry Pi in the SCT-80.
   - Wire the button and LED matrix to GPIO as defined in `gpio_config.py`.
   - Add a relay for the display backlight and connect it to the deck’s power switch and a Pi control pin.

2. Software
   - Install Raspberry Pi OS Lite (64-bit recommended).
   - Install Plexamp Headless using odinb’s guide.
   - Clone this repository to the Pi.

3. Environment variables
   - Copy `env.example` to `.env` and set:
     ```
     PLEXAMP_PORT=32500
     PLEXAMP_TOKEN=your_plexamp_token
     PLEXAMP_PLAYER=your_player_id
     PLEX_SERVER=your_plex_server_ip
     PLEX_PORT=32400
     ```
   - The server values are only used for submitting ratings. All other calls use `localhost`.

4. Run the controller
   ```bash
   nohup python3 main.py &
   ```
   This starts GPIO scanning and LED updates in the background.

---

## Testing

Available in `user_scripts/`:
- `led_tester.py` — verify LED wiring
- `button_matrix_test.py` — check switch matrix input
- `status_test.py` — read player state via the local timeline endpoint

---

## Notes

- If your LED matrix wiring differs from the diagrams, adjust `LED_PINS` and `LED_COMMON` in `gpio_config.py`.
- The `star` function reads the current item’s `ratingKey` from the local poll and then sends a single request to the Plex Media Server to submit the rating.
- Repeat and shuffle are placeholders until Plexamp exposes those controls in the local API.