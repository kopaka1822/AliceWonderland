##### CHANGELOG #####

screen changelog():

    default ver_num = None
    tag menu
    use game_menu(_("Changelog"), scroll="viewport"):
        style_prefix "c_log"

        hbox:
            frame:
                ymaximum 1520
                xsize 310

                vpgrid:
                    cols 1
                    spacing 20
                    draggable True
                    mousewheel True
                    scrollbars None
                    xalign 0.45
                    yalign 0.5


                    for version_number in version_list:
                        imagebutton:
                            alt "version_number.name"
                            auto changelog_version_button_image
                            hover_foreground Text(_(version_number.name), xalign=0.5, yalign=0.5)
                            idle_foreground Text(_(version_number.name), xalign=0.5, yalign=0.5)
                            selected_idle "gui/button/settings_selected_idle.png"
                            selected_hover "gui/button/settings_selected_hover.png"
                            action (SetScreenVariable(name='ver_num', value= version_number))
                            tooltip _("version_number.name")

            null width 50

            vbox:
                xsize 610
                xalign 0.5
                ypos 20

                if ver_num:
                    text ver_num.name
                else:
                    pass

                ## Used as a content divider
                if ver_num:
                    null height 5
                    bar ysize 5 xsize 400
                    null height 5

                if ver_num:
                    text ver_num.cha
                else:
                    pass


init python:
    class Item(object):
        def __init__(self, name, changes):
            self.name = name
            self.cha = changes

default version_list = [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10]

define item1 = Item("v1.28", "[v128]")
define item2 = Item("v1.29", "[v129]")
define item3 = Item("v1.30", "[v130]")
define item4 = Item("v1.31", "[v131]")
define item5 = Item("v1.32", "[v132]")
define item6 = Item("Item 6", "Item 6")
define item7 = Item("Item 7", "Item 7")
define item8 = Item("Item 8", "Item 8")
define item9 = Item("Item 9", "Item 9")
define item10 = Item("Item 10", "Item 10")

style c_log_label is gui_label
style c_log_label_text is gui_label_text
style c_log_text is gui_text
style c_log_label_text:
    size gui.label_text_size
style c_log_frame:
    background Frame("gui/blank.png", gui.frame_borders, tile=gui.frame_tile)




define v128 = _("""
- Added a {color=#000}changelog{/color}.
- Added {color=#000}in_nvl{/color} variable (Line 260) for checking if in NVL mode and not show the {color=000}persistent.quick_menu_align{/color} toggle button.
- Adjusted {color=000}game_menu_label{/color} text size and centered it.
- Changed {color=000}return button design{/color} in game_menu to match rest of GUI.
- Updated {color=FFFF00}History screen{/color} to fit the new {color=000}1080x1920{/color} resolution.
- Added screen {color=000}nav_content{/color} for displaying main menu buttons on screens other than the main menu.
""")


define v129 = _("""
- Condensed all button background images into an easily modified buttons.rpy file. Now all button images can be easily changed by changing a single file path.
- Added {color=000}new_game_%s.png{/color} to show how the buttons can be individually changed now.
- Adjusted load/save screen thumbnail sizes, thumbnail positions, bordersize, load/save time text position.
- Aligned pagination buttons between save slot thumbnails and navigation menu buttons.
""")

define v130 = _("""
- Added additional button states to buttons.rpy
- Added {color=000}history{/color} button to buttons.rpy
- Fixed odd behaviour of {color=FFFF00}Extras{/color} screen.
- Added {color=FFFF00}underconstruction{/color} screen as a placeholder for screens that exist, but are not ready.
- Adjusted screen {color=FFFF00}Extras{/color} to look like screen {color=FFFF00}Settings{/color}, keeping the theme consistent.
- Adjusted {color=000}style game_menu_outer_frame:{/color} to not overflow the navigation content.
- Adjusted buttons to navigate pages in save/load screens to {color=000}yalign 1.0{/color} (previously 0.83) to fit better in the new game_menu_outer_frame size.
- Changed {color=FFFF00}line 39{/color} of changelog.rpy to {color=000}xsize 610{/color}, removing 20 pixels to fix overflowing text.
- Edited {color=FFFF00}nav_content{/color} screen to show {color=FFFF00}History{/color} instead of \"New Game\", added a save button and removed extras button.
""")

define v131 = _("""
- Fixed quick_menu_style toggle button behaviour. The wrong quick menu style could be left on screen if not hidden before switching styles.
- Adjusted help menu to match button theme established in other screens.
- Minor positioning adjustments to various screens.
- Removed unused phone variant images.
- Created new buttons for help screen to depict devices as the text based buttons were too large.
- Removed considerable redundant imagebutton image states. This removes 90 lines of code from the current GUI, and possibly more from future versions.
- Partial optimisation of {color=FFFF00}help{/color} screen and controller support.
- Various screens have been optimised to have less redundancy.
- Began moving screens with multiple available styles to their own .rpy file in an attempt to streamline the GUI later.
""")

define v132 = _("""
- Not yet available -

Preparing for the release of v2.0
v2.0 will (hopefully) allow the user to select between Portrait (9:16) and Landscape (16:9) with a single preference option.
(This will require additional GUI elements and more artwork if used, keep that in mind)
""")

#### TODO ####

# -
# -
# -
