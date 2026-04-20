# dFlash MCP Server

This is an MCP (Model Context Protocol) server wrapper for `dflash.exe`, a Windows executable for interfacing with Xbox One consoles over USB serial. It exposes common commands like dumping the flash, reading/writing files, reading fuse values, and querying headers, so that they can be invoked directly by AI agents.

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

## Configuring in AnythingLLM

To make this server available as an agent skill inside AnythingLLM, follow these steps:

1. Open AnythingLLM and navigate to **Settings** (the gear icon).
2. Go to **Agent Skills** (or the corresponding agents section).
3. Under **Agent MCP Servers**, click **Add New MCP Server**.
4. Fill out the configuration with the following settings:
   *   **Name:** `dFlash-Xbox` (or any name you prefer)
   *   **Command:** `python` 
       *(Or specify the absolute path to `python.exe` inside your virtual environment, for example: `C:\Users\titleos\source\repos\dsmcMCPServer\dsmcvenv\Scripts\python.exe`)*
   *   **Args:** `server.py`
       *(If AnythingLLM runs this from a different working directory, provide the absolute path to the `server.py` script instead).*
5. Save your changes. AnythingLLM will attempt to securely start the MCP server using standard I/O communication.

Once successfully loaded, the AI agent inside AnythingLLM will automatically be aware of your tools, such as `read_flash_remote_file`, `dump_fuses`, `dump_header`, `power_on`, and `write_flash_offset`, which it can use to directly inspect and manipulate the attached Xbox One console. 

## Supported Operations

*   Reading logic slots, binary offsets, and remote files
*   Writing new images/files to offsets or remote files
*   Viewing Slot A, B, C headers
*   Issuing power-on, reset, and bypass commands
*   Dumping SMC static fuses
*   Viewing and setting SMC settings
*   Setting eMMC frequencies
