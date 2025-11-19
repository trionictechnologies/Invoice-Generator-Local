"""
PyInstaller build script for WhatsApp Invoice Tool.
Creates a standalone Windows executable.

Usage:
    python build_spec.py
    or
    pyinstaller whatsapp_invoice_tool.spec
"""

from pathlib import Path

# PyInstaller spec file content
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
        'PySide6',
        'openpyxl',
        'jinja2',
        'pdfkit',
        'playwright',
        'playwright.sync_api',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one
)
"""

# Write spec file
spec_path = Path(__file__).parent / "whatsapp_invoice_tool.spec"
with open(spec_path, 'w', encoding='utf-8') as f:
    f.write(spec_content)

print(f"PyInstaller spec file created: {spec_path}")
print("\nTo build the executable, run:")
print("  pyinstaller whatsapp_invoice_tool.spec")
print("\nOr use:")
print("  pyinstaller --onefile --windowed --name WhatsAppInvoiceTool app.py")
