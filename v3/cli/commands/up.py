"""Start ObsStack observability backend."""
import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.docker.network_manager import NetworkManager

console = Console()

def up_command(detach: bool = True, build: bool = False):
    """
    Start ObsStack observability backend.
    
    Args:
        detach: Run in background
        build: Rebuild images before starting
    """
    console.print("\n🚀 [bold]Starting ObsStack observability backend...[/bold]\n")
    
    # Check if backend exists
    backend_dir = Path.cwd() / "backend"
    if not backend_dir.exists():
        console.print("[bold red]✗ Backend not found![/bold red]")
        console.print("\n[yellow]Run first:[/yellow] [cyan]obs-stack init[/cyan]\n")
        sys.exit(1)
    
    compose_file = backend_dir / "docker-compose.yml"
    if not compose_file.exists():
        console.print(f"[bold red]✗ {compose_file} not found![/bold red]\n")
        sys.exit(1)
    
    try:
        # 1. Create network
        console.print("🌐 [cyan]Setting up network...[/cyan]")
        network_manager = NetworkManager()
        network_manager.create_network()
        
        # 2. Start services
        console.print("\n📦 [cyan]Starting services...[/cyan]\n")
        
        cmd = ["docker-compose", "-f", str(compose_file)]
        
        if build:
            cmd.extend(["up", "--build"])
        else:
            cmd.append("up")
        
        if detach:
            cmd.append("-d")
        
        result = subprocess.run(
            cmd,
            cwd=backend_dir,
            capture_output=False,
            text=True
        )
        
        if result.returncode != 0:
            console.print("\n[bold red]✗ Failed to start services[/bold red]\n")
            sys.exit(1)
        
        # 3. Wait a bit for services to start
        import time
        console.print("\n⏳ [cyan]Waiting for services to start...[/cyan]")
        time.sleep(5)
        
        # 4. Check service status
        console.print()
        _check_services(backend_dir)
        
        # 5. Success message
        console.print(Panel(
            "[bold green]✅ ObsStack is running![/bold green]\n\n"
            "[white]Access:[/white]\n"
            "  📊 Grafana:    [cyan]http://localhost:3001[/cyan] (admin/obsstack)\n"
            "  📈 Prometheus: [cyan]http://localhost:9090[/cyan]\n"
            "  📝 Loki:       [cyan]http://localhost:3100[/cyan]\n"
            "  🔍 Tempo:      [cyan]http://localhost:3200[/cyan]\n\n"
            "[white]Next:[/white]\n"
            "  • Instrument apps: [cyan]obs-stack instrument <container>[/cyan]\n"
            "  • View logs: [cyan]obs-stack logs[/cyan]\n"
            "  • Stop: [cyan]obs-stack down[/cyan]",
            title="🎉 Success",
            border_style="green"
        ))
        console.print()
        
    except FileNotFoundError:
        console.print("\n[bold red]✗ docker-compose not found![/bold red]")
        console.print("Install: [cyan]https://docs.docker.com/compose/install/[/cyan]\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}\n")
        sys.exit(1)

def _check_services(backend_dir: Path):
    """Check status of backend services."""
    try:
        result = subprocess.run(
            ["docker-compose", "-f", "docker-compose.yml", "ps"],
            cwd=backend_dir,
            capture_output=True,
            text=True
        )
        
        # Parse output
        lines = result.stdout.strip().split('\n')
        if len(lines) < 3:
            console.print("[yellow]⚠️  No services found[/yellow]")
            return
        
        # Create status table
        table = Table(title="Service Status", show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Ports", style="yellow")
        
        # Parse service lines (skip header)
        for line in lines[2:]:
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                status = parts[3] if "Up" in line else "Down"
                
                # Extract ports
                ports = "N/A"
                if "->" in line:
                    port_parts = [p for p in parts if "->" in p]
                    if port_parts:
                        ports = port_parts[0].split("->")[0]
                
                status_color = "green" if "Up" in status else "red"
                status_icon = "✅" if "Up" in status else "❌"
                
                table.add_row(
                    name.replace("obs-stack-", ""),
                    f"[{status_color}]{status_icon} {status}[/{status_color}]",
                    ports
                )
        
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not check service status: {e}[/yellow]")