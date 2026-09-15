#!/usr/bin/env python3
"""Install the complete JioLite pipeline for the current macOS user."""

from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import venv


RESOURCE_DIRECTORY = Path(__file__).resolve().parent
PAYLOAD_DIRECTORY = RESOURCE_DIRECTORY / "payload"
if not PAYLOAD_DIRECTORY.is_dir():
    PAYLOAD_DIRECTORY = RESOURCE_DIRECTORY.parent / "payload"

USER_HOME = Path.home()
SUPPORT_DIRECTORY = USER_HOME / "Library" / "Application Support" / "JioLite"
RUNTIME_DIRECTORY = SUPPORT_DIRECTORY / "runtime"
VENV_DIRECTORY = SUPPORT_DIRECTORY / "venv"
APPLICATIONS_DIRECTORY = USER_HOME / "Applications"
JIOLITE_APPLICATION = APPLICATIONS_DIRECTORY / "JioLite.app"
USERSCRIPT_INSTALLER_APPLICATION = APPLICATIONS_DIRECTORY / "Install JioLite Userscript.app"

OSACOMPILE = Path("/usr/bin/osacompile")
CODESIGN = Path("/usr/bin/codesign")
PLIST_BUDDY = Path("/usr/libexec/PlistBuddy")
LAUNCH_SERVICES = Path(
    "/System/Library/Frameworks/CoreServices.framework/Frameworks/"
    "LaunchServices.framework/Support/lsregister"
)


def run(arguments: list[str | os.PathLike[str]], **kwargs) -> subprocess.CompletedProcess:
    printable = " ".join(str(argument) for argument in arguments)
    print(f"+ {printable}", flush=True)
    return subprocess.run([str(argument) for argument in arguments], check=True, **kwargs)


def set_plist_value(plist: Path, key: str, value_type: str, value: str) -> None:
    result = subprocess.run(
        [str(PLIST_BUDDY), "-c", f"Set :{key} {value}", str(plist)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode:
        run([PLIST_BUDDY, "-c", f"Add :{key} {value_type} {value}", plist])


def compile_apple_script(source: Path, destination: Path, bundle_identifier: str) -> None:
    run([OSACOMPILE, "-o", destination, source])
    info_plist = destination / "Contents" / "Info.plist"
    set_plist_value(info_plist, "CFBundleIdentifier", "string", bundle_identifier)


def configure_url_scheme(application: Path) -> None:
    info_plist = application / "Contents" / "Info.plist"
    subprocess.run(
        [str(PLIST_BUDDY), "-c", "Delete :CFBundleURLTypes", str(info_plist)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    commands = [
        "Add :CFBundleURLTypes array",
        "Add :CFBundleURLTypes:0 dict",
        "Add :CFBundleURLTypes:0:CFBundleURLName string JioLite Download Link",
        "Add :CFBundleURLTypes:0:CFBundleTypeRole string Viewer",
        "Add :CFBundleURLTypes:0:CFBundleURLSchemes array",
        "Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string jiolite",
    ]
    for command in commands:
        run([PLIST_BUDDY, "-c", command, info_plist])


def copy_runtime() -> None:
    payload_runtime = PAYLOAD_DIRECTORY / "runtime"
    if not (payload_runtime / "orpheus.py").is_file():
        raise RuntimeError(f"JioLite runtime payload is incomplete: {payload_runtime}")

    SUPPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        payload_runtime,
        RUNTIME_DIRECTORY,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("config", "__pycache__", "*.pyc", ".DS_Store"),
    )

    installed_config = RUNTIME_DIRECTORY / "config" / "settings.json"
    if not installed_config.exists():
        installed_config.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(payload_runtime / "config" / "settings.json", installed_config)


def create_environment() -> Path:
    print(f"Creating Python environment at {VENV_DIRECTORY}", flush=True)
    venv.EnvBuilder(with_pip=True).create(VENV_DIRECTORY)
    python_executable = VENV_DIRECTORY / "bin" / "python3"
    run(
        [
            python_executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--upgrade",
            "-r",
            RUNTIME_DIRECTORY / "requirements.txt",
        ]
    )
    return python_executable


def initialize_orpheus(python_executable: Path) -> None:
    run(
        [python_executable, "orpheus.py", "settings", "refresh"],
        cwd=RUNTIME_DIRECTORY,
    )


def build_applications() -> None:
    APPLICATIONS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    payload_app = PAYLOAD_DIRECTORY / "app"
    payload_userscript = PAYLOAD_DIRECTORY / "userscript"

    compile_apple_script(
        payload_app / "JioLite.applescript",
        JIOLITE_APPLICATION,
        "com.thompcha.JioLite",
    )
    configure_url_scheme(JIOLITE_APPLICATION)
    run([CODESIGN, "--force", "--deep", "--sign", "-", JIOLITE_APPLICATION])
    run([LAUNCH_SERVICES, "-f", JIOLITE_APPLICATION])

    compile_apple_script(
        payload_app / "Install JioLite Userscript.applescript",
        USERSCRIPT_INSTALLER_APPLICATION,
        "com.thompcha.JioLite.UserscriptInstaller",
    )
    resources = USERSCRIPT_INSTALLER_APPLICATION / "Contents" / "Resources"
    shutil.copy2(payload_userscript / "serve-installer.py", resources)
    shutil.copy2(payload_userscript / "JioLite.user.js", resources)
    run(
        [
            CODESIGN,
            "--force",
            "--deep",
            "--sign",
            "-",
            USERSCRIPT_INSTALLER_APPLICATION,
        ]
    )


def write_receipt() -> None:
    receipt = {
        "installed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "python": platform.python_version(),
        "architecture": platform.machine(),
        "runtime": str(RUNTIME_DIRECTORY),
    }
    (SUPPORT_DIRECTORY / "install-receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if sys.platform != "darwin":
        raise RuntimeError("JioLite currently supports macOS only.")
    if sys.version_info < (3, 9):
        raise RuntimeError("JioLite requires Python 3.9 or newer.")

    print(f"Installing JioLite from {PAYLOAD_DIRECTORY}", flush=True)
    copy_runtime()
    python_executable = create_environment()
    initialize_orpheus(python_executable)
    build_applications()
    write_receipt()
    print("JioLite installation completed successfully.", flush=True)


if __name__ == "__main__":
    main()
