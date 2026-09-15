on run
	set suggestedURL to ""
	try
		set clipboardText to the clipboard as text
		if clipboardText starts with "https://" or clipboardText starts with "http://" then
			set suggestedURL to clipboardText
		end if
	end try

	set dialogResult to display dialog "Paste a JioSaavn URL:" default answer suggestedURL buttons {"Cancel", "Download"} default button "Download" cancel button "Cancel" with title "JioLite"
	my downloadURL(text returned of dialogResult)
end run

on open droppedItems
	repeat with droppedItem in droppedItems
		set itemPath to POSIX path of droppedItem
		if itemPath ends with ".webloc" then
			set suppliedURL to do shell script "/usr/bin/plutil -extract URL raw -o - " & quoted form of itemPath
		else
			try
				set suppliedURL to read droppedItem as «class utf8»
			on error
				display alert "That item does not contain a readable URL." as critical
				return
			end try
		end if
		my downloadURL(suppliedURL)
	end repeat
end open

on open location incomingURL
	try
		set pythonExecutable to my getPythonExecutable()
		set decoderCode to "import sys; from urllib.parse import parse_qs, urlsplit; print(parse_qs(urlsplit(sys.argv[1]).query)['url'][0])"
		set suppliedURL to do shell script quoted form of pythonExecutable & " -c " & quoted form of decoderCode & " " & quoted form of incomingURL
		my downloadURL(suppliedURL)
	on error errorMessage number errorNumber
		display alert "JioLite could not read that download link." message ("Error " & errorNumber & ": " & errorMessage) as critical
	end try
end open location

on downloadURL(suppliedURL)
	set projectDirectory to my getProjectDirectory()
	set pythonExecutable to my getPythonExecutable()
	set downloadsDirectory to POSIX path of (path to downloads folder from user domain)
	set logFile to POSIX path of (path to library folder from user domain) & "Logs/JioLite.log"
	set cleanURL to my trimText(suppliedURL)
	if cleanURL does not start with "https://" and cleanURL does not start with "http://" then
		display alert "Please provide a complete web URL beginning with https:// or http://." as critical
		return
	end if

	display notification "The download is running." with title "JioLite"
	set startLine to "\n\n===== " & (current date as text) & " =====\nURL: " & cleanURL & "\n"
	do shell script "/usr/bin/printf %s " & quoted form of startLine & " >> " & quoted form of logFile

	set downloadCommand to "cd " & quoted form of projectDirectory & " && /usr/bin/caffeinate -i " & quoted form of pythonExecutable & " orpheus.py -o " & quoted form of downloadsDirectory & " " & quoted form of cleanURL & " >> " & quoted form of logFile & " 2>&1"
	try
		with timeout of 86400 seconds
			do shell script downloadCommand
		end timeout
		display notification "Download finished." with title "JioLite"
	on error errorMessage number errorNumber
		set logTail to ""
		try
			set logTail to do shell script "/usr/bin/tail -n 18 " & quoted form of logFile
		end try
		set errorDialog to display alert "JioLite could not complete the download." message (my shortenText(logTail & "\n\nError " & errorNumber & ": " & errorMessage, 3000)) as critical buttons {"Close", "Open Log"} default button "Open Log"
		if button returned of errorDialog is "Open Log" then
			do shell script "/usr/bin/open -t " & quoted form of logFile
		end if
	end try
end downloadURL

on trimText(valueToTrim)
	set whitespace to {space, tab, return, linefeed}
	set outputText to valueToTrim as text
	repeat while outputText is not "" and first character of outputText is in whitespace
		set outputText to text 2 thru -1 of outputText
	end repeat
	repeat while outputText is not "" and last character of outputText is in whitespace
		set outputText to text 1 thru -2 of outputText
	end repeat
	return outputText
end trimText

on shortenText(valueToShorten, maximumLength)
	if (length of valueToShorten) is less than or equal to maximumLength then return valueToShorten
	return "…" & text (-(maximumLength - 1)) thru -1 of valueToShorten
end shortenText

on getProjectDirectory()
	return POSIX path of (path to application support from user domain) & "JioLite/runtime"
end getProjectDirectory

on getPythonExecutable()
	return POSIX path of (path to application support from user domain) & "JioLite/venv/bin/python3"
end getPythonExecutable
