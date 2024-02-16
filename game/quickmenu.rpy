## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

## We need a variable to control the quick menu when in NVL mode
default in_nvl = False
default quick_menu = True


init python:
    def force_autosave_blocking_and_restart():
        renpy.force_autosave(False, True)
        renpy.full_restart()

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
        background "#000C"
        ysize 115
        xfill True
        modal True # dont allow click through
        ## Align the quick menu to the top of the screen
        ypos 0
        has hbox
        style_prefix "touch_quick"

        xalign 0.5
        yalign 0.5
        spacing 32

        textbutton _("Back") action Rollback()
        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Menu") action [force_autosave_blocking_and_restart]
        textbutton _("Hide") action HideInterface()   


style touch_quick_button is default
style touch_quick_button_text is button_text

style touch_quick_button:
    properties gui.button_properties("touch_quick_button")
    yfill True

style touch_quick_button_text:
    properties gui.button_text_properties("touch_quick_button")
    selected_color "#5fb9ff"
