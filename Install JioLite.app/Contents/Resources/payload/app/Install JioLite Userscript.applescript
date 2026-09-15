on run
	set pythonExecutable to POSIX path of (path to application support from user domain) & "JioLite/venv/bin/python3"
	set installerScript to POSIX path of (path to resource "serve-installer.py")
	set installerLog to POSIX path of (path to library folder from user domain) & "Logs/JioLite Userscript Installer.log"
	set installCommand to "/usr/bin/nohup " & quoted form of pythonExecutable & " " & quoted form of installerScript & " > " & quoted form of installerLog & " 2>&1 < /dev/null &"
	try
		do shell script installCommand
		display notification "Approve the userscript on the Violentmonkey page in Firefox." with title "JioLite Installer"
	on error errorMessage number errorNumber
		display alert "Could not open the JioLite userscript installer." message ("Error " & errorNumber & ": " & errorMessage) as critical
	end try
end run
