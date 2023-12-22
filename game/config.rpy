default persistent.men_style = True
default persistent.navigation_return_button_style = True
default persistent.navigation_menu_content_style = True
default persistent.quick_menu_style = True
default persistent.quick_menu_align = True


## Disable the gallery while it is not ready
default persistent.gal_screen = False

screen configs():
    tag menu

    ## Make the background black
    add "black"

    ## Generate the viewport to hold everything
    side "c":
        area (20, 20, 1040, 1880)

        viewport id "configuration_viewport":
            draggable True
            scrollbars None

            ## RTFM (This is intended to be humorous)
            vbox:
                text ("""This GUI is configurable while config.developer is True
Play through the demo and adjust the GUI with the provided tools, then check this screen.
Edit config.rpy to match the values here, to use the GUI as it appears.
Delete persistent data before building a distribution.""")

                null height 5
                ## Used as a content divider
                bar ysize 5 xsize 1040

                ## The values
                text "persistent.men_style"
                text "%s" %persistent.men_style

                text "persistent.navigation_return_button_style"
                text "%s" %persistent.navigation_return_button_style

                text "persistent.navigation_menu_content_style"
                text "%s" %persistent.navigation_menu_content_style

                text "persistent.quick_menu_style"
                text "%s" %persistent.quick_menu_style

                text "persistent.quick_menu_align"
                text "%s" %persistent.quick_menu_align

                ## divide (and conquer)
                null height 50

                ## We've got to get back out of this screen somehow, right?
                textbutton _("Return") action Return()



screen conf_button():

    if config.developer:
        vbox:
            xalign 0.98
            ypos 0.165

            imagebutton:
                alt "change configuration settings"
                auto "gui/button/settings_%s.png"
                hover_foreground Text(_("Configure GUI"), xalign=0.5, yalign=0.5)
                idle_foreground Text(_("Configure GUI"), xalign=0.5, yalign=0.5)
                selected_idle "gui/button/settings_selected_idle.png"
                selected_hover "gui/button/settings_selected_hover.png"
                action ShowMenu("configs")
                tooltip _("Change Configuration settings")
