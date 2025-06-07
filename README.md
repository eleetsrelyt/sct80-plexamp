# 🎛️ SCT-80 Vintage Tape Deck Plexamp Build

This project converts a 1980s **Realistic SCT-80 stereo cassette deck** into a modern streaming music player powered by a Raspberry Pi running [Plexamp Headless](https://plexamp.com). It uses the original buttons, meters, and shell—blending analog charm with digital brains.

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