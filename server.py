from mcp.server.fastmcp import FastMCP
import subprocess
import os

mcp = FastMCP("dFlash Xbox Utility")

def run_dflash(args: list[str]) -> str:
    """Helper function to run dflash.exe with the specified arguments."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dflash.exe')
    if not os.path.exists(path):
        # Fallback in case it's in the system PATH
        path = "dflash.exe"
        
    # Always append /NoPause so it doesn't block waiting for a key press
    cmd = [path] + args + ["/NoPause"]
    
    try:
        # Always reset the FPGA before doing anything else
        if "/Reset" not in args and "/ResetCycle" not in args:
            subprocess.run([path, "/Reset", "/NoPause"], capture_output=True, check=False)
            
        # Some dflash commands might write to stderr or return non-zero exit codes.
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        output = result.stdout.strip()
        if result.stderr:
            output += "\n[STDERR]:\n" + result.stderr.strip()
            
        if result.returncode != 0:
            return f"Command failed with exit code {result.returncode}:\n{output}"
            
        return output
    except Exception as e:
        return f"Error executing dflash: {str(e)}"

@mcp.tool()
def read_flash_offset(output_file: str, offset: str, length: str) -> str:
    """
    Read data from flash memory and write it to a local file.
    
    Args:
        output_file: The local file path to save the dumped contents.
        offset: The starting offset address in flash (decimal or hex like 0x10000).
        length: The length of data to read (decimal or hex).
    """
    args = [f"/RawRead:{output_file}", f"/Offset:{offset}", f"/Length:{length}"]
    return run_dflash(args)

@mcp.tool()
def read_flash_remote_file(output_file: str, remote_file: str) -> str:
    """
    Read a specific logical file from the console's flash memory and save it locally.
    
    Args:
        output_file: The local file path to save the dumped contents.
        remote_file: The remote file to read (e.g. 'A\\smc_d.cfg' or just file name). Use dump_headers to find files.
    """
    args = [f"/RawRead:{output_file}", f"/RemoteFile:{remote_file}"]
    return run_dflash(args)

@mcp.tool()
def write_flash_offset(input_file: str, offset: str) -> str:
    """
    Write a local file to the flash memory at a specific offset address.
    
    Args:
        input_file: The local file to write to the flash memory.
        offset: The starting offset address in flash (decimal or hex).
    """
    args = [f"/RawWrite:{input_file}", f"/Offset:{offset}"]
    return run_dflash(args)

@mcp.tool()
def write_flash_remote_file(input_file: str, remote_file: str) -> str:
    """
    Write a local file to a specific remote logical file on the console's flash.
    
    Args:
        input_file: The local file to write.
        remote_file: The remote file to overwrite (e.g. 'A\\smc_d.cfg').
    """
    args = [f"/RawWrite:{input_file}", f"/RemoteFile:{remote_file}"]
    return run_dflash(args)

@mcp.tool()
def overwrite_flash(offset: str, length: str) -> str:
    """
    Write 0xFF to the flash memory for the specified offset and length.
    
    Args:
        offset: The starting offset address in flash (decimal or hex).
        length: The length of data to overwrite (decimal or hex).
    """
    args = ["/RawOverWrite", f"/Offset:{offset}", f"/Length:{length}"]
    return run_dflash(args)

@mcp.tool()
def dump_header(slot: str) -> str:
    """
    Dump the FLASH_HEADER structure associated with the specified slot (A, B, or C).
    Useful for seeing available remote file names.
    
    Args:
        slot: "A", "B", or "C"
    """
    slot = slot.upper()
    if slot not in ["A", "B", "C"]:
        return "Error: Slot must be A, B, or C."
        
    return run_dflash([f"/DumpHeader{slot}"])

@mcp.tool()
def dump_fuses() -> str:
    """
    Dumps the fuse values that the SMC places in the SPI-visible registers.
    """
    return run_dflash(["/DumpFuses"])

@mcp.tool()
def power_on() -> str:
    """
    Power on the FPGA and daughter board.
    """
    return run_dflash(["/PowerOn"])

@mcp.tool()
def reset() -> str:
    """
    Reset the FPGA.
    """
    return run_dflash(["/Reset"])

@mcp.tool()
def reset_cycle() -> str:
    """
    Perform a reset cycle (/Reset followed by /ResetRelease).
    """
    return run_dflash(["/ResetCycle"])

@mcp.tool()
def smc_list() -> str:
    """
    List the available SMC settings to modify, with descriptions.
    """
    return run_dflash(["/smcset:list"])

@mcp.tool()
def smc_set(setting: str) -> str:
    """
    Modify an SMC static or dynamic setting.
    
    Args:
        setting: The setting command, e.g. 'init', 'init:a\\smc_d.cfg', 'Name=TRUE', '*\\Name=Value'.
    """
    return run_dflash([f"/smcset:{setting}"])

@mcp.tool()
def set_clock_speed(mhz: float) -> str:
    """
    Sets the SDCLK frequency in the eMMC Clock Control register.
    
    Args:
        mhz: Frequency in MHz, such as 50, 24.6, or 196.875
    """
    return run_dflash([f"/sdclk:{mhz}"])

if __name__ == "__main__":
    mcp.run()
