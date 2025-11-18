"""
Setup script for WhatsApp Invoice Tool.
Installs all dependencies and sets up the environment.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command and print status."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    try:
        subprocess.check_call(command, shell=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"  Error: {e}")
        return False


def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("  WhatsApp Invoice Tool - Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required!")
        print(f"  Current version: {sys.version}")
        return False
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Install Python dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        return False
    
    # Install Playwright browsers
    if not run_command(
        f"{sys.executable} -m playwright install chromium",
        "Installing Playwright Chromium browser"
    ):
        print("⚠ Warning: Playwright installation failed")
        print("  You may need to run: playwright install chromium")
    
    # Create necessary directories
    print("\n" + "="*60)
    print("  Creating directories")
    print("="*60)
    
    directories = [
        "logs",
        "invoices_output",
        "playwright_profile"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created: {directory}/")
    
    # Create sample Excel file
    print("\n" + "="*60)
    print("  Creating sample Excel file")
    print("="*60)
    
    try:
        exec(open("create_sample_excel.py").read())
    except Exception as e:
        print(f"⚠ Warning: Could not create sample Excel: {e}")
    
    # Check for wkhtmltopdf
    print("\n" + "="*60)
    print("  Checking wkhtmltopdf installation")
    print("="*60)
    
    try:
        subprocess.check_output("wkhtmltopdf --version", shell=True, stderr=subprocess.STDOUT)
        print("✓ wkhtmltopdf is installed")
    except:
        print("⚠ Warning: wkhtmltopdf not found!")
        print("  Please download and install from:")
        print("  https://wkhtmltopdf.org/downloads.html")
    
    # Final message
    print("\n" + "="*60)
    print("  Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Edit config.json with your company details")
    print("  2. Run the application: python app.py")
    print("  3. Or build executable: python build_spec.py")
    print("\n" + "="*60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
