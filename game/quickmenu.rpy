## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

## We need a variable to control the quick menu when in NVL mode
default in_nvl = False
default quick_menu = True


screen quick_menu():

    ## Ensure the quick menu appears above other screens
    zorder 100

    ## Only show if the quick menu is allowed
    if quick_menu:

        ## Determine quick menu style to use
        if persistent.quick_menu_style and persistent.quick_menu_align:
            use quick_menu_b


screen quick_menu_b():
    ## Create a container for the quick menu content
    frame:

        xfill True
        ## Align the quick menu to the top of the screen
        ypos 0
        has hbox
        style_prefix "touch_quick"

        xalign 0.5
        yalign 0.8
        spacing 35

        textbutton _("Back") action Rollback()
        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Menu") action ShowMenu('navigation')


style quick_menu_frame:
    xfill True
    ysize 150

    background Frame("gui/overlay/menu_top.png", gui.frame_borders, tile=gui.frame_tile)
    padding gui.frame_borders.padding

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


style touch_quick_button is default
style touch_quick_button_text is button_text

style touch_quick_button:
    properties gui.button_properties("touch_quick_button")

style touch_quick_button_text:
    properties gui.button_text_properties("touch_quick_button")
    selected_color "#5fb9ff"
