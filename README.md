# Meow Bypass

A tool for bypassing DPI (Deep Packet Inspection) network blocks.

## Features

- Bypass website blocking without VPN
- Two different methods for DPI circumvention
- Special configurations for Discord, Cloudflare, and other services
- Simple graphical user interface

## How It Works

Meow Bypass uses the WinDivert library to intercept and modify network traffic. The program applies various DPI bypass techniques:

- TCP packet fragmentation (split method)
- SSL/TLS header spoofing (fake-tls)
- Special handling of QUIC protocol
- TTL manipulations
- Packet sequence modifications

## Installation

1. Download the executable from the [release page](https://github.com/Whiskydumb/meow-bypass/releases/latest)

2. Run meow.exe as administrator (required for WinDivert operation)

## Usage

1. Select a bypass method in settings:
   - Method 1: Primary method for most blocks
   - Method 2: Alternative method with additional parameters

2. Press the "Start" button to begin bypassing

3. The program will work in the background, intercepting and modifying traffic

4. To stop the bypass, press the "Stop" button

## System Requirements

- Windows 7/8/10/11
- Administrator privileges
- Antivirus disabled (may block WinDivert)

## Troubleshooting

- If the program doesn't start, make sure you're running it as administrator
- If initialization errors occur, check that all required files are present
- If some websites still don't open, try the alternative bypass method

## License

This project is distributed under the [MIT](https://github.com/Whiskydumb/meow-bypass/blob/main/LICENSE) license

## Inspired By

- [GoodbyeDPI](https://github.com/ValdikSS/GoodbyeDPI)
- [Zapret](https://github.com/bol-van/zapret)