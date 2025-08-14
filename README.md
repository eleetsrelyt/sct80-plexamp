# 🎛️ SCT-80 Vintage Tape Deck Plexamp Build

This project transforms a 1980s **Realistic SCT‑80 stereo cassette deck** into a fully modern streaming music player powered by a Raspberry Pi running [Plexamp Headless](https://plexamp.com). It retains the original front‑panel controls, LEDs, and overall vintage look, while replacing the tape mechanism with digital audio hardware and smart GPIO control. The result is an analog‑era design with digital convenience.

In addition to basic playback, the build integrates LED feedback, a relay‑controlled display, and custom scripts that allow the original buttons to control Plexamp over its local API for near‑instant responsiveness.

![SCT-80 Front Panel](images/IMG_6402.jpeg)

---

## 🛠️ What It Does

- **Raspberry Pi 3** embedded in the tape deck
- Runs **Plexamp in headless mode** (via `odinb` install)
- All original front panel **buttons and LEDs repurposed** through GPIO
- **USB DAC** feeds audio through the original RCA jacks
- **4” HDMI display** replaces the tape window, shows album art and playback info
- Physical **button controls** for Play, Stop, Next, etc.
- LED feedback for **playback status**
- **Relay-based screen power** (screen only turns on when the deck is powered)
- Entire system mounts inside the original SCT-80 chassis

- Reads playback state and metadata directly from Plexamp's **local port (localhost)** for faster updates and reduced dependency on the Plex Media Server

---

## 🧠 Control Mapping and GPIO Reference

These charts show how the original SCT-80 buttons, LEDs, and display wiring were mapped to the Raspberry Pi GPIO:

### Front Panel Mapping
![Front Panel GPIO Map](images/front_GPIO.png)

### Switch and LED Matrix Details
![Matrix Wiring Map](images/wires_buttons_leds.png)

---

## 📸 Build Photos

| Original Interior | Pi + GPIO Installed | Final Look |
|------------------|----------------------|------------|
| ![Before](images/IMG_6209.jpeg) | ![Wired](images/IMG_6398.jpeg) | ![Final](images/IMG_6402.jpeg) |

---

## 📁 Folder Structure

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
├── env.example          # Safe placeholder for .env
├── gpio_config.py
├── led_control.py
├── main.py              # Starts GPIO listeners and state loop
├── plexamp_api.py       # Unofficial Plexamp Web API controller
├── README.md
└── state_manager.py
```

---

## 🚀 Features in Detail

- **Local API Integration** – All real‑time LED updates and button actions use Plexamp’s local `/player/timeline/poll` endpoint, minimizing network latency and avoiding unnecessary server calls.
- **Physical Controls** – Every button from the SCT‑80 has been mapped via a GPIO switch matrix. Actions include Play/Pause, Next/Previous track, Star (rating), Repeat, Shuffle (future), Random Album Radio, and power‑controlled display backlight.
- **LED Feedback** – Original LED indicators light or blink based on player state (e.g., Play LED on when playing, Pause LED blinking when paused). Additional LEDs are available for genre/mood or other metadata.
- **Relay‑Based Display Control** – The HDMI display behind the cassette window powers on only when the SCT‑80’s physical power switch is engaged.
- **Easy Extensibility** – Actions and LED mappings are driven by `button_config.py` and `led_control.py`, making it simple to change behaviors without rewiring.
- **Headless Operation** – The Raspberry Pi runs Plexamp in headless mode via the `odinb` install method, outputting audio through a USB DAC to the original RCA connectors.

---

## ⚙️ Setup & Configuration

1. **Hardware Prep**
   - Remove the tape mechanism and mount the Raspberry Pi 3 inside the SCT‑80 chassis.
   - Connect button and LED wiring to the Pi via GPIO according to `gpio_config.py`.
   - Install a relay module for the display backlight, wired to the SCT‑80’s power switch and Pi control pin.

2. **Software Installation**
   - Install Raspberry Pi OS Lite (64‑bit recommended).
   - Install Plexamp Headless using [odinb’s guide](https://howtohifi.com/how-to-create-a-headless-plexamp-player-using-odinbs-plexamp-installer-script/).
   - Clone this repository to the Pi.

3. **Environment Variables**
   - Copy `env.example` to `.env` and set:
     ```
     PLEXAMP_PORT=32500
     PLEXAMP_TOKEN=your_plexamp_token
     PLEXAMP_PLAYER=your_player_id
     PLEX_SERVER=your_plex_server_ip
     PLEX_PORT=32400
     ```
   - `PLEX_SERVER` and `PLEX_PORT` are only used for rating (star) actions; all other commands use `localhost`.

4. **Run the Controller**
   ```
   nohup python3 main.py &
   ```
   This will start GPIO scanning and LED state updates in the background.

---

## 🧪 Testing

Test scripts are available in `user_scripts/`:
- `led_tester.py` – Cycle through LEDs to verify wiring.
- `button_matrix_test.py` – Detect button presses in the switch matrix.
- `status_test.py` – Query Plexamp’s local timeline and display playback state.

---

## 📌 Notes

- This build assumes the SCT‑80’s LEDs are wired as per the documented matrix; if yours differs, adjust `LED_PINS` and `LED_COMMON` in `gpio_config.py`.
- The `star` function uses the local API to get the current track’s `ratingKey` and then calls the Plex Media Server only to submit the rating.
- Repeat and Shuffle actions are placeholders until Plexamp exposes them in the local API.