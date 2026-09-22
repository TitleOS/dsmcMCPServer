# dFlash MCP Server

This is an MCP (Model Context Protocol) server wrapper for `dflash.exe`, a Windows executable for interfacing with Xbox One consoles over USB serial via an official or unofficial FTDI device. It exposes common commands like dumping the flash, reading/writing files, reading fuse values, and querying headers, so that they can be invoked directly by AI agents.

## Prerequisites

1.  **Python 3.10+** - Make sure Python is installed and optionally added to your PATH.
2.  **dflash.exe** - Obtain the executable and its dependencies (`dsmcdll.exe` etc) and place them in the root of this project folder.
3.  **FTDI Device** - An Xbox One flash interface must be connected via USB. The server assumes the **first active FTDI device** represents the console you are interacting with.

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv dsmcvenv
   ```
2. Activate it:
   ```bash
   .\dsmcvenv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Use cases:

* Automated restarting of console upon crash due to driver fuzzing, allowing for atleast partially automated fuzzing of Xbox OS drivers. 

## Supported Operations

*   Reading logic slots, binary offsets, and remote files
*   Writing new images/files to offsets or remote files
*   Viewing Slot A, B, C headers
*   Issuing power-on, reset, and bypass commands
*   Dumping SMC static fuses
*   Viewing and setting SMC settings
*   Setting eMMC frequencies
