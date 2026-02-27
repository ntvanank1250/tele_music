import asyncio
import logging
import os
import platform
import sys
import time
from typing import Dict, List, Optional

try:
    import psutil
except ImportError:
    psutil = None

logger = logging.getLogger(__name__)


async def _run_command(cmd: List[str]) -> tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()
    except FileNotFoundError:
        return -1, "", "Command not found"
    except Exception as exc:
        logger.exception("Error running command %s: %s", cmd, exc)
        return -1, "", str(exc)


async def get_system_info() -> str:
    """Get comprehensive system information."""
    info_parts = []
    
    # OS Information
    info_parts.append("🖥️ HỆ THỐNG")
    info_parts.append(f"OS: {platform.system()} {platform.release()}")
    info_parts.append(f"Architecture: {platform.machine()}")
    info_parts.append(f"Hostname: {os.uname().nodename}")
    info_parts.append(f"Python: {sys.version.split()[0]}")
    
    # Uptime if psutil available
    if psutil:
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = int(time.time() - boot_time)
            uptime_str = _format_uptime(uptime_seconds)
            info_parts.append(f"Uptime: {uptime_str}")
        except Exception as exc:
            logger.warning("Error getting uptime: %s", exc)
    
    # CPU and Memory info (if psutil is available)
    if psutil:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info_parts.append(f"\n💻 TÀI NGUYÊN")
            info_parts.append(f"CPU: {cpu_count} cores ({cpu_percent}% used)")
            info_parts.append(
                f"RAM: {_format_bytes(memory.used)} / {_format_bytes(memory.total)} "
                f"({memory.percent}%)"
            )
            info_parts.append(
                f"Disk: {_format_bytes(disk.used)} / {_format_bytes(disk.total)} "
                f"({disk.percent}%)"
            )
        except Exception as exc:
            logger.warning("Error getting system resources: %s", exc)
    else:
        info_parts.append(f"\n💻 TÀI NGUYÊN")
        info_parts.append("⚠️ psutil not installed - detailed resource info unavailable")
    
    # Docker info
    docker_info = await get_docker_info()
    if docker_info:
        info_parts.append(f"\n{docker_info}")
    
    # Supervisor info
    supervisor_info = await get_supervisor_info()
    if supervisor_info:
        info_parts.append(f"\n{supervisor_info}")
    
    return "\n".join(info_parts)


async def get_docker_info() -> Optional[str]:
    """Get Docker containers information."""
    # Check if docker is available
    returncode, _, _ = await _run_command(["docker", "--version"])
    if returncode != 0:
        # Docker not accessible (normal in container), return None to skip
        return None
    
    try:
        # Get all containers
        all_containers = await _get_docker_containers(all_containers=True)
        running_containers = await _get_docker_containers(all_containers=False)
        
        if not all_containers:
            return None
        
        info_parts = ["🐳 DOCKER"]
        info_parts.append(f"Total containers: {len(all_containers)}")
        info_parts.append(f"Running: {len(running_containers)}")
        
        if running_containers:
            info_parts.append("\nRunning Containers:")
            for container in running_containers:
                info_parts.append(
                    f"  • {container['name']} ({container['image']}) - {container['status']}"
                )
        
        if len(all_containers) > len(running_containers):
            stopped_containers = [
                c for c in all_containers 
                if c not in running_containers
            ]
            info_parts.append(f"\nStopped Containers: {len(stopped_containers)}")
            for container in stopped_containers[:5]:  # Show max 5 stopped
                info_parts.append(f"  • {container['name']} - {container['status']}")
            
            if len(stopped_containers) > 5:
                info_parts.append(f"  ... and {len(stopped_containers) - 5} more")
        
        return "\n".join(info_parts)
        
    except Exception as exc:
        logger.exception("Error getting Docker info: %s", exc)
        return "🐳 DOCKER\nError retrieving Docker info"


async def _get_docker_containers(all_containers: bool = False) -> List[Dict[str, str]]:
    """Get list of Docker containers."""
    cmd = ["docker", "ps", "--format", "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}"]
    if all_containers:
        cmd.insert(2, "-a")
    
    returncode, stdout, stderr = await _run_command(cmd)
    
    if returncode != 0:
        logger.error("Docker ps failed: %s", stderr)
        return []
    
    containers = []
    for line in stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            containers.append({
                "id": parts[0],
                "name": parts[1],
                "image": parts[2],
                "status": parts[3]
            })
    
    return containers


async def get_supervisor_info() -> Optional[str]:
    """Get Supervisor programs information."""
    # Check if supervisorctl is available
    returncode, _, _ = await _run_command(["supervisorctl", "version"])
    if returncode != 0:
        # Supervisor not accessible, return None to skip
        return None
    
    try:
        # Get all programs status
        returncode, stdout, stderr = await _run_command(["supervisorctl", "status"])
        
        if returncode not in [0, 3]:  # 3 = some programs not running
            logger.error("supervisorctl status failed: %s", stderr)
            return None
        
        programs = _parse_supervisor_status(stdout)
        
        if not programs:
            return "⚙️ SUPERVISOR\nNo programs configured"
        
        running_programs = [p for p in programs if p["state"] == "RUNNING"]
        stopped_programs = [p for p in programs if p["state"] != "RUNNING"]
        
        info_parts = ["⚙️ SUPERVISOR"]
        info_parts.append(f"Total programs: {len(programs)}")
        info_parts.append(f"Running: {len(running_programs)}")
        
        if running_programs:
            info_parts.append("\nRunning Programs:")
            for program in running_programs:
                uptime = program.get("uptime", "")
                info_parts.append(f"  • {program['name']} - {uptime}")
        
        if stopped_programs:
            info_parts.append(f"\nStopped Programs: {len(stopped_programs)}")
            for program in stopped_programs:
                info_parts.append(f"  • {program['name']} - {program['state']}")
        
        return "\n".join(info_parts)
        
    except Exception as exc:
        logger.exception("Error getting Supervisor info: %s", exc)
        return "⚙️ SUPERVISOR\nError retrieving Supervisor info"


def _parse_supervisor_status(output: str) -> List[Dict[str, str]]:
    """Parse supervisorctl status output."""
    programs = []
    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        
        # Format: "program_name    STATE    uptime/info"
        parts = line.split(None, 2)  # Split on whitespace, max 3 parts
        if len(parts) >= 2:
            program = {
                "name": parts[0],
                "state": parts[1]
            }
            if len(parts) >= 3:
                program["uptime"] = parts[2]
            programs.append(program)
    
    return programs


def _format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f}PB"


def _format_uptime(seconds: int) -> str:
    """Format uptime to human-readable format."""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "< 1m"
