on run
	set installerScript to POSIX path of (path to resource "install.py")
	set installerLog to POSIX path of (path to library folder from user domain) & "Logs/JioLite Installer.log"
	set userHome to POSIX path of (path to home folder from user domain)
	set pythonCandidates to {"/opt/homebrew/bin/python3", "/usr/local/bin/python3", userHome & ".pyenv/shims/python3", "/usr/bin/python3"}
	set pythonExecutable to ""

	repeat with candidate in pythonCandidates
		try
			do shell script "test -x " & quoted form of candidate
			set pythonExecutable to candidate as text
			exit repeat
		end try
	end repeat

	if pythonExecutable is "" then
		set pythonDialog to display alert "Python 3 is required to install JioLite." message "Install Python 3 for macOS, then run this installer again." buttons {"Cancel", "Get Python"} default button "Get Python" cancel button "Cancel"
		if button returned of pythonDialog is "Get Python" then
			do shell script "/usr/bin/open https://www.python.org/downloads/macos/"
		end if
		return
	end if

	display notification "Setting up JioLite and its private Python environment…" with title "JioLite Installer"
	set installCommand to quoted form of pythonExecutable & " " & quoted form of installerScript & " > " & quoted form of installerLog & " 2>&1"
	try
		with timeout of 3600 seconds
			do shell script installCommand
		end timeout
		display notification "JioLite is installed. Approve the userscript in Violentmonkey." with title "JioLite Installer"
		set userscriptInstaller to POSIX path of (path to applications folder from user domain) & "Install JioLite Userscript.app"
		do shell script "/usr/bin/open " & quoted form of userscriptInstaller
	on error errorMessage number errorNumber
		set logTail to ""
		try
			set logTail to do shell script "/usr/bin/tail -n 30 " & quoted form of installerLog
		end try
		set errorDialog to display alert "JioLite could not be installed." message (logTail & "\n\nError " & errorNumber & ": " & errorMessage) as critical buttons {"Close", "Open Log"} default button "Open Log"
		if button returned of errorDialog is "Open Log" then
			do shell script "/usr/bin/open -t " & quoted form of installerLog
		end if
	end try
end run
