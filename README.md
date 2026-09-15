# JioLite

JioLite is a macOS front end for downloading JioSaavn tracks through a button
added to JioSaavn song rows by a Violentmonkey userscript. Downloads are saved
to the current user's `~/Downloads` folder with tags and embedded cover art.

## Install on another Mac

1. Sync or download this entire folder.
2. Ensure Python 3.9 or newer and Violentmonkey are installed.
3. Open `Install JioLite.app` (right-click and choose **Open** if macOS asks).
4. When Firefox opens Violentmonkey, approve the JioLite userscript.
5. Reload JioSaavn. Use the green arrow on any song row to download it.

The installer creates a private environment under
`~/Library/Application Support/JioLite`, installs `JioLite.app` and the
userscript installer under `~/Applications`, and registers the private
`jiolite://` browser handoff. No Terminal commands are needed by the end user.

## Update the distributable installer

After changing anything under `payload/` or `installer/`, run:

```sh
./build-distribution.sh
```

Commit both the source files and the rebuilt `Install JioLite.app` bundle.

## Data and privacy

The repository contains no downloads, browser data, cookies, login storage,
logs, or virtual environment. The local installer server binds only to
`127.0.0.1` on a random port and shuts down automatically.

See [NOTICE.md](NOTICE.md) for upstream source attribution and redistribution
notes.
