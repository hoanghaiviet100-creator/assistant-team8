import sys
import subprocess
import os

def check_python():
    v = sys.version_info
    if v.major >= 3 and v.minor >= 10:
        print(f"[OK] Python >= 3.10 (found {v.major}.{v.minor}.{v.micro})")
        return True
    else:
        print(f"[FAIL] Python >= 3.10 required (found {v.major}.{v.minor}.{v.micro})")
        return False

def check_venv():
    in_venv = (hasattr(sys, 'real_prefix') or 
               (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    if in_venv:
        print("[OK] running inside a virtual environment")
        return True
    else:
        print("[FAIL] not running inside a virtual environment")
        return False

def check_package(pkg_name):
    try:
        __import__(pkg_name)
        print(f"[OK] {pkg_name} installed")
        return True
    except ImportError:
        print(f"[FAIL] {pkg_name} not installed")
        return False

def check_git():
    try:
        res = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        print(f"[OK] git available ({res.stdout.strip()})")
        
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, check=True)
        print("[OK] inside a git repository")
        
        email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
        if email:
            print(f"[OK] git user.email set ({email})")
        else:
            print("[FAIL] git user.email not set")
            
        if os.path.exists(".gitignore"):
            print("[OK] .gitignore present")
        else:
            print("[FAIL] .gitignore present")
            
        return True
    except Exception:
        print("[FAIL] git is not available or not in a git repository")
        return False

def check_readme():
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
            if "TODO" in content:
                print("[FAIL] README has no TODO left")
                return False
            else:
                print("[OK] README has no TODO left")
                return True
    else:
        print("[FAIL] README.md not found")
        return False

def check_assistant():
    try:
        from assistant.rules import reply
        ans = reply("help")
        if ans:
            print("[OK] starter app imports and answers")
            return True
        else:
            print("[FAIL] starter app did not return an answer")
            return False
    except Exception:
        print("[FAIL] starter app imports and answers")
        return False

def main():
    print("Checking environment...")
    ok = True
    ok &= check_python()
    ok &= check_venv()
    ok &= check_package("pytest")
    ok &= check_git()
    ok &= check_readme()
    ok &= check_assistant()
    
    if ok:
        print("\nAll checks passed successfully!")
    else:
        print("\nSome checks failed. Please fix them above.")

if __name__ == "__main__":
    main()