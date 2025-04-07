# Business Card Sharing Gadget

This project creates a business card sharing gadget using the Raspberry Pi Pico W (hereafter referred to as Pico W) that operates in Wi-Fi AP (Access Point) mode. It features a "captive portal" that automatically displays a business card (HTML) on connected devices.

A captive portal is a feature often seen in public Wi-Fi APs, such as those in airports, that redirects users to a notification or authentication page upon connection. In addition to HTML, this project can also deliver vCard (.vcf) files to devices. When a vCard (.vcf) is delivered, the device automatically launches its contacts app. This has been tested on iPhones.

## Features

- **Wi-Fi Access Point Mode**: The Pico W operates as a Wi-Fi AP.
- **Captive Portal**: Automatically delivers data to connected devices. In this case, it displays a business card in HTML format.
- **Customizable Business Card Information**: You can easily modify the business card content by editing the `namecard.html` file.
- **OLED Display Support**: Displays the SSID and password on an SSD1351 OLED display, allowing sharing only with people nearby.

## Requirements

- Raspberry Pi Pico W
- SSD1351 OLED
- MicroPython Firmware 1.29.0

## Optional

- Button: Connecting a button to 3V3EN allows you to restart the Pico W with a press, which is useful for development.

## Setup

1. **Clone the Code**:

   ```bash
   git clone https://github.com/tkumata/pico1w-namecard-wifiap-py.git
   git clone https://github.com/Tamakichi/pico_MicroPython_misakifont.git
   cp -pr pico_MicroPython_misakifont/misakifont pico1w-namecard-wifiap-py/
   cd pico1w-namecard-wifiap-py
   ```

2. **Configure Wi-Fi Information**: Copy `secrets.py.sample` to `secrets.py` and set the SSID and password.

   ```python
   SSID = "YourSSID"
   PASSWORD = "YourPassword"
   ```

3. **Edit the Business Card HTML**: Copy `namecard.html.sample` to `namecard.html` and customize the business card information.
4. **Upload the Code**: Upload the code to the Pico W. Right-click on the file list pane and select "Upload project to Pico."
5. **Verify Operation**: Connect a device to the Pico W's Wi-Fi, and the browser will automatically launch and display the business card.

## File Structure

- `main.py`: Main script that controls Wi-Fi AP mode and server operation.
- `ssd1351.py`: SSD1351 OLED display driver. Depends on `misakifont`.
- `namecard.html.sample`: Business card HTML template.
- `secrets.py.sample`: Sample file for Wi-Fi AP configuration.
- `misakifont`: Font data for the SSD1351 OLED display.
- `namecard.vcf.sample`: Sample file for delivering vCard instead of `namecard.html`.

## Usage

1. When the Pico W starts, the SSID and password are displayed on the OLED screen.
2. Connect to the specified SSID using a device such as an iPhone.
3. After connecting, the browser will automatically launch and display the business card HTML.

## Planned Features

- Display QR codes on the OLED display for easier Wi-Fi connection.
- Support for delivering arbitrary data, not limited to business cards.

## License

This project is released under the MIT License.

## Contribution

Bug reports and feature suggestions are welcome. Please send a pull request.
