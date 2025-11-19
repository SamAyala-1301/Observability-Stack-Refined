"""Main CLI entry point - ENHANCED."""
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.detector.framework_detector import FrameworkDetector
from core.detector.framework_db import get_all_frameworks
from cli.commands.detect_all import detect_all_command
from cli.commands.validate import validate_command
from cli.commands.instrument import instrument_command
from cli.commands.instrument_all import instrument_all_command
from cli.commands.status import status_command

console = Console()

@click.group()
@click.version_option(version="3.0.0-alpha", prog_name="obs-stack")
def cli():
    """
    🚀 ObsStack V3 - Instant Observability for Any App
    
    Auto-detect frameworks and add monitoring with zero code changes.
    """
    pass

@cli.command()
def version():
    """Show version information."""
    console.print("\n[bold blue]ObsStack v3.0.0-alpha[/bold blue]")
    console.print("Auto-detection and instrumentation system")
    console.print("\n[dim]Status: MS1 Complete - Detection + Instrumentation ✅[/dim]\n")

@cli.command()
@click.argument('container')
def detect(container):
    """
    Detect framework in a specific container.
    
    CONTAINER: Container ID or name
    
    Example: obs-stack detect flask-app
    """
    console.print(f"\n🔍 Detecting framework in: [cyan]{container}[/cyan]\n")
    
    try:
        detector = FrameworkDetector()
        result = detector.detect(container)
        
        # Create results table
        table = Table(title="Detection Results", show_header=True)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Container ID", result.container_id[:12])
        table.add_row("Container Name", result.container_name)
        table.add_row("Framework", result.framework.value)
        table.add_row("Language", result.language.value)
        if result.version:
            table.add_row("Version", result.version)
        table.add_row("Confidence", f"{result.confidence:.2%}")
        
        console.print(table)
        
        # Confidence indicator
        if result.is_confident():
            console.print(f"\n[bold green]✓[/bold green] High confidence detection")
        else:
            console.print(f"\n[bold yellow]⚠[/bold yellow] Low confidence - run 'obs-stack validate {container}' for details")
        
    except ValueError as e:
        console.print(f"[bold red]✗ Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}")
        sys.exit(1)

@cli.command(name='detect-all')
def detect_all():
    """Scan and detect frameworks in all running containers."""
    detect_all_command()

@cli.command()
@click.argument('container')
def validate(container):
    """
    Validate detection with detailed breakdown.
    
    CONTAINER: Container ID or name
    
    Shows which detectors contributed to the result.
    """
    validate_command(container)

@cli.command(name='list-frameworks')
def list_frameworks():
    """List all supported frameworks."""
    frameworks = get_all_frameworks()
    
    console.print("\n📚 [bold]Supported Frameworks:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Framework", style="cyan", width=15)
    table.add_column("Language", style="blue", width=10)
    table.add_column("Description", style="white")
    
    for sig in frameworks:
        table.add_row(
            sig.display_name,
            sig.language.value,
            sig.description
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {len(frameworks)} frameworks[/dim]\n")

@cli.command()
def list_indicators():
    """Show all detection indicators."""
    detector = FrameworkDetector()
    indicators = detector.get_indicators()
    
    console.print("\n[bold]🔍 Detection Indicators:[/bold]\n")
    
    for category, data in indicators.items():
        console.print(f"[cyan]{category.replace('_', ' ').title()}:[/cyan]")
        rprint(f"  {data}\n")

@cli.command()
@click.argument('container')
def instrument(container):
    """
    Instrument a container with OpenTelemetry.
    
    CONTAINER: Container ID or name
    
    Adds observability to detected framework automatically.
    """
    instrument_command(container)

@cli.command(name='instrument-all')
def instrument_all():
    """Instrument all running containers."""
    instrument_all_command()

@cli.command()
@click.argument('container', required=False)
def status(container):
    """
    Check instrumentation status.
    
    CONTAINER: Optional container ID or name. If omitted, checks all.
    
    Example: obs-stack status flask-app
    """
    status_command(container)

if __name__ == '__main__':
    cli()