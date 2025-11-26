import os
import subprocess


PUBLISHED_VERSION_FILE = ".published_version"   # stored in project root



# ------------------------------------------------------------
# run command helpers
# ------------------------------------------------------------
def get_command_output(*args):
    """Tries to execute a command and returns output as string. In case of failure None is returned."""
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except Exception as e:
        cmd_line = " ".join(args)
        print("Error when running '" + cmd_line + "':", str(e))
        return None

    # some commands print via rich, stderr may contain the real output
    output = result.stdout or result.stderr
    return output


def run_command(*args):
    """Tries to run a command."""
    try:
        subprocess.run(
            args,
            text=True,
            check=True,
        )
    except Exception as e:
        cmd_line = " ".join(args)
        print("Error when running '" + cmd_line + "':", str(e))


# ------------------------------------------------------------
# Hatch helpers
# ------------------------------------------------------------

def get_hatch_version():
    """Return the version from hatch version."""
    output = get_command_output("hatch", "version")
    if isinstance(output, str):
        return output.strip()
    return None


# ------------------------------------------------------------
# Git helpers
# ------------------------------------------------------------

def get_git_tag():
    """Return the latest git tag (e.g. `v1.2.3`) or None."""
    output = get_command_output("git", "describe", "--tags", "--abbrev=0")
    if isinstance(output, str):
        return output.strip()
    return None



# ------------------------------------------------------------
# File helpers
# ------------------------------------------------------------

def read_published_version():
    """Return the version stored by the publisher, or None."""
    if not os.path.isfile(PUBLISHED_VERSION_FILE):
        return None

    try:
        with open(PUBLISHED_VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def write_published_version(version: str):
    """Write version into the tracking file."""
    with open(PUBLISHED_VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(version.strip())
