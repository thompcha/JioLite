# JioLite

JioLite adds a green download arrow to song rows on JioSaavn. Click the arrow
and the track is downloaded to your Mac's **Downloads** folder with its title,
artist, album, date, and cover art embedded.

JioLite is for **macOS only**. Use it only for media you are allowed to
download.

## What you need

Before installing JioLite, install:

1. [Python 3 for macOS](https://www.python.org/downloads/macos/) — version 3.9
   or newer.
2. [Violentmonkey for Firefox](https://addons.mozilla.org/en-US/firefox/addon/violentmonkey/),
   or Violentmonkey for the Chromium-based browser you use.

The JioLite installer will tell you if it cannot find Python.

## Easiest installation — no Terminal required

1. Open the [JioLite GitHub page](https://github.com/thompcha/JioLite).
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Open your Mac's **Downloads** folder.
5. Double-click the downloaded ZIP file to unpack it.
6. Open the new `JioLite-main` folder.
7. Right-click **Install JioLite.app** and choose **Open**. Do not double-click
   it on the first launch.
8. If macOS says it cannot verify that JioLite is free of malicious software,
   click **Done**, then follow [If macOS blocks the installer](#if-macos-blocks-the-installer)
   below.
9. Wait while JioLite creates its private Python environment and installs its
   dependencies. This can take a few minutes on the first run.
10. Your browser will open Violentmonkey's installation page. Click
    **Install** or **Confirm installation**.
11. Open or reload [JioSaavn](https://www.jiosaavn.com/).

You should now see a green download arrow on each song row.

## Installation with Git

Open **Terminal**, paste this entire command, and press Return:

```sh
git clone https://github.com/thompcha/JioLite.git "$HOME/Downloads/JioLite" && open "$HOME/Downloads/JioLite/Install JioLite.app"
```

If macOS blocks the installer, open `~/Downloads/JioLite` in Finder,
right-click **Install JioLite.app**, and choose **Open**.

## Downloading a track

1. Visit a JioSaavn album, playlist, chart, or other page containing song rows.
2. Click the green download arrow beside a song.
3. The first time, your browser may ask for permission to open JioLite. Approve
   it. Enable **Always allow** if your browser offers that choice.
4. JioLite runs without opening Terminal and displays a notification when the
   download finishes.
5. Find the finished `.m4a` file in your Mac's **Downloads** folder.

The userscript also hides the cookie notice, trial banner, and `Pro Only`
labels, and restores song rows to full brightness.

## Updating JioLite

If you installed with Git, open Terminal and run:

```sh
cd "$HOME/Downloads/JioLite" && git pull && open "Install JioLite.app"
```

Then approve the userscript update when Violentmonkey opens.

If you used **Download ZIP**, download a fresh ZIP from GitHub and run its
**Install JioLite.app** again. Reinstalling preserves your existing JioLite
configuration.

## Troubleshooting

### If macOS blocks the installer

JioLite is currently ad-hoc signed rather than notarized with a paid Apple
Developer ID. macOS therefore treats the app from a browser-downloaded ZIP as
unverified. You have two options.

#### Option 1: Approve it in System Settings

1. Try to open **Install JioLite.app** once and dismiss the warning.
2. Open **System Settings**.
3. Select **Privacy & Security**.
4. Scroll down to the **Security** section.
5. Find the message about **Install JioLite.app** and click **Open Anyway**.
6. Enter your Mac password or use Touch ID if requested.
7. Click **Open** in the final confirmation.

The **Open Anyway** button only appears for about an hour after an attempted
launch. See Apple's guide to
[safely opening Mac apps](https://support.apple.com/en-us/102445) for the
official instructions.

#### Option 2: Use one exact Terminal command

If you used GitHub's **Download ZIP** button, open Terminal, paste this entire
command, and press Return:

```sh
xattr -dr com.apple.quarantine "$HOME/Downloads/JioLite-main/Install JioLite.app" && open "$HOME/Downloads/JioLite-main/Install JioLite.app"
```

This removes the browser's quarantine marker only from the JioLite installer,
then opens it. Review this public repository's source before running the
command if you have any concerns.

The `git clone` installation command above normally avoids this specific issue
because Git does not add the browser-download quarantine marker.

### There is no green download arrow

- Confirm that Violentmonkey is installed and enabled in the browser currently
  showing JioSaavn.
- Open the Violentmonkey dashboard and confirm that **JioLite for JioSaavn** is
  enabled.
- Reload the JioSaavn tab.
- If the userscript is missing, open
  `~/Applications/Install JioLite Userscript.app` and approve it again.

### Clicking the arrow does nothing

- Approve the browser prompt asking to open JioLite.
- Confirm that `JioLite.app` exists in your personal Applications folder:
  `~/Applications`.
- Run **Install JioLite.app** again to repair the app and its `jiolite://` link
  registration.

### A download fails

Open this log file in Finder using **Go → Go to Folder**:

```text
~/Library/Logs/JioLite.log
```

The installation log is located at:

```text
~/Library/Logs/JioLite Installer.log
```

## What the installer changes

JioLite keeps its files within your user account:

- Runtime and private Python environment:
  `~/Library/Application Support/JioLite`
- Download application: `~/Applications/JioLite.app`
- Userscript installer: `~/Applications/Install JioLite Userscript.app`
- Downloaded tracks: `~/Downloads`

It does not install browser cookies, credentials, login sessions, or a
system-wide background service.

## Developer notes

After changing anything under `payload/` or `installer/`, rebuild the
distributable installer with:

```sh
./build-distribution.sh
```

Commit both the source files and the rebuilt `Install JioLite.app` bundle.

See [NOTICE.md](NOTICE.md) for upstream source attribution and redistribution
notes.
