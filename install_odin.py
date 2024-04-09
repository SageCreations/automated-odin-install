import os
import platform
import subprocess

# Global variables
ODIN_REPO_URL = "https://github.com/odin-lang/Odin"
ODIN_DIR = "./Odin"
LLVM_VERSION = "llvm@14"
XCODE_COMMAND_LINE_TOOLS_CHECK = ["xcode-select", "-p"]
XCODE_COMMAND_LINE_TOOLS_INSTALL = ["xcode-select", "--install"]
BREW_INSTALL_LLVM_COMMAND = [f"brew install {LLVM_VERSION}"]


# has debugging now
def run_command(command, workdir=".", shell=False, check=True):
    if shell:
        command = ' '.join(command)
    try:
        completed_process = subprocess.run(command, cwd=workdir, shell=shell, check=True, text=True, capture_output=True)
        print(f"Output: {completed_process.stdout}")
        if completed_process.stderr:
            print(f"Error: {completed_process.stderr}")
        print(f"Executed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        if check:
            raise


# Finished
def clone_odin_repository():
    if not os.path.exists(ODIN_DIR):
        git_clone_command = ["git", "clone", ODIN_REPO_URL]
        run_command(git_clone_command)
    else:
        print(f"A directory named '{ODIN_DIR}' was found.")


# TODO: havent tested
def setup_windows():
    os.chdir(ODIN_DIR)
    run_command(["build.bat"])


# Finished
def setup_macos():
    try:
        run_command(XCODE_COMMAND_LINE_TOOLS_CHECK)
        print("Xcode Command Line Tools are already installed.")
    except subprocess.CalledProcessError:
        run_command(XCODE_COMMAND_LINE_TOOLS_INSTALL, shell=True, check=False)

    if not subprocess.check_output(["brew", "list", "--formula", LLVM_VERSION]):
        run_command(BREW_INSTALL_LLVM_COMMAND, shell=True)
    else:
        print(f"{LLVM_VERSION} is already installed.")

    with open(os.path.expanduser("~/.zshrc"), "a") as f:
        f.write(f'\nexport PATH="/usr/local/opt/{LLVM_VERSION}/bin:$PATH"')
    print(f"Added {LLVM_VERSION} to PATH in ~/.zshrc.")

    os.chdir(ODIN_DIR)
    run_command(["make"])

    print("Please run 'source ~/.zshrc' or restart your terminal to update PATH in the current terminal session.")


# TODO: havent tested
def setup_linux():
    run_command(["sudo", "apt-get", "install", "-y", "clang", LLVM_VERSION], shell=True)
    os.chdir(ODIN_DIR)
    run_command(["make"])



def main():
    os_type = platform.system()
    clone_odin_repository()

    if os_type == "Windows":
        setup_windows()
    elif os_type == "Darwin":
        setup_macos()
    elif os_type == "Linux":
        setup_linux()
    else:
        print(f"Unsupported OS: {os_type}")

if __name__ == "__main__":
    main()
