## This is a work in progress requiring major work, enable it at own risk.
## In config.rpy set persistent.gal_screen to True


image abc = "images/400x400.png"
image bca = "images/400x400b.png"
image lock = "images/400x400c.png"

init python:

    # Step 1. Create the gallery object.
    g = Gallery()

    # Step 2. Add buttons and images to the gallery.

    # A button that contains an image that automatically unlocks.
    g.button("thumb")
    g.image("abc")
    g.unlock("abc")
    g.unlocked_advance = True
    g.locked_button = "images/400x400c.png"
    
    g.button("thumb_b")
    g.image("bca")
    g.unlock("bca")
    g.unlocked_advance

    # The transition used when switching images.
    g.transition = dissolve

# Step 3. The gallery screen we use.
screen gallery():

    # Ensure this replaces the main menu.
    tag menu
    
    # Add a style prefix.
    style_prefix "gallery"
    
    # Add the background image.
    add gui.game_menu_background
    
    # Arrange the images in a viewport grid.
        
    vpgrid:
        xpos 5
        ypos 80
        rows 5
        yinitial 0.0

        mousewheel True
        draggable True
        pagekeys True

        side_yfill True

        transclude

        xmaximum 700
        spacing 5

        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add Null()
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add g.make_button("thumb_b", "bca", xalign=0.5, yalign=0.5)
        add g.make_button("thumb", "abc", xalign=0.5, yalign=0.5)
        add Null()


    # The screen is responsible for returning to the main menu. It could also
    # navigate to other gallery screens.
    textbutton "Return" action Return() xalign 0.02 yalign 0.98
    