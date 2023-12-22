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

        ## The button used to determine textbox or top of screen alignment.
        if config.developer and persistent.quick_menu_style and not in_nvl:
            use quick_menu_a

        ## Determine quick menu style to use
        if persistent.quick_menu_style and persistent.quick_menu_align:

            use quick_menu_b

        elif persistent.quick_menu_style and not persistent.quick_menu_align:

            use quick_menu_c

        elif not persistent.quick_menu_style:
            use quick_menu_ham


screen quick_menu_a():
    vbox:
        xalign 1.0
        yalign 0.26
        imagebutton:
            alt "Toggle quick menu position"
            hover "gui/button/switch_rotated.png"
            idle "gui/button/switch_rotated.png"
            action ToggleVariable("persistent.quick_menu_align", True, False)
            tooltip _("Quick menu")


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


screen quick_menu_c():
    ## Create a container for the quick menu content
    frame:

        xfill True
        ## Number not yet accurate
        ypos 1466
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


screen quick_menu_2():

    zorder 100

    frame:
        style_prefix "quick_menu"
        xalign 0.5
        yalign 0

        grid 4 2:
            xalign 0.5
            yalign 0.5
            spacing 5

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu ("navigation")
            textbutton _("History") action ShowMenu("history")
            textbutton _("Q.save") action QuickSave()
            textbutton _("Q.load") action QuickLoad()
            textbutton _("Settings") action ShowMenu("preferences")
    use quick_menu_ham


## Used in multiple places
screen quick_menu_ham():

    ## Ensure the quick menu button stays on top of the quick menu so it can be closed
    zorder 101

    vbox:
        xalign 1.0
        yalign 0.0
        imagebutton:
            alt "Open the quick menu"
            hover "gui/button/hamburger.png"
            idle "gui/button/hamburger.png"
            action ToggleScreen('quick_menu_2')
            tooltip _("Quick menu")


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
