import subprocess
import sys

def install(package):
    print(f"--- Installing {package} ---")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", package])
        print(f"SUCCESS: {package} installed.")
    except Exception as e:
        print(f"FAILED: {package}. Error: {e}")

if __name__ == "__main__":
    # We install dependencies one by one to see exactly where it fails
    packages = [
        'reportlab==3.6.12', 
        'html5lib', 
        'Pillow', 
        'xhtml2pdf'
    ]
    
    for pkg in packages:
        install(pkg)