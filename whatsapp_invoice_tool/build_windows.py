"""
Automated Windows Executable Builder
Run this on Windows to create WhatsAppInvoiceTool.exe

Usage:
    python build_windows.py

Output:
    dist/WhatsAppInvoiceTool.exe
"""
import sys
import subprocess
import os
import shutil
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and 8 <= version.minor <= 11:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor} not supported")
        print("  Please use Python 3.8-3.11")
        return False


def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed")
            return True
        except:
            print("✗ Failed to install PyInstaller")
            return False


def create_spec_file():
    """Create PyInstaller spec file."""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json', '.'),
        ('templates', 'templates'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'openpyxl',
        'openpyxl.utils',
        'openpyxl.styles',
        'jinja2',
        'jinja2.ext',
        'pdfkit',
        'playwright',
        'playwright.sync_api',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WhatsAppInvoiceTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    with open('WhatsAppInvoiceTool.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Spec file created")


def build_executable():
    """Build the executable using PyInstaller."""
    print("\nBuilding executable (this may take 3-5 minutes)...")
    print("Please wait...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "WhatsAppInvoiceTool.spec"
        ])
        print("\n✓ Executable built successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Build failed")
        return False


def create_distribution_package():
    """Create a distribution package with all necessary files."""
    print("\nCreating distribution package...")
    
    # Create distribution folder
    dist_pkg = Path("dist_package") / "WhatsAppInvoiceTool"
    if dist_pkg.exists():
        shutil.rmtree(dist_pkg)
    dist_pkg.mkdir(parents=True)
    
    # Copy executable
    exe_src = Path("dist") / "WhatsAppInvoiceTool.exe"
    if exe_src.exists():
        shutil.copy2(exe_src, dist_pkg / "WhatsAppInvoiceTool.exe")
        print("  ✓ Copied executable")
    else:
        print("  ✗ Executable not found")
        return False
    
    # Copy config
    if Path("config.json").exists():
        shutil.copy2("config.json", dist_pkg / "config.json")
        print("  ✓ Copied config.json")
    
    # Copy templates
    if Path("templates").exists():
        shutil.copytree("templates", dist_pkg / "templates")
        print("  ✓ Copied templates/")
    
    # Copy documentation
    for doc in ["README.md", "QUICKSTART.md", "sample_invoices.xlsx"]:
        if Path(doc).exists():
            shutil.copy2(doc, dist_pkg / doc)
            print(f"  ✓ Copied {doc}")
    
    print("\n✓ Distribution package created")
    return True


def main():
    """Main build process."""
    print_header("WhatsApp Invoice Tool - Windows Builder")
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check if we're on Windows
    if sys.platform != "win32":
        print("\n⚠ WARNING: You're not on Windows!")
        print("  This script should be run on Windows to create .exe files")
        print("  Continuing anyway, but may create Linux/Mac binaries instead")
        print()
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            return 1
    
    # Install PyInstaller
    print_header("Installing Dependencies")
    if not install_pyinstaller():
        return 1
    
    # Create spec file
    print_header("Creating Build Configuration")
    create_spec_file()
    
    # Build executable
    print_header("Building Executable")
    if not build_executable():
        return 1
    
    # Create distribution package
    print_header("Creating Distribution Package")
    if not create_distribution_package():
        return 1
    
    # Success message
    print_header("Build Complete!")
    print()
    print("Executable Location:")
    print(f"  {Path('dist').absolute() / 'WhatsAppInvoiceTool.exe'}")
    print()
    print("Distribution Package:")
    print(f"  {Path('dist_package').absolute() / 'WhatsAppInvoiceTool'}")
    print()
    print("Next Steps:")
    print("  1. Test the executable")
    print("  2. Copy distribution package to target machines")
    print("  3. Ensure wkhtmltopdf is installed on target machines")
    print()
    print("="*60)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
