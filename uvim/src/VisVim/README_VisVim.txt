===============================
Visual Studio - uVim Integration
===============================

Copyright (C) 1997 Heiko Erhardt

VisVim is a Visual Studio Add-In that allows uVim to be integrated
as the default text editor. It will be used instead of the Visual
Studio built-in editor when you double-click on a file or press F4
after compiling (it will go to the proper line in the uVim buffer).
The file can be loaded exclusively by uVim or additionally to the
builtin Visual Studio editor (this option can be set in the VisVim
configuration dialog inside Visual Studio).
uVim does not replace the Visual Studio editor, it still runs in its
own window.

VisVim is based upon VisEmacs by Christopher Payne
(Copyright (C) Christopher Payne 1997).

Author: Heiko Erhardt <heiko.erhardt@gmx.net>
Based upon: VisEmacs by Christopher Payne <payneca@sagian.com>
Version: 1.0
Created: 23 Oct 1997
Date: 23 Oct 1997

VisVim was originally GNU GPL licensed, as stated below.  On March 21 2012
Heiko Erhardt declared this work to be relicensed under the uVim license, as
stated in ../../runtime/doc/license.txt (or ":help uganda" in uVim).

VisVim is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

VisVim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.


Requirements
------------

VisVim works with the *OLE-enabled* version of uVim version 5.0 and higher
only!!!  You must download the extra archive containing the OLE-enabled
executable from your uVim download site.  When building your own uVim
executable, use the if_ole_vc.mak makefile (uVim 5.1 and higher).
VisVim needs DevStudio 5.0 or higher. It does not work with DevStudio 4.2.


Installation
------------

1) Close running instances of DevStudio.

2) Copy VisVim.dll into a convenient directory like \vim,
   \vim\lib, or \vim\addin

3) Register the DLL using regsvr32.exe ...  (Skip this on Windows 95/98)
   Example:
   > cd \vim\addin
   > regsvr32 VisVim.dll
   On NT, you should do this from an administrator account.
   Before installing a new version of VisVim you should unregister
   the old one using
   > regsvr32 -unregister VisVim.dll
   The batch files register.bat and unregister.bat can do that for you.

3a) If you didn't do this yet: Register the OLE gvim:
   > gvim -register

4) Start Visual Studio and go to:
      Tools
	 Customize...
	    Add-Ins and Macro Files

5) Click on Browse, and point Visual Studio to your VisVim.dll file.

6) Click the checkbox to indicate that you want to use the Add-In, and
   Close the Customize dialog box.

7) You should notice the VisVim Toolbar with the uVim Icon.
   Click the first item of the toolbar to get to the options dialog.


Compiling VisVim
----------------

Two Options:

1) Load the VisVim.mak file as a Workspace in Visual Studio and compile

2) Use the MSVC command line compiler:
	vcvars32
	nmake -f VisVim.mak


Using VisVim
------------

The VisVim DLL exposes several functions to the user. These functions are
accessible using the toolbar or by assigning hotkeys to them (see below).
The following functions are visible on the toolbar (from left to right):

1. VisVim settings dialog
   The settings you adjust here will be saved in the registry and
   will be reloaded on program startup.

2. Enable uVim
   Enables uVim as Visual Studio editor. Control will be switched to uVim when:
   - Clicking a file in the file view
   - Clicking a compiler error message line
   - Using the 'File-Open' Dialog
   - Showing the current source line when encountering a debugger breakpoint.
   - Using File-New

3. Disable uVim
   The internal Visual Studio editor will be used to edit files.

4. Toggle enable state
   Toggles the enable state of VisVim. Use this function if you want to have
   one button only to activate/deactivate uVim.

5. Load current file in uVim
   Loads the file shown in the internal editor into uVim. Use this function if
   you want the internal editor to stay active and just edit one file in uVim.
   This command works always whether uVim is enabled as default editor or not.

You cannot use DevStudio's debugger commands from inside uVim, so you should
disable uVim before running the debugger.

You can customize the uVim toolbar itself or add the uVim buttons to other
toolbars.
To have fast access to the VisVim options dialog I suggest to create keyboard
shortcuts:

1) Choose
      Tools
	 Customize...
	    Keyboard
2) Choose Category:AddIns and Commands:VisVim.
3) Choose 'Main' as editor, enter each hotkey and press the Assign button.
   I suggest:
       VisVimDialogCmd    Alt+Shift+V
       VisVimEnableCmd    Alt+Shift+E
       VisVimDisableCmd   Alt+Shift+D
       VisVimToggleCmd    Alt+Shift+T
       VisVimLoadCmd      Alt+Shift+G
4) Close the dialog

Now a typical debugging example:

Using "Alt+Shift+d" you turn off uVim before starting the debugger.
After hitting the breakpoint you single step through your application
using the internal source code editor and examine variables.
When you stumble across the line with the null pointer
assignment, just press "Alt+Shift+g", and correct the error in uVim.
Save the file, press Alt+Tab to return to DevStudio and press F7 to compile.
That's it.


Troubleshooting
---------------

1. When opening a file in DevStudio the file is opened in the DevStudio
   editor and immediately vanishes. No uVim shows up.
   Cause:       Probably you don't have the OLE-enabled uVim or you didn't
		register it.
   Explanation: VisVim is notified by DevStudio if an 'open document' event
		occurs. It then closes the document in the internal editor
		and tries to start uVim. If uVim isn't properly OLE-registered,
		this won't work.
   Workaround:  Download and install the OLE-enable version of uVim and
		execute "gvim -register".

2. Sometimes when clicking on a file, the file won't be opened by uVim but
   instead the Visual Studio editor comes up.
   Cause:       The file was already loaded by the DevStudio editor.
   Explanation: VisVim works by hooks exposed by Visual Studio.
		Most of the functionality works from the OpenDocument hook.
		If a document is already loaded in the Visual Studio editor,
		no 'open document' event will be generated when clicking the
		file in the file list.
   Workaround:  Close the document in Visual Studio first.

3. I can't get VisVim to work. Either the uVim toolbar does not appear at all
   or weird crashes happen.
   Cause:       The Visual Studio installation is messed up.
   Explanation: I can't give you one. Ask M$.
   Workaround:  Reinstall DevStudio (I know this is brute, but in some cases
		it helped). There was one case where the service pack 1 had
		to be installed, too.

4. If an instance of uVim is already running, VisVim will use that instance
   and not start a new one.
   Cause:	 This is proper OLE behaviour
   Explanation:  Some call it a bug, some a feature. That's just the way OLE
		 works.

5. When being in insert mode in uVim and selecting a file in Visual Studio,
   the uVim command :e ... is inserted as text instead of being executed.
   Cause:	 You probably know...
   Explanation:  The uVim OLE automation interface interprets the VisVim
		 commands as if they were typed in by the user.
		 So if you're in insert mode uVim considers it to be text.
		 I decided against sending an ESC before the command because
		 it may cause a beep or at least a screen flash when noeb is
		 set.
   Workaround:	 Get used to press ESC before switching to DevStudio.

6. I'm tired of VisVim but I can't get rid of it. I can't delete it in
   Tools-Customize-Add-Ins.
   Cause:	 You can't delete an item you once added to the add-ins
		 list box.
   Explanation:  M$ just didn't put a 'delete' button in the dialog box.
		 Unfortunately there is no DEL key accellerator as well...
   Workaround:	 You can't kill it, but you can knock it out:
		 1. Uncheck the check box in front of 'uVim Developer Studio
		    Add-in'.
		 2. Close Visual Studio.
		 3. Delete VisVim.dll or move it somewhere it can't be found.
		 4. Run Visual Studio.
		 5. Tools -> Customize ->Add-ins and Macro-Files.
		 6. A message appears:
		    ".../VisVim.dll" "This add-in no longer exists.  It will
		    no longer be displayed."
		 That's it!


Change history
--------------

1.0a to 1.0
-----------

- All settings in the VisVim dialog are remembered between DevStudio sessions
  by keeping them in the registry (HKEY_CURRENT_USER\Software\uVim\VisVim).
- Added an option to do a :cd before opening the file (having a file opened
  by clicking it but finding out to be still in C:\Windows\system when trying to
  open another file by ":e" can be annoying). Change directory can be
  done to the source file's directory or it's parent directory.
- Added some explanations to the error message for the CO_E_CLASSSTRING error
  ("Use OLE uVim and make sure to register...").

1.0 to 1.1a
-----------

- The VisVim toolbar button now shows the new uVim icon instead of the old one.
- Made some changes to the documentation, added the troubleshooting chapter
  and ToDo list.
- File-New-* now invokes uVim instead of the builtin editor if enabled.

1.1 to 1.1b
-----------

- Extended the VisVim toolbar to have multiple buttons instead of one.
- Moved the enable/disable commands from the settings dialog to the toolbar.
- Added the toggle enable/disable command
- Added the 'load current file' command.

1.1b to 1.2
-----------

No new features, just some fine tuning:

- Changed the GUID of the VisVim OLE interface to avoid conflicts with a
  version of VisEmacs or VisVile on the same computer (Guy Gascoigne)
- Fixed a bug caused by a bug in the Developer Studio add-in code generator
  (Clark Morgan)
- Fixed a memory leak (Clark Morgan)
- Added an option in the VisVim dialog to prepend ESC before the first command
  that is sent to uVim. This will avoid inserting the command as text when uVim
  is still in insert mode.
- An :update command is sent to uVim before any other command to update the
  current file if it is modified, or else the following :cd or :e command will fail.

1.2 to 1.3a
-----------

- Fixed a bug caused by a missing EnableModeless() function call in VimLoad().
  This seems to reduce VisVim crashing DevStudio on some systems (it
  occasionally still seems to happen, but it's more stable now).
  (Vince Negri)
- Added support for the new CTRL-\ CTRL-N command of uVim 5.4a.
  This prevents uVim from beeping when a VisVim command is executed and uVim is
  not in insert mode.


ToDo List
---------

P1 is highest priority, P10 lowest

P9  Switching to DevStudio using ALT-TAB may get annoying. Would be nice to
    have the option to map ActivateApplication("Visual Studio") in uVim.
    uVim DLLs would solve that problem.

P8  Execute :tag command in uVim for word under cursor in DevStudio

P7  Controlling the Visual Studio Debugger from inside uVim
    See message above. Also a 'Debug' highlight group and a
    command to highlight a certain line would be necessary.

P6  Provide an option to open the current file in VisVim in
    Visual Studio editor
    Same as above message. A kind of two way OLE automation would have to be
    established between VisVim and uVim. Also a 'Debug' highlight group and a
    command to highlight a certain line would be necessary.


Known Problems
--------------

- Occasional memory corruptions in DevStudio may appear on some systems.
  Reinstalling DevStudio helped in some cases.
  The cause of these crashes is unclear; there is no way to debug this.
  Recompiling VisVim with DevStudio SP3 didn't help.
  I assume it's a problem deep inside the DevStudio add-in OLE interfaces.
  This will hopefully be fixed with DevStudio 6.


Have fun!

Heiko Erhardt
heiko.erhardt@gmx.net
