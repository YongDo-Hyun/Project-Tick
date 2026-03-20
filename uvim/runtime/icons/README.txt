Choose your preferred icon and replace the standard uVim icon with it.
[This is for the Amiga]

When started from Workbench, uVim opens a window of standard terminal size
(80 x 25). Trying to change this by adding a tool type results in a window
that disappears before uVim comes up in its own window.
If you want uVim to start with another size, it can be done using
IconX.

Follow these steps:

1. Create a script file called e.g. uVim.WB, with a single line in which the
   uVim executable is started:
      Echo "uVim" > uVim.WB
      Protect uVim.WB +s

2. Rename the uVim icon to uVim.WB.

3. By default, the uVim icon is a program icon.
   Change the icon type from "program" to "project" using IconEdit from the
   "Tools" directory.

4. Change the icon settings using "information" from the WorkBench's "icon"
   menu:
   - The default program, of course, is "IconX".
   - A stack size of 4096 should be sufficient.
   - Create a WINDOW tooltype of the desired size.
     The appropriate values depend on your WB font.

   Example:
   On a standard non-interlaced WB screen with full overscan resolution
   (724 x 283 ), the WINDOW tooltype "CON:30/10/664/273" results in a
   horizontally centered window with 80 columns and 32 lines.

Now uVim comes up with the new window size.
