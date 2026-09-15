#!/bin/sh
set -eu

package_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
staging_directory=$(/usr/bin/mktemp -d "$package_root/.build.XXXXXX")
staged_application="$staging_directory/Install JioLite.app"
distribution_application="$package_root/Install JioLite.app"

cleanup() {
    /bin/rm -rf "$staging_directory"
}
trap cleanup EXIT INT TERM

/usr/bin/osacompile -o "$staged_application" "$package_root/installer/Install JioLite.applescript"
/bin/cp "$package_root/installer/install.py" "$staged_application/Contents/Resources/install.py"
/bin/cp -R "$package_root/payload" "$staged_application/Contents/Resources/payload"
/usr/libexec/PlistBuddy -c "Add :CFBundleIdentifier string com.thompcha.JioLite.BootstrapInstaller" "$staged_application/Contents/Info.plist"
/usr/bin/codesign --force --deep --sign - "$staged_application"

case "$distribution_application" in
    "$package_root/Install JioLite.app") ;;
    *) echo "Refusing to replace an unexpected path" >&2; exit 1 ;;
esac
/bin/rm -rf "$distribution_application"
/bin/mv "$staged_application" "$distribution_application"

echo "Built $distribution_application"
