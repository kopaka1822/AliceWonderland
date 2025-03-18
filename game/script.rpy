default persistent.started_story = False

init python:
    import random
    import time

    # remove mouse wheel from rollback (its annoying in the browser)
    config.keymap['rollback'] = ['any_K_PAGEUP', 'any_KP_PAGEUP', 'K_AC_BACK']
    config.keymap['rollforward'] = ['any_K_PAGEDOWN', 'any_KP_PAGEDOWN']

    renpy.register_shader("game.breathing", variables="""
        uniform sampler2D tex0;
        uniform float u_time;
        uniform float u_breath_cycle;
        uniform float u_offset; // in 0 1
        uniform vec2 res0;
        varying vec2 v_tex_coord;
    """, fragment_300="""
        float scale = 0.5 + 0.5 * sin((u_offset + u_time / u_breath_cycle) * 2.0 * 3.141);
        #ifndef TEXC
        vec2 texC = v_tex_coord.xy;
        #endif
        texC.y = 1.0 - (1.0 - texC.y) * (1.0 + 0.01 * scale);
        if(texC.y < 0.0 || texC.y > 1.0) discard;

        gl_FragColor = texture2D(tex0, texC, -0.55);
    """)
    renpy.register_shader("game.animation", variables="""
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform float u_time;
        uniform float u_breath_cycle;
        uniform float u_offset; // in 0 1
        varying vec2 v_tex_coord;
    """, fragment_250="""
        float a = texture2D(tex1, v_tex_coord, -0.5).x;
        #define TEXC
        vec2 texC = v_tex_coord.xy;
        float xspread = -(texC.x - 0.5) * (1.0 + sin((u_offset + u_time / u_breath_cycle) * 2.0 * 3.141)) * a * 0.04;
        texC.x += xspread;
        texC.y += cos((u_offset + u_time / u_breath_cycle) * 2.0 * 3.141) * a * 0.006;
        gl_FragColor = texture2D(tex0, texC, -0.5);
    """)

    renpy.register_shader("game.wind", variables="""
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform float u_time;
        uniform vec2 res0;
        varying vec2 v_tex_coord;
    """, fragment_300="""
        float a = texture2D(tex1, v_tex_coord, 0.5).x;
        #define TEXC
        vec2 texC = v_tex_coord.xy;
        if(a > 0.0){
            // original from https://github.com/bitsawer/renpy-shader/blob/master/ShaderDemo/game/shader/shadercode.py
            const float FLUIDNESS = 0.75;
            const float WIND_SPEED = 1.0;
            const float DISTANCE = 2.0;
            vec2 pixel = texC * res0; // calc in pixel coordinates to be independent for wider images
            float modifier = sin(pixel.x * 0.006 + u_time) / 2.0 + 1.5;
            texC.x += sin(pixel.x * 0.006 * FLUIDNESS + u_time * WIND_SPEED) * modifier * a * (DISTANCE / res0.x);
            texC.y += cos(pixel.y * 0.02 * FLUIDNESS + u_time * WIND_SPEED) * a * (DISTANCE / res0.y);
        }
        gl_FragColor = texture2D(tex0, texC, -0.5);
    """)
    renpy.register_shader("game.mask2", variables="""
        uniform sampler2D tex0;
        uniform sampler2D tex2;
        varying vec2 v_tex_coord;
    """, fragment_500="""
        #ifndef TEXC
        vec2 texC = v_tex_coord.xy;
        #endif
        float alphaMask = texture2D(tex2, texC, -0.5).a;
        gl_FragColor = texture2D(tex0, texC, -0.5) * alphaMask;
    """)

    def get_shaders_breathing(child):
        if preferences.graphic_preset == 0:
            return "renpy.texture"
        if isinstance(child.target, renpy.display.im.Image):
            return ["renpy.texture", "game.breathing"]
        return ["renpy.texture", "game.animation", "game.breathing"]

    def get_shaders_swimming(child):
        if preferences.graphic_preset == 0:
            return "renpy.texture"
        if isinstance(child.target, renpy.display.im.Image):
            return ["renpy.texture"]
        return ["renpy.texture", "game.animation"]

    def get_shaders_wind(child):
        if preferences.graphic_preset <= 1:
            return "renpy.texture"
        return ["renpy.texture", "game.wind"]

    def get_shaders_wind_mask(child):
        if preferences.graphic_preset <= 1:
            return ["renpy.texture", "game.mask2"]
        return ["renpy.texture", "game.wind", "game.mask2"]

    def get_shader_breathing_pause():
        if preferences.graphic_preset == 0:
            return 3600
        if preferences.graphic_preset == 1:
            return 0.1
        return 0
    
    def get_shader_wind_pause():
        if preferences.graphic_preset <= 1:
            return 3600
        return 0

    def get_object_rng(obj):
        if isinstance(obj, renpy.display.image.ImageReference):
            return (hash(obj.name[0]) % 7919) / 7919
        return 0.0

    def zoom_for_zpos(zpos):
        if zpos < 0: return 1 - 0.00142 * zpos
        return 1 - 0.0014 * zpos


define alice = Character("Alice", color="#ADD8E6")
define rabbit = Character(_("Rabbit"), color="#ffffff")
define mouse = Character(_("Mouse"), color="#adadad")
define lory = Character(_("Lory"), color="#8c00ff")
define duck = Character(_("Duck"), color="#ff8c00")
define dodo = Character(_("Dodo"), color="#008cff")
define eaglet = Character(_("Eaglet"), color="#be8200")
define everyone = Character(_("Everyone"), color="#ffffff")
define old_crab = Character(_("Old Crab"), color="#ff4a3d")
define young_crab = Character(_("Young Crab"), color="#ff8c00")
define magpie = Character(_("Magpie"), color="#ffffff")
define canary = Character(_("Canary"), color="#ffe600")
define pat = Character(_("Pat"), color="#00ff00")
define anon = Character("???", color="#ffffff")
define bill = Character("Bill", color="#b5ff9e")
define caterpillar = Character(_("Caterpillar"), color="#5cffc9")
define pigeon = Character(_("Pigeon"), color="#adadad")
define fishfoot = Character(_("Fish-Footmen"), color="#9694ff")
define frogfoot = Character(_("Frog-Footmen"), color="#b5ff9e")
define duchess = Character(_("Duchess"), color="#ff8c00")
define cat = Character(_("Cheshire Cat"), color="#fa6400")
define hare = Character(_("March Hare"), color="#fa6400")
define hatter = Character(_("Mad Hatter"), color="#00ff00")
define dormouse = Character(_("Dormouse"), color="#ff8c00")
define two = Character(_("Two"), color="#eee")
define five = Character(_("Five"), color="#eee")
define seven = Character(_("Seven"), color="#eee")
define queen = Character(_("Queen"), color="#ff0000")
define soldiers =  Character(_("Soldiers"), color="#fff")
define king = Character(_("King"), color="#ff0000")
define gryphon = Character(_("Gryphon"), color="#ff8c00")
define mock = Character(_("Mock Turtle"), color="#6cb30f")
define cook = Character(_("Cook"), color="#ffffff")
define knave = Character(_("Knave"), color="#ff0000")
define sister = Character(_("Sister"), color="00ff00")

define alice_scale = 0.55
define alice_scale_large = 1.3
define rabbit_scale = 0.7
define mouse_scale = 0.5
define queen_scale = 0.98
define king_scale = 1.0
define cat_scale = 0.5
define duchess_scale = 0.52

define cam_transition = 0.5
define center_offset = 540 # half of 1080


define three_legged_table_xpos = 5.55
define three_legged_table_ypos = 1.06
define three_legged_table_zpos = -400.0
define three_legged_table_zoom = 0.9


## ANIMATED TRANSFORMS ##
## remove comment below to work with action editor
P'''
transform breathing_calm(child):
    child
    anchor (0.5, 1.0)
    shader get_shaders_breathing(child)
    u_breath_cycle 6.0
    u_offset get_object_rng(child)
    pause get_shader_breathing_pause()
    repeat

transform breathing(child):
    child
    anchor (0.5, 1.0)
    shader get_shaders_breathing(child)
    u_breath_cycle 5.0
    u_offset get_object_rng(child)
    pause get_shader_breathing_pause()
    repeat

transform breathing_crying(child):
    child
    anchor (0.5, 1.0)
    shader get_shaders_breathing(child)
    u_offset get_object_rng(child)
    #u_breath_cycle 3.5
    u_breath_cycle 5.0
    pause get_shader_breathing_pause()
    repeat

transform swimming(child):
    child
    anchor (0.5, 1.0)
    shader get_shaders_swimming(child)
    u_breath_cycle 5.0
    u_offset get_object_rng(child)
    ease 2.0 yoffset -10 
    ease 2.0 yoffset 10
    # TODO maybe add breathing anim.
    repeat

transform windy(child):
    anchor (0.5,0)
    pos(0.0,0)
    xoffset center_offset
    child
    shader get_shaders_wind(child)
    pause get_shader_wind_pause()
    repeat

transform windy_no_anchor(child):
    child
    shader get_shaders_wind(child)
    pause get_shader_wind_pause()
    repeat

transform windy_mask(child):
    anchor (0.5,0)
    pos(0.0,0)
    xoffset center_offset
    child
    shader get_shaders_wind_mask(child)
    pause get_shader_wind_pause()
    repeat

# alice pictures
image alice sleepy = Model().child("alice sleepy.png", fit=True).texture("alice_mask.png")
image alice crying = Model().child("alice crying.png", fit=True).texture("alice_mask.png")
image alice excited = Model().child("alice excited.png", fit=True).texture("alice_mask.png")
image alice happy = Model().child("alice happy.png", fit=True).texture("alice_mask.png")
image alice normal = Model().child("alice normal.png", fit=True).texture("alice_mask.png")
image alice pout = Model().child("alice pout.png", fit=True).texture("alice_mask.png")
image alice surprised = Model().child("alice surprised.png", fit=True).texture("alice_mask.png")
image alice thinking = Model().child("alice thinking.png", fit=True).texture("alice_mask.png")
image alice belly = Model().child("alice belly.png", fit=True).texture("alice_belly_mask.png")
image alice disturbed = Model().child("alice disturbed.png", fit=True).texture("alice_mask.png")
image alice joking = Model().child("alice joking.png", fit=True).texture("alice_mask.png")

image queen normal = Model().child("queen normal.png", fit=True).texture("queen_mask.png")
image queen happy = Model().child("queen happy.png", fit=True).texture("queen_mask.png")
image queen angry = Model().child("queen angry.png", fit=True).texture("queen_mask.png")

image king = Model().child("king.png", fit=True).texture("king_mask.png")
image king scared = Model().child("king scared.png", fit=True).texture("king_mask.png")

image rabbit normal = Model().child("rabbit normal.png", fit=True).texture("rabbit_mask.png")
image rabbit court = Model().child("rabbit court.png", fit=True).texture("rabbit_mask.png")

image dormouse sleep = Model().child("dormouse sleep.png", fit=True).texture("dormouse sleep_mask.png")
image dormouse tired = Model().child("dormouse tired.png", fit=True).texture("dormouse tired_mask.png")

image hatter normal = Model().child("hatter normal.png", fit=True).texture("hatter_mask.png")
image hatter scared = Model().child("hatter scared.png", fit=True).texture("hatter_mask.png")

image hare = Model().child("hare.png", fit=True).texture("hare_mask.png")

image gryphon = Model().child("gryphon.png", fit=True).texture("gryphon_mask.png")

# backgrounds

image blades = Model().child("blades.png", fit=True).texture("blades_wind.png")
image buttercup = Model().child("buttercup.png", fit=True).texture("buttercup_wind.png")
'''

# non-animated transforms (comment in for action editor)
transform breathing_calm:
    anchor (0.5, 1.0)

transform breathing:
    anchor (0.5, 1.0)

transform breathing_crying:
    anchor (0.5, 1.0)

transform swimming:
    anchor (0.5, 1.0)
    ease 2.0 yoffset -10 
    ease 2.0 yoffset 10
    repeat

transform windy:
    anchor (0.5,0)
    pos (0,0)
    xoffset center_offset

transform windy_no_anchor:
    xoffset 0 # do nothing

transform windy_mask:
    anchor (0.5,0)
    pos (0,0)
    xoffset center_offset

#'''
# end comment out



# general transforms / lables
transform anchor:
    anchor (0.5, 1.0)

transform popup:
    align (0.5, 0.5) ypos 0.38

transform angrily:
    anchor (0.5, 0.5)
    ease 2 rotate 10 zoom 0.9
    ease 2 rotate 0 zoom 1.0
    repeat

transform parallax(z=0):
    anchor (0.5, 0.5)
    pos (0.5, 0.5)
    zpos z
    # zzoom True # zzoom does not work with tiling qwq
    zoom zoom_for_zpos(z)

label reset_camera:
    camera:
        perspective False
        xpos 0 ypos 0 zpos 0 zoom 1.0 xoffset 0 zrotate 0
    return

label start:
    # select language on first start
    call screen language

label chapter1:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1001"
    "{size=+40}Chapter I: \n{/size}Down the Rabbit-Hole"

    #scene riverbank at windy
    scene bluesky at parallax(-4000)
    show hills at parallax(-4000)
    show water at parallax(-300):
        xpos 1.3 xtile 5 yoffset 110
        linear 10.0 xoffset 1460
        xoffset 0
        repeat
    show river at parallax(-300):
        xoffset -900 xtile 5 yoffset 110
    show grass at parallax:
        yoffset 550 xoffset -900 xtile 3
    show tree at parallax(300) zorder 10:
        xpos -0.48
    
    play music "audio/rinne wanderer.mp3"

    define alice_riverbank = -0.22
    define rabbit_riverbank = 0.5

    camera:
        perspective True
        xpos alice_riverbank xoffset -center_offset

    show alice sleepy at breathing_calm:
        xpos -0.22 ypos 0.9 zoom alice_scale

    voice "n1002"
    "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it."

    camera:
        ease cam_transition zpos -300
    
    show alice surprised at breathing_calm
    voice "alice001"
    alice "(And what is the use of a book without pictures or conversations?)" 

    show alice sleepy at breathing_calm
    voice "n1003"
    "So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    voice "n1004"
    "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself:"

    show rabbit normal at breathing:
        xpos rabbit_riverbank ypos 0.9 zoom rabbit_scale
    camera:
        ease cam_transition xpos rabbit_riverbank ypos 400 zpos -300

    voice "rabbit01"
    rabbit "Oh dear! Oh dear! I shall be too late!"

    voice "n1005"
    "(When she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural)"
    
    voice "n1006"
    "But when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it."
    
    show rabbit normal at breathing:
        ease 1.0 xpos 1.0 ypos 2.0
    show alice excited at breathing:
        zoom 0.6
        ease 1.0 xpos rabbit_riverbank
    camera:
        ease cam_transition xpos rabbit_riverbank ypos 0 zpos 0
    voice "n1007"
    "Burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge."

    show alice happy at breathing:
        ease 1.0 xpos 1.0 ypos 2.0
    voice "n1008"
    "In another moment down went Alice after it, never once considering how in the world she was to get out again."

    scene black
    call reset_camera

    stop music fadeout 1.0
    voice "n1009"
    "The rabbit-hole went straight on like a tunnel for some way."
    
    scene well at center 
    play music "audio/rinne aurelia.mp3" fadeout 1.0 fadein 1.0 

    show alice falling:
        xpos -0.4 ypos 0.0
        linear 1.0 xoffset -20 yoffset -20 rotate 5
        linear 1.0 xoffset 20 yoffset 20 rotate -5
        linear 1.0 xoffset -20 yoffset 20 rotate 5
        linear 1.0 xoffset 20 yoffset -20 rotate -5
        repeat

    voice "n1010"
    "And then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well."

    voice "n1011"
    "Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next."

    voice "n1012"
    "First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs."

    hide alice
    show popup at popup onlayer screens
    show orange marmalade at popup onlayer screens

    voice "n1013"
    "She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it."

    hide orange marmalade onlayer screens
    hide popup onlayer screens
    show alice falling:
        xpos -0.4 ypos 0.0
        linear 1.0 xoffset -20 yoffset -20 rotate 5
        linear 1.0 xoffset 20 yoffset 20 rotate -5
        linear 1.0 xoffset -20 yoffset 20 rotate 5
        linear 1.0 xoffset 20 yoffset -20 rotate -5
        repeat

    voice "alice002"
    alice "(Well! After such a fall as this, I shall think nothing of tumbling down stairs!)"  
    
    voice "alice003"
    alice "(How brave they'll all think me at home!)" 
    
    voice "alice004"
    alice "(Why, I wouldn’t say anything about it, even if I fell off the top of the house!)"  
    
    voice "n1014"
    "(Which was very likely true)"

    voice "n1015"
    "Down, down, down. Would the fall never come to an end?"
    voice "alice005"
    alice "I wonder how many miles I've fallen by this time?"
    voice "alice006"
    alice "I must be getting somewhere near the centre of the earth."
    voice "alice007"
    alice "Let me see: that would be four thousand miles down, I think—"

    voice "n1016"
    "(for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over)"

    voice "alice008"
    alice "—yes, that’s about the right distance—but then I wonder what Latitude or Longitude I’ve got to?"

    voice "n1017"
    "(Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say)"

    voice "n1018"
    "Presently she began again."

    voice "alice009"
    alice "I wonder if I shall fall right through the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think—"

    voice "n1019"
    "(she was rather glad there was no one listening, this time, as it didn’t sound at all the right word)"

    voice "alice010"
    alice "—but I shall have to ask them what the name of the country is, you know. Please, Ma’am, is this New Zealand or Australia?"

    voice "n1020"
    "(and she tried to curtsey as she spoke—fancy curtseying as you’re falling through the air! Do you think you could manage it?)"

    voice "alice011"
    alice "And what an ignorant little girl she’ll think me for asking! No, it’ll never do to ask: perhaps I shall see it written up somewhere."

    voice "n1021"
    "Down, down, down."

    voice "n1022"
    "There was nothing else to do, so Alice soon began talking again."

    voice "alice012"
    alice "Dinah’ll miss me very much to-night, I should think!"

    voice "n1023"
    "(Dinah was the cat)"

    voice "alice013"
    alice "I hope they’ll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me!"
    voice "alice014"
    alice "There are no mice in the air, I’m afraid, but you might catch a bat, and that’s very like a mouse, you know." 
    voice "alice015"
    alice "But do cats eat bats, I wonder?"

    voice "n1024"
    "And here Alice began to get rather sleepy, and went on saying to herself, in a dreamy sort of way:"
    voice "alice016"
    alice "Do cats eat bats? Do cats eat bats?"

    voice "n1025"
    "And sometimes"
    voice "alice017"
    alice "Do bats eat cats?" 

    voice "n1026"
    "You see, as she couldn’t answer either question, it didn’t much matter which way she put it."
    
    voice "n1027"
    "She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly:"
    voice "alice018"
    alice "Now, Dinah, tell me the truth: did you ever eat a bat?"

    stop music fadeout 1.0
    scene black

    play sound "sfx/thump2.mp3"
    voice "n1028"
    "When suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over."
    
    voice "n1029"
    "Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead."

    scene passage
    image passage_front_mask = AlphaMask("passage", "passage_front")
    show passage_front_mask zorder 10
    call reset_camera
    camera:
        perspective True

    show rabbit normal at breathing zorder 5:
        xpos 0.54 ypos 0.58 zoom 0.25

    show alice surprised at breathing zorder 20:
        xpos 0.82 ypos 0.9 zoom alice_scale

    voice "n1030"
    "Before her was another long passage, and the White Rabbit was still in sight, hurrying down it."

    show rabbit normal at breathing zorder 5:
        ease 1.0 xpos 0.38 ypos 0.54 zoom 0.2
    voice "n1031"
    "There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner:"

    
    camera:
        perspective True
        ease cam_transition xpos 0.14 ypos 955 zoom 2.09
    voice "rabbit02"
    rabbit "Oh my ears and whiskers, how late it's getting!"
    
    show rabbit normal at breathing zorder 5:
        ease 1.0 xpos 0.14
    show alice pout at breathing zorder 20:
        ease 1.0 xpos 0.52 ypos 0.58 zoom 0.2
    voice "n1032"
    "She was close behind it when she turned the corner, but the Rabbit was no longer to be seen."

    jump ch1_hall_start

label setup_hallway:
    show court_floor as floor1:
        align (0.5, 0.5) pos(1024, 1.0) xrotate 90.0 zoom 2.0

    show court_floor as floor2:
        align (0.5, 0.5) pos(3072, 1.0) xrotate 90.0 zoom 2.0

    show court_floor as floor3:
        align (0.5, 0.5) pos(5120, 1.0) xrotate 90.0 zoom 2.0

    show court_floor as floor4:
        align (0.5, 0.5) pos(7168, 1.0) xrotate 90.0 zoom 2.0

    show court_floor as floor5:
        align (0.5, 0.5) pos(9216, 1.0) xrotate 90.0 zoom 2.0

    show court_floor as floor6:
        align (0.5, 0.5) pos(11264, 1.0) xrotate 90.0 zoom 2.0
    
    show garden:
        align (0.5, 1.0) xpos 9.79 ypos 0.96 zpos -655.0 zoom 0.42

    show hallway doors:
        align (0.0, 1.0) zoom 5.3 zpos -450

    show lamp antique as lamp1 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32

    show lamp antique as lamp2 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 1.6
        
    show lamp antique as lamp3 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 2.7
        
    show lamp antique as lamp4 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 3.8
        
    show lamp antique as lamp5 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 4.9
        
    show lamp antique as lamp6 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 6.0
        
    show lamp antique as lamp7 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 7.1

    show lamp antique as lamp8 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 8.2
        
    show lamp antique as lamp9 zorder 110:
        zpos 100 zoom 3.0 align (0.5, 0.0) ypos -0.32 xpos 9.3

    return

label ch1_hall_start:


    play music "audio/rinne memories of clockwise tower.mp3" fadein 1.0
    scene black
    call setup_hallway
    call reset_camera

    define alice_hall_start_pos = 8695
    define alice_hall_default_zoom = 0.66
      

    show alice normal at breathing zorder 100:
        xpos alice_hall_start_pos zoom alice_hall_default_zoom zpos -45.0 ypos 1.0


    camera:
        perspective True
        xpos 885 xoffset -center_offset ypos 0 zpos 0 zoom 1.0
        ease 10 xpos alice_hall_start_pos
    
    voice "n1033"
    "She found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof."

    voice "n1034"
    "There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again."
    
    show three_legged_table_key zorder 50:
        align (0.5, 1.0) xpos three_legged_table_xpos zoom three_legged_table_zoom zpos three_legged_table_zpos ypos three_legged_table_ypos

    camera:
        ease 3 xpos 6000

    define alice_hall_table_pos1 = 6500

    show alice normal at breathing:
        ease 2 xpos alice_hall_table_pos1

    voice "n1035"
    "Suddenly she came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them."
    
    define alice_hall_curtain_pos = 10390
    camera:
        ease 3 xpos alice_hall_curtain_pos ypos 255 zpos -595

    voice "n1036"
    "However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about fifteen inches high: she tried the little golden key in the lock, and to her great delight it fitted!"

   
    #camera:
    #    ease 3 xpos 10555 ypos 465 zpos -1085.0
    # TODO garden?

    play sound "sfx/unlock.mp3"
    voice "n1037"
    "Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw."

    camera:
        ease 3 xpos 10390 ypos 255 zpos -595

    show alice normal at breathing:
        xpos alice_hall_start_pos zoom alice_hall_default_zoom zpos -45.0

    camera:
        ease 4 xpos alice_hall_start_pos zpos 0 ypos 0

    
    show alice pout at breathing
    voice "n1038"
    "How she longed to get out of that dark hall, and wander about among those beds of bright flowers and those cool fountains, but she could not even get her head through the doorway."

    camera:
        ease 4 xpos alice_hall_start_pos zpos 0 ypos 0

    #show alice pout at breathing:
    #    xpos 0.5 ypos 0.9 zoom alice_scale
    voice "alice019"
    alice "(And even if my head would go through, it would be of very little use without my shoulders)"
    show alice excited at breathing
    voice "alice020"
    alice "(Oh, how I wish I could shut up like a telescope! I think I could, if I only knew how to begin)"

    voice "n1039"
    "For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible."

    hide three_legged_table_key
    show three_legged_table_bottle:
        align (0.5, 1.0) xpos three_legged_table_xpos zoom three_legged_table_zoom zpos three_legged_table_zpos ypos three_legged_table_ypos

    show alice normal at breathing: 
        ease 2 xpos 6500 zpos -405.0 

    camera:
        perspective True
        xpos 8695 xoffset -center_offset
        ease 3 xpos 6300


    voice "n1040"
    "There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it."
    show alice thinking at breathing:
        xpos 6500 zpos -405.0
    voice "alice021"
    alice "This certainly was not here before."

    camera:
        ease 2 xpos 6100 ypos 330 zpos -845
    voice "n1041"
    "Around the neck of the bottle was a paper label, with the words 'DRINK ME' beautifully printed on it in large letters."
    
    camera:
        ease 2 xpos 6300 ypos 0 zpos 0

    voice "n1042"
    "It was all very well to say 'Drink me', but the wise little Alice was not going to do that in a hurry."

    voice "alice022"
    alice "No, I’ll look first and see whether it’s marked 'poison' or not."
    
    voice "n1043"
    "She had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they would not remember the simple rules their friends had taught them: "
    voice "n1044"
    "Such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger very deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked 'poison', it is almost certain to disagree with you, sooner or later."

    play sound "sfx/cork.mp3"

    show alice happy at breathing
    voice "n1045"
    "However, this bottle was not marked 'poison,' so Alice ventured to taste it, and finding it very nice, (it had, in fact, a sort of mixed flavour of cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off."
    
    camera:
        pause 1.0
        ease 8.0 zpos -770 ypos 730 xpos 6500
    show alice surprised at breathing:
        ease 10.0 zoom 0.2

    voice "alice023"
    alice "What a curious feeling! I must be shutting up like a telescope."

    

    voice "n1046"
    "And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden."

    voice "n1047"
    "First, however, she waited for a few minutes to see if she was going to shrink any further: she felt a little nervous about this."
    voice "alice024"
    alice "It might end, you know, in my going out altogether, like a candle. I wonder what I should be like then?"

    hide three_legged_table_bottle

    show box_cake:
        align (0.5, 0.8) xpos 5.48 ypos 1.0 zpos -400.0 zoom 0.125

    show three_legged_table_key:
        align (0.5, 1.0) xpos three_legged_table_xpos zoom three_legged_table_zoom zpos three_legged_table_zpos ypos three_legged_table_ypos


    voice "n1048"
    "And she tried to fancy what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing."

    define alice_hall_table_leg_pos = 6100

    show alice thinking at breathing:
        zoom 0.2
        # go to garden animation
        ease 5 xpos alice_hall_curtain_pos
        pause 2.0
        xzoom -1
        # go back to table animation
        ease 5 xpos alice_hall_table_leg_pos zpos -405.0
    camera:
        # go to garden animation
        ease 5.5 xpos alice_hall_curtain_pos
        pause 1.5
        # go to table animation
        ease 5.5 xpos alice_hall_table_leg_pos zpos -770.0 ypos 730

    voice "n1049"
    "After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice, when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: "
    camera:
        xpos alice_hall_table_leg_pos zpos -770.0 ypos 730
    show alice pout at breathing:
        zoom 0.2 xpos alice_hall_table_leg_pos zpos -405.0 xzoom -1
        pause 1.0
        easein 1.0 ypos 0.95
        easeout 1.0 ypos 1.0

    
    play sound "<silence 8.0>"
    queue sound "voice/alice_crying1.mp3"
    voice "n1050"
    "She could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried."
    show alice crying at breathing_crying:
        zoom 0.2 xpos alice_hall_table_leg_pos zpos -405.0 xzoom -1

    voice "alice025"
    alice "(Come, there’s no use in crying like that!)"
    show alice pout at breathing
    voice "alice026"
    alice "(I advise you to leave off this minute!)"

    voice "n1051"
    "She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people."
    voice "alice027"
    alice "(But it’s no use now, to pretend to be two people! Why, there’s hardly enough of me left to make one respectable person!)"

    #hide alice 
    camera:
        ease 2 xpos 5920 ypos 820 zpos -800.0
    voice "n1052"
    "Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words 'EAT ME' were beautifully marked in currants."

    camera: 
        ease 2 xpos 6035 ypos 730 zpos -770.0 

    show alice normal at breathing
    voice "alice028"
    alice "Well, I’ll eat it, and if it makes me grow larger, I can reach the key; and if it makes me grow smaller, I can creep under the door: so either way I’ll get into the garden, and I don’t care which happens!"

    voice "n1053"
    "She ate a little bit." #, and said anxiously to herself: "
    show alice excited at breathing
    voice "alice029"
    alice "(Which way? Which way?)" # anxiously
    voice "n1054"
    "She was holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to find that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way."
    voice "n1055"
    "So she set to work, and very soon finished off the cake."
    
    hide box_cake_removebg

label chapter2:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1056"
    "{size=+40}Chapter II: \n{/size}The Pool of Tears"

    scene black
    call setup_hallway
    call reset_camera
    
    play music "audio/rinne memories of clockwise tower.mp3"

    show three_legged_table_key:
        align (0.5, 1.0) xpos three_legged_table_xpos zoom three_legged_table_zoom zpos three_legged_table_zpos ypos three_legged_table_ypos


    camera:
        perspective True
        xpos 6080 zpos -500 ypos 530
        pause 2.0
        ease 10.0 zpos 0 ypos 0
    
    show alice excited at breathing:
        xpos 6605 ypos 1.0 zpos -340.0 
        zoom 0.2
        easeout 10.0 zoom alice_scale_large

    voice "alice030"
    alice "Curiouser and curiouser!"
    voice "n1057"
    "(she was so much surprised, that for the moment she quite forgot how to speak good English)"
    voice "alice031"
    alice "Now I’m opening out like the largest telescope that ever was!"
    voice "alice032"
    alice "Good-bye, feet!"
    voice "n1058"
    "(For when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off)"
    show alice surprised at breathing:
        zoom alice_scale_large
    voice "alice033"
    alice "(Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able!)"
    voice "alice034"
    alice "(I shall be a great deal too far off to trouble myself about you: you must manage the best way you can; —but I must be kind to them, or perhaps they won’t walk the way I want to go!)" 
    voice "alice035"
    alice "(Let me see: I’ll give them a new pair of boots every Christmas)"
    voice "n1059"
    "And she went on planning to herself how she would manage it."
    show alice normal at breathing
    voice "alice036"
    alice "(They must go by the carrier, and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!)"
    voice "n1060" # should this be alice?
    "Alice’s Right Foot, Esq. \nHearthrug, \nNear the Fender, \n(with Alice’s love)\n"
    show alice joking at breathing
    voice "alice037"
    alice "(Oh dear, what nonsense I’m talking!)"
    play sound "sfx/bump.mp3"
    show alice normal at breathing
    voice "n1061"
    "Just then, her head struck against the roof of the hall: in fact she was now rather more than nine feet high, and she at once took up the little golden key and hurried off to the garden door."
    voice "n1062"
    "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again."
    show alice crying at breathing_crying
    voice "alice038"
    alice "You ought to be ashamed of yourself, a great girl like you, to go on crying in this way! Stop this moment, I tell you!"
    voice "n1063"
    "But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall."

    show alice pout at breathing
    voice "n1064"
    "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming."
    voice "n1065"
    "It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other:"
    voice "n1066"
    "He came trotting along in a great hurry, muttering to himself as he came:"

    show rabbit normal at breathing:
        xpos 7.35 ypos 0.9 zoom 0.5
        ease 1.0 xpos 7.25
    camera:
        ease cam_transition xpos 7270 ypos 385 zpos -365
    voice "rabbit03"
    rabbit "Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!"
    voice "n1067"
    "Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice:"
    camera:
        ease cam_transition xpos 6035 ypos 0 zpos 0
    show alice surprised at breathing
    voice "alice039"
    alice "If you please, sir—"
    # hide alice

    show popup at popup onlayer screens
    show fan gloves at popup onlayer screens
    camera:
        ease cam_transition xpos 7270 ypos 385 zpos -365
    show rabbit normal at breathing:
        xpos 7.25 ypos 0.9 zoom 0.5
        ease 2.0 xpos 7.75
    voice "n1068"
    "The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go."
    camera:
        ease cam_transition xpos 6035 ypos 0 zpos 0
    voice "n1069"
    "Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking:"
    hide fan gloves onlayer screens
    hide popup onlayer screens
    hide rabbit

    show alice pout at breathing
    voice "alice040"
    alice "Dear, dear! How queer everything is to-day! And yesterday things went on just as usual."
    show alice thinking at breathing
    voice "alice041"
    alice "I wonder if I’ve been changed in the night? Let me think:"
    voice "alice042"
    alice "Was I the same when I got up this morning? I almost think I can remember feeling a little different."
    voice "alice043"
    alice "But if I’m not the same, the next question is, Who in the world am I? Ah, that’s the great puzzle!"
    voice "n1070"
    "And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them."
    voice "alice044"
    alice "I’m sure I’m not Ada, for her hair goes in such long ringlets, and mine doesn’t go in ringlets at all; and I’m sure I can’t be Mabel, for I know all sorts of things, and she, oh! she knows such a very little! Besides, she’s she, and I’m I, and—oh dear, how puzzling it all is!"
    voice "alice045"
    alice "I’ll try if I know all the things I used to know. Let me see: four times five is twelve, and four times six is thirteen, and four times seven is—oh dear! I shall never get to twenty at that rate!"
    voice "alice046"
    alice "However, the Multiplication Table doesn’t signify: let’s try Geography. London is the capital of Paris, and Paris is the capital of Rome, and Rome—no, that’s all wrong, I’m certain!"
    voice "alice047"
    alice "I must have been changed for Mabel! I’ll try and say 'How doth the little—'"
    voice "n1071"
    "And she crossed her hands on her lap as if she were saying lessons, and began to repeat it, but her voice sounded hoarse and strange, and the words did not come the same as they used to do:"
    voice "alice048"
    alice "How doth the little crocodile\n{space=30}Improve his shining tail,\nAnd pour the waters of the Nile\n{space=30}On every golden scale!"
    voice "alice049"
    alice "How cheerfully he seems to grin,\n{space=30}How neatly spread his claws,\nAnd welcome little fishes in\n{space=30}With gently smiling jaws!"

    show alice disturbed at breathing
    voice "alice050"
    alice "I’m sure those are not the right words."
    voice "alice051"
    alice "I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh!"
    voice "alice052"
    alice "Ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here!" 
    voice "alice053"
    alice "It’ll be no use their putting their heads down and saying 'Come up again, dear!' I shall only look up and say 'Who am I then?'" 
    show alice pout at breathing
    voice "alice054"
    alice "'Tell me that first, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else' —but, oh dear!"
    voice "alice055"
    alice "I do wish they would put their heads down! I am so very tired of being all alone here!"

    show alice thinking at breathing:
        easein 20.0 zoom 0.1

    camera:
        xpos 6035 zpos 0 ypos 0
        pause 1.0
        ease 20.0 xpos 6060 ypos 0.420 zpos -850.0
    
    voice "n1072"
    "As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking."
    voice "alice056"
    alice "How can I have done that?"
    voice "alice057"
    alice "I must be growing small again."
    
    show alice thinking at breathing:
        ease 2 zoom 0.1 xpos 6300
    camera:
        ease 2 xpos 5800 ypos 0.420 zpos -850.0
    voice "n1073"
    "She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly:"
    voice "n1103" # out of order oops
    "She soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether."

    voice "alice058"
    alice "That was a narrow escape!"
    show alice happy at breathing:
        ease 5  zoom 0.10
    voice "n1074"
    "She was a good deal frightened at the sudden change, but very glad to find herself still in existence."
    voice "alice059"
    alice "And now for the garden!"

    show alice happy at breathing:
        ease 2.8 xpos 10527 ypos 1.0 zpos -340.0
    camera:
        ease 3 xpos 9970 ypos 0.42 zpos -850.0
    voice "n1075"
    "And she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before."
    show alice pout at breathing:
        xpos 10527 ypos 1.0 zpos -340.0
    voice "alice060"
    alice "And things are worse than ever, for I never was so small as this before, never! And I declare it’s too bad, that it is!"

    stop music fadeout 1.0
    play sound "sfx/splash.mp3"
    voice "n1076"
    "As she said these words her foot slipped, and in another moment, splash!"
    
    camera:
        xpos 9970 ypos 0.42 zpos -850.0

    show waves zorder 0:
        xpos 9.93 ypos 1.19 zpos -595.0
        anchor (0.5, 1.0)
        linear 1.0 yoffset 20
        linear 1.0 yoffset 10
        repeat
    show wavestop zorder 99:
        xpos 9.93 ypos 1.21 zpos -385.0
        anchor (0.5, 1.0)
        linear 1.0 yoffset 20
        linear 1.0 yoffset 10
        repeat
    show alice pout zorder 1 at swimming:
        xpos 10527 ypos 1.0 zoom 0.1
    play music "audio/rinne beyond the sea.mp3"
    voice "n1077"
    "She was up to her chin in salt water."

    show alice thinking at swimming
    voice "n1078"
    "Her first idea was that she had somehow fallen into the sea."
    voice "alice061"
    alice "(And in that case I can go back by railway)"
    voice "n1079"
    "(Alice had been to the seaside once in her life, and had come to the general conclusion, that wherever you go to on the English coast you find a number of bathing machines in the sea, some children digging in the sand with wooden spades, then a row of lodging houses, and behind them a railway station)"
    voice "n1080"
    "However, she soon made out that she was in the pool of tears which she had wept when she was nine feet high."

    show alice pout at swimming
    voice "alice062"
    alice "I wish I hadn’t cried so much!"
    voice "n1081"
    "She swam about, trying to find her way out."
    voice "alice063"
    alice "I shall be punished for it now, I suppose, by being drowned in my own tears! That will be a queer thing, to be sure! However, everything is queer to-day."

    show alice thinking at swimming
    play sound "sfx/splash.mp3"
    voice "n1082"
    "Just then she heard something splashing about in the pool a little way off, and she swam nearer to make out what it was:"
    show alice thinking at swimming:
        ease 1.0 xpos 10450
    show mouse zorder 1 at swimming:
        xpos 11370 zpos -1050 ypos 1.07 zoom mouse_scale
        ease 2.0 xpos 10920 
    voice "n1083"
    "At first she thought it must be a walrus or hippopotamus, but then she remembered how small she was now, and she soon made out that it was only a mouse that had slipped in like herself."
    voice "alice064"
    alice "Would it be of any use, now, to speak to this mouse?"
    voice "alice065"
    alice "Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying."
    voice "n1084"
    "So she began:"
    show alice normal at swimming
    voice "alice066"
    alice "O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!"
    voice "n1085"
    "(Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, 'A mouse—of a mouse—to a mouse—a mouse—O mouse!')"
    voice "n1086"
    "The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing."

    show alice thinking at swimming
    voice "alice067"
    alice "Perhaps it doesn’t understand English, I daresay it’s a French mouse, come over with William the Conqueror."
    voice "n1087"
    "(For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened)"
    voice "n1088"
    "So she began again:"
    #voice "n1089"
    show alice normal at swimming
    voice "alice068"
    alice "Où est ma chatte?"
    voice "n1090"
    "Which was the first sentence in her French lesson-book."
    voice "n1091"
    "The mouse gave a sudden leap out of the water, and seemed to quiver all over with fright."
    show alice thinking at swimming
    voice "alice069"
    alice "Oh, I beg your pardon!"
    voice "n1092"
    "She was afraid that she had hurt the poor animal’s feelings."
    voice "alice070"
    alice "I quite forgot you didn’t like cats."

    voice "mouse01"
    mouse "Not like cats!"
    voice "mouse02"
    mouse "Would you like cats if you were me?"

    voice "alice071"
    alice "Well, perhaps not, don’t be angry about it."
    show alice happy at swimming
    voice "alice072"
    alice "And yet I wish I could show you our cat Dinah: I think you’d take a fancy to cats if you could only see her."
    voice "alice073"
    alice "She is such a dear quiet thing."
    voice "n1093"
    "Alice went on, half to herself, as she swam lazily about in the pool."
    voice "alice074"
    alice "And she sits purring so nicely by the fire, licking her paws and washing her face—and she is such a nice soft thing to nurse—and she’s such a capital one for catching mice—oh, I beg your pardon!"
    voice "n1094"
    "This time the Mouse was bristling all over, and she felt certain it must be really offended."
    show alice surprised at swimming
    voice "alice075"
    alice "We won’t talk about her any more if you’d rather not."

    voice "mouse03"
    mouse "We indeed!"
    voice "n1095"
    "The mouse was trembling down to the end of its tail."
    voice "mouse04"
    mouse "As if I would talk on such a subject! Our family always hated cats: nasty, low, vulgar things! Don’t let me hear the name again!"

    voice "alice076"
    alice "I won’t indeed!"
    voice "n1096"
    "Alice was in a great hurry to change the subject of conversation."
    voice "alice077"
    alice "Are you—are you fond—of—of dogs?"
    voice "n1097"
    "The mouse did not answer, so Alice went on eagerly:"
    show alice happy at swimming
    voice "alice078"
    alice "There is such a nice little dog near our house I should like to show you!"
    voice "alice079"
    alice "A little bright-eyed terrier, you know, with oh, such long curly brown hair!"
    voice "alice080"
    alice "And it’ll fetch things when you throw them, and it’ll sit up and beg for its dinner, and all sorts of things—I can’t remember half of them—and it belongs to a farmer, you know, and he says it’s so useful, it’s worth a hundred pounds!"
    voice "alice081"
    alice "He says it kills all the rats and—oh dear!"
    show alice crying at swimming
    voice "n1098"
    "Alice cried in a sorrowful tone."
    voice "alice082"
    alice "I’m afraid I’ve offended it again!"
    show mouse at swimming:
        linear 10.0 xoffset 1000
    voice "n1099"
    "For the Mouse was swimming away from her as hard as it could go, and making quite a commotion in the pool as it went."
    voice "alice083"
    alice "Mouse dear! Do come back again, and we won’t talk about cats or dogs either, if you don’t like them!"
    show alice normal at swimming
    show mouse at swimming:
        linear 10.0 xoffset 0
    voice "n1100"
    "When the Mouse heard this, it turned round and swam slowly back to her: its face was quite pale (with passion, Alice thought), and it said in a low trembling voice:"
    voice "mouse05"
    mouse "Let us get to the shore, and then I’ll tell you my history, and you’ll understand why it is I hate cats and dogs."
    voice "n1101"
    "It was high time to go, for the pool was getting quite crowded with the birds and animals that had fallen into it: there were a Duck and a Dodo, a Lory and an Eaglet, and several other curious creatures."
    stop music fadeout 1.0
    voice "n1102"
    "Alice led the way, and the whole party swam to the shore."

label chapter3:
    $ persistent.started_story = True
    scene black 
    call reset_camera
    voice "n1104"
    "{size=+40}Chapter III: \n{/size}A Caucus-Race and a Long Tale"

    # show all characters
    define muddy_eaglet_pos = 1104
    define muddy_eaglet_cam_pos = 1054
    define muddy_lory_pos = 540
    define muddy_duck_pos = 822
    define muddy_dodo_pos = 1950
    define muddy_dodo_cam_pos = 1940
    define muddy_alice_pos = 1386
    define muddy_mouse_pos = 1668
    define muddy_old_crab_pos = 2232
    define muddy_young_crab_pos = 2514
    define muddy_magpie_pos = 2796
    define muddy_magpie_cam_pos = 2780
    define muddy_canary_pos = 3078
    define muddy_canary_cam_pos = 3071

    define alice_scale_muddy = 0.35
    define mouse_muddy_scale = 0.3
    define lory_scale = 0.3
    define duck_scale = 0.4
    define dodo_scale = 0.7
    define eaglet_scale = 0.45
    define old_crab_scale = 0.3
    define young_crab_scale = 0.2
    define magpie_scale = 0.35
    define canary_scale = 0.2

    jump ch3_start
label ch3_scene_setup:
    scene bluesky at parallax(-4000)
    show hills at parallax(-4000)
    show mud at parallax(-300) as mud_safe: # safety mud layer behind river
        yoffset 550 xtile 5
    show water at parallax(-300):
        xpos 1.3 xtile 5 yoffset 110
        linear 10.0 xoffset 1460
        xoffset 0
        repeat
    show river at parallax(-300):
        xpos 1.3 xtile 5 yoffset 110
    show mud at parallax:
        yoffset 550 xtile 5
        xpos 1.3
    return
label ch3_setup:
    call ch3_scene_setup
    show eaglet at breathing:
        xpos muddy_eaglet_pos ypos 0.7 zoom eaglet_scale
    show lory at breathing:
        xpos muddy_lory_pos ypos 0.7 zoom lory_scale
    show duck at breathing:
        xpos muddy_duck_pos ypos 0.7 zoom duck_scale
    show dodo at breathing:
        xpos muddy_dodo_pos ypos 0.7 zoom dodo_scale
    show alice normal at breathing:
        xpos muddy_alice_pos ypos 0.7 zoom alice_scale_muddy
    show mouse at breathing:
        xpos muddy_mouse_pos ypos 0.7 zoom mouse_muddy_scale
    show old_crab at breathing:
        xpos muddy_old_crab_pos ypos 0.7 zoom old_crab_scale
    show young_crab at breathing:
        xpos muddy_young_crab_pos ypos 0.7 zoom young_crab_scale
    show magpie at breathing:
        xpos muddy_magpie_pos ypos 0.7 zoom magpie_scale
    show canary at breathing:
        xpos muddy_canary_pos ypos 0.7 zoom canary_scale
    return
label ch3_start:
    call ch3_setup
    camera:
        perspective True
        xpos center_offset xoffset -center_offset
        linear 20.0 xpos 2280


    play music "audio/rinne oak general store.mp3"

    voice "n1105"
    "They were indeed a queer-looking party that assembled on the bank—the birds with draggled feathers, the animals with their fur clinging close to them, and all dripping wet, cross, and uncomfortable."
    voice "n1106"
    "The first question of course was, how to get dry again: they had a consultation about this, and after a few minutes it seemed quite natural to Alice to find herself talking familiarly with them, as if she had known them all her life."
    voice "n1107"
    "Indeed, she had quite a long argument with the Lory, who at last turned sulky, and would only say:"

    define muddy_lory_ypos = 220
    camera: 
        ease cam_transition xpos muddy_lory_pos zpos -500 ypos muddy_lory_ypos
    voice "lory1"
    lory "I am older than you, and must know better."
    voice "n1108"
    "And this Alice would not allow without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said."

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos muddy_lory_ypos
    voice "n1109"
    "At last the Mouse, who seemed to be a person of authority among them, called out:"
    voice "mouse06"
    mouse "Sit down, all of you, and listen to me! I’ll soon make you dry enough!"
    voice "n1110"
    "They all sat down at once, in a large ring, with the Mouse in the middle."
    voice "n1111"
    "Alice kept her eyes anxiously fixed on it, for she felt sure she would catch a bad cold if she did not get dry very soon."
    voice "mouse07"
    mouse "Ahem!"
    voice "mouse08"
    mouse "Are you all ready? This is the driest thing I know."
    voice "mouse09"
    mouse "Silence all round, if you please!"
    voice "mouse10"
    mouse "'William the Conqueror, whose cause was favoured by the pope, was soon submitted to by the English, who wanted leaders, and had been of late much accustomed to usurpation and conquest." 
    voice "mouse11"
    mouse "Edwin and Morcar, the earls of Mercia and Northumbria—'"

    camera: 
        ease cam_transition xpos muddy_lory_pos zpos -500 ypos muddy_lory_ypos
    voice "lory2"
    lory "Ugh!"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos muddy_lory_ypos
    voice "mouse12"
    mouse "I beg your pardon!"
    voice "mouse13"
    mouse "Did you speak?"

    camera: 
        ease cam_transition xpos muddy_lory_pos zpos -500 ypos muddy_lory_ypos
    voice "lory3"
    lory "Not I!"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos muddy_lory_ypos
    voice "mouse14"
    mouse "I thought you did, —I proceed."
    voice "mouse15"
    mouse "'Edwin and Morcar, the earls of Mercia and Northumbria, declared for him: and even Stigand, the patriotic archbishop of Canterbury, found it advisable—'"

    camera: 
        ease cam_transition xpos muddy_duck_pos zpos -500 ypos 160
    voice "duck1"
    duck "Found what?"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "mouse16"
    mouse "Found it, of course you know what 'it' means."

    camera: 
        ease cam_transition xpos muddy_duck_pos  zpos -500 ypos 160
    voice "duck2"
    duck "I know what 'it' means well enough, when I find a thing, it’s generally a frog or a worm. The question is, what did the archbishop find?"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "n1112"
    "The Mouse did not notice this question, but hurriedly went on."

    voice "mouse17"
    mouse "'—found it advisable to go with Edgar Atheling to meet William and offer him the crown. William’s conduct at first was moderate. But the insolence of his Normans—'"
    voice "n1113"
    "It continued, turning to Alice as it spoke."
    voice "mouse18"
    mouse "How are you getting on now, my dear?"

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    show alice pout at breathing
    voice "alice084"
    alice "As wet as ever, it doesn’t seem to dry me at all."

    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo01"
    dodo "In that case, I move that the meeting adjourn, for the immediate adoption of more energetic remedies—"

    camera: 
        ease cam_transition xpos muddy_eaglet_cam_pos zpos -510 ypos -50
    voice "eaglet1"
    eaglet "Speak English! I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!"
    voice "n1114"
    "And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly."

    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo02"
    dodo "What I was going to say, was that the best thing to get us dry would be a Caucus-race."

    "..."

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    show alice thinking at breathing
    voice "alice085"
    alice "What is a Caucus-race?"

    voice "n1115"
    "Not that she wanted much to know, but the Dodo had paused as if it thought that somebody ought to speak, and no one else seemed inclined to say anything."

    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo03"
    dodo "Why, the best way to explain it is to do it."

    voice "n1116"
    "(And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it)"

    #show racetrack at Position(ypos = 0.65) onlayer screens
    voice "n1117"
    "First it marked out a race-course, in a sort of circle."
    voice "dodo04"
    dodo "The exact shape doesn’t matter."
    #hide racetrack onlayer screens

    camera: 
        ease cam_transition xpos 1805 zpos -135 ypos -130

    # place party members randomly
    show alice normal at breathing:
        ease cam_transition xpos 2000
    show mouse:
        ease cam_transition xpos 1900
    show duck:
        ease cam_transition xpos 2200
    show old_crab:
        ease cam_transition xpos 2100
    show young_crab:
        ease cam_transition xpos 2150

    voice "n1118"
    "And then all the party were placed along the course, here and there."

    show alice happy at breathing:
        ease 2.0 xoffset -1000
        ease 2.0 xoffset 0
        repeat
    show mouse:
        ease 1.6 xoffset -900
        ease 1.6 xoffset 0
        repeat
    show duck:
        xzoom -1.0
        ease 1.7 xoffset -1300 
        xzoom 1.0
        ease 1.7 xoffset 0
        repeat
    show old_crab:
        ease 2.2 xoffset -1200
        ease 2.2 xoffset 0
        repeat
    show young_crab:
        ease 1.5 xoffset -1200
        ease 1.5 xoffset 0
        repeat
    show dodo:
        xzoom 1.0
        ease 2.5 xoffset -800
        xzoom -1.0
        ease 2.5 xoffset 0
        repeat
    show eaglet:
        ease 2.0 xoffset 1000
        ease 2.0 xoffset 0
        repeat
    show lory:
        ease 1.8 xoffset 1200
        ease 1.8 xoffset 0
        repeat
    camera:
        ease 2.0 xpos muddy_eaglet_pos
        ease 2.0 xpos muddy_dodo_pos
        repeat

    voice "n1119"
    "There was no 'One, two, three, and away', but they began running when they liked, and left off when they liked, so that it was not easy to know when the race was over."
    "..."
    voice "n1120"
    "However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out:"

    # restore original positions
    call ch3_setup

    camera:
        xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo05"
    dodo "The race is over!"

    camera:
        ease cam_transition xpos muddy_alice_pos zpos 0 ypos 0
    voice "n1121"
    "And they all crowded round it, panting, and asking:"
    voice "everyone1"
    everyone "But who has won?"
    voice "n1122"
    "This question the Dodo could not answer without a great deal of thought, and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence."

    camera:
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo06"
    dodo "Everybody has won, and all must have prizes."

    camera:
        ease cam_transition xpos muddy_alice_pos zpos 0 ypos 0

    voice "everyone2"
    everyone "But who is to give the prizes?"

    camera:
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo07"
    dodo "Why, she, of course." 
    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos -130
    show alice surprised at breathing
    voice "n1123"
    "Said the Dodo, pointing to Alice with one finger; and the whole party at once crowded round her, calling out in a confused way:"

    camera:
        ease cam_transition xpos muddy_alice_pos zpos 0 ypos 0
    voice "everyone3"
    everyone "Prizes! Prizes!"

    show popup at popup onlayer screens
    show comfits at popup onlayer screens
    voice "n1124"
    "Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes."
    voice "n1125"
    "There was exactly one a-piece all round."
    hide popup onlayer screens
    hide comfits onlayer screens

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "mouse19"
    mouse "But she must have a prize herself, you know."

    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo08"
    dodo "Of course. What else have you got in your pocket?"
    voice "n1126"
    "The dodo turned to Alice."

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos -130
    show alice normal at breathing

    show popup at popup onlayer screens
    show thimble at popup onlayer screens 
    voice "alice086"
    alice "Only a thimble."
    hide thimble onlayer screens 
    hide popup onlayer screens

    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    voice "dodo09"
    dodo "Hand it over here."
    voice "n1127"
    "Then they all crowded round her once more, while the Dodo solemnly presented the thimble."
    camera: 
        ease cam_transition xpos muddy_dodo_cam_pos zpos -450 ypos -130
    show popup at popup onlayer screens
    show thimble at popup onlayer screens
    voice "dodo10"
    dodo "We beg your acceptance of this elegant thimble."
    voice "n1128"
    "And, when it had finished this short speech, they all cheered."
    voice "n1129"
    "Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could."
    hide thimble onlayer screens
    hide popup onlayer screens

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos -130
    voice "n1130"
    "The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back."

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "n1131"
    "However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more."

    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    voice "alice087"
    alice "You promised to tell me your history, you know."
    voice "alice088"
    alice "And why it is you hate—C and D."
    voice "n1132"
    "Alice added in a whisper, half afraid that it would be offended again."

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
 
    voice "mouse20"
    mouse "Mine is a long and a sad {b}tale{/b}!"
    
    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    voice "alice089"
    alice "It is a long {b}tail{/b}, certainly, but why do you call it sad?"
    voice "n1133"
    "She kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:—"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220

    voice "mouse21"
    mouse "{k=1}Fury said to a mouse, \n{space=260}That he met in the house.\n{space=460}‘Let us both go to law: \n{space=300} I will prosecute YOU. \n{space=100}—Come, I’ll take no denial; \n We must have a trial: \n{space=100}For really this morning \n{space=280}I’ve nothing to do.’"
    voice "mouse22"
    mouse "{space=320}Said the mouse to the cur, \n{space=260}‘Such a trial, \n{space=200}dear Sir, \n{space=20} With no jury or judge, \n {space=60} would be wasting our breath.’\n {space=220} ‘I’ll be judge, I’ll be jury’\n {space=100} Said cunning old Fury:\n ‘I’ll try the whole cause,\n {space=80} and condemn you to death.’"

    # book indents
    #mouse " {space=80} Fury said to a\n {space=60} mouse. That he\n {space=40} met in the\n {space=20} house.\n'Let us\n {space=20} both go to\n {space=40} law: I will\n {space=60} prosecute\n {space=80} YOU.—Come,\n {space=100} I’ll take no"
    #mouse " {space=120} denial; We\n {space=100} must have a\n {space=80} trial: For\n {space=60} really this\n {space=40} morning I’ve\n {space=20} nothing\nto do.'\n {space=20} Said the\n {space=40} mouse to the\n {space=60} cur, 'Such"
    #mouse " {space=80} a trial,\n {space=100} dear Sir,\n {space=120} With\n {space=100} no jury\n {space=80} or judge,\n {space=60} would be\n {space=40} wasting\n {space=20} our\n {space=40} breath.'\n {space=60} 'I’ll be"
    #mouse " {space=80} judge, I’ll\n {space=100} be jury'\n {space=120} Said\n {space=100} cunning\n {space=120} old Fury:\n {space=140} 'I’ll\n {space=120} try the\n {space=140} whole\n {space=160} cause,\n {space=180} and"
    #mouse " {space=160} condemn\n {space=140} you\n {space=120} to\n {space=140} death.'"
    voice "mouse23"
    mouse "You are not attending!"
    voice "mouse24"
    mouse "What are you thinking of?"

    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    show alice surprised at breathing
    voice "alice090"
    alice "I beg your pardon, you had got to the fifth bend, I think?"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "mouse25"
    mouse "I had not!" # cried the Mouse, sharply and very angrily.

    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    voice "alice091"
    alice "A knot!" # said Alice, always ready to make herself useful, and looking anxiously about her. 
    voice "alice092"
    alice "Oh, do let me help to undo it!"

    camera: 
        ease cam_transition xpos muddy_mouse_pos zpos -500 ypos 220
    voice "mouse26"
    mouse "I shall do nothing of the sort."
    show mouse:
        ease 1.0 xoffset 270
    voice "n1134"
    "The Mouse got up and walked away."
    voice "mouse27"
    mouse "You insult me by talking such nonsense!"

    camera:
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    voice "alice093"
    alice "I didn’t mean it! But you’re so easily offended, you know!"
    show mouse:
        ease 1.0 xoffset 400
    voice "n1135"
    "The Mouse only growled in reply."
    voice "alice094"
    alice "Please come back and finish your story!"
    #"All the others joined in chorus:"
    show mouse:
        ease 1.0 xoffset 600

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos 0 ypos 0
    voice "everyone4"
    everyone "Yes, please do!"
    voice "n1136"
    "But the Mouse only shook its head impatiently, and walked a little quicker."
    hide mouse

    camera: 
        ease cam_transition xpos muddy_lory_pos zpos -500 ypos muddy_lory_ypos
    voice "lory4"
    lory "What a pity it wouldn’t stay!"
    voice "n1137"
    "Sighed the Lory, as soon as it was quite out of sight; and an old Crab took the opportunity of saying to her daughter:"

    camera: 
        ease cam_transition xpos muddy_old_crab_pos zpos -500 ypos muddy_lory_ypos
    voice "old_crab1"
    old_crab "Ah, my dear! Let this be a lesson to you to never to lose your temper!"
    
    camera: 
        ease cam_transition xpos muddy_young_crab_pos zpos -500 ypos muddy_lory_ypos
    voice "young_crab1"
    young_crab "Hold your tongue, Ma! You’re enough to try the patience of an oyster!"

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    show alice normal at breathing
    voice "alice095"
    alice "I wish I had our Dinah here, I know I do!"
    voice "alice096"
    alice "She’d soon fetch it back!"

    camera: 
        ease cam_transition xpos muddy_lory_pos zpos -500 ypos muddy_lory_ypos
    voice "lory5"
    lory "And who is Dinah, if I might venture to ask the question?"

    camera: 
        ease cam_transition xpos muddy_alice_pos zpos -450 ypos 0
    show alice happy at breathing
    voice "alice097"
    alice "Dinah’s our cat. And she’s such a capital one for catching mice you can’t think! And oh, I wish you could see her after the birds! Why, she’ll eat a little bird as soon as look at it!"

    camera: 
        ease cam_transition xpos muddy_magpie_cam_pos zpos -535 ypos 165
    voice "n1138"
    "This speech caused a remarkable sensation among the party. Some of the birds hurried off at once: one old Magpie began wrapping itself up very carefully"
    show magpie at breathing:
        pause 4.0
        xzoom -1.0
        linear 1.0 xpos 4000
    voice "magpie1"
    magpie "I really must be getting home; the night-air doesn’t suit my throat!"
    hide magpie

    camera:
        ease cam_transition xpos muddy_canary_cam_pos zpos -550 ypos 275
    voice "n1139"
    "And a Canary called out in a trembling voice to its children:"
    voice "canary1"
    canary "Come away, my dears! It’s high time you were all in bed!"

    show young_crab:
        linear 2.0 xpos 4000
    show old_crab:
        linear 2.0 xpos 4000
    hide dodo
    hide eaglet
    hide lory
    hide duck

    camera: 
        ease 2.0 xpos muddy_alice_pos zpos -425 ypos -130
    voice "n1140"
    "On various pretexts they all moved off, and Alice was soon left alone."

    show alice pout at breathing
    voice "alice098"
    alice "(I wish I hadn’t mentioned Dinah!)"
    voice "alice099"
    alice "(Nobody seems to like her, down here, and I’m sure she’s the best cat in the world!)"
    voice "alice100"
    alice "(Oh, my dear Dinah! I wonder if I shall ever see you any more!)"
    show alice crying at breathing_crying
    voice "n1141"
    "And here poor Alice began to cry again, for she felt very lonely and low-spirited."
    voice "n1142"
    "In a little while, however, she again heard a little pattering of footsteps in the distance, and she looked up eagerly, half hoping that the Mouse had changed his mind, and was coming back to finish his story."

label chapter4:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1143"
    "{size=+40}Chapter IV: \n{/size}The Rabbit Sends in a Little Bill"
    call ch3_scene_setup
    camera:
        perspective True
    play music "audio/rinne oak general store.mp3" if_changed
    #jump ch4_forest
    #jump ch4_grass

    show alice pout at breathing:
        xpos 0.7 ypos 0.7 zoom alice_scale

    show rabbit normal at breathing:
        anchor (0.5, 1.0)
        zoom rabbit_scale
        ypos 0.8
        xpos 1.2
        ease 20.0 xpos -1.0

    voice "n1144"
    "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something." #; and she heard it muttering to itself:"
    voice "rabbit43"  # forgot this at first
    rabbit "*muttering* The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where can I have dropped them, I wonder?"
    voice "n1145"
    "Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen—everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely."

    show rabbit normal at breathing:
        xzoom -1.0
        ease 5.0 xpos 0.2 ypos 0.7
    voice "n1146"
    "Very soon the Rabbit noticed Alice, as she went hunting about." # , and called out to her in an angry tone"
    show alice surprised at breathing
    voice "rabbit04"
    rabbit "*angry* Why, Mary Ann, what are you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!"
    show alice surprised at breathing:
        linear 1.0 xpos 2.0
    voice "n1147"
    "And Alice was so much frightened that she ran off at once in the direction it pointed to, without trying to explain the mistake it had made."
    scene black
    voice "alice101"
    alice "(He took me for his housemaid. How surprised he’ll be when he finds out who I am! But I’d better take him his fan and gloves—that is, if I can find them)"

    scene rabbit_house:
        xalign 0.0
        linear 10.0 xalign 1.0
    voice "n1148"
    "As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name 'W. RABBIT' engraved upon it."
    voice "n1149"
    "She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves."

    scene rabbit_room:
        xalign 0.0
        linear 10.0 xalign 1.0
    voice "alice102"
    alice "(How queer it seems, to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!)"
    voice "n1150"
    "And she began fancying the sort of thing that would happen:"
    voice "alice103"
    alice "('Miss Alice! Come here directly, and get ready for your walk!' 'Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.')"
    voice "alice104"
    alice "(Only I don’t think, that they’d let Dinah stop in the house if it began ordering people about like that!)"

    show popup at popup onlayer screens
    show fan gloves at popup onlayer screens
    voice "n1151"
    "By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves:"
    hide fan gloves onlayer screens
    hide popup onlayer screens
    show alice excited at breathing:
        xpos 0.5 ypos 0.9 zoom alice_scale
    voice "n1152"
    "She took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass."
    play sound "sfx/cork.mp3"
    voice "n1153"
    "There was no label this time with the words 'DRINK ME', but nevertheless she uncorked it and put it to her lips."
    voice "alice105"
    alice "(I know something interesting is sure to happen, whenever I eat or drink anything; so I’ll just see what this bottle does)"
    voice "alice106"
    alice "(I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!)"

    show alice excited at breathing:
        pos (0.5, 0.9)
        anchor (0.5, 1.0)
        zoom alice_scale
        easeout 60.0 zoom 10.0
    voice "n1154"
    "It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken."
    voice "n1155"
    "She hastily put down the bottle."
    voice "alice107"
    alice "(That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk so much!)"

    show alice belly at breathing:
        xpos 0.7 ypos 1.0 zoom 1.9
    voice "n1156"
    "Alas! it was too late to wish that! She went on growing, and growing, and very soon had to kneel down on the floor:"
    voice "n1157"
    "In another minute there was not even room for this, and she tried the effect of lying down with one elbow against the door, and the other arm curled round her head."
    voice "n1158"
    "Still she went on growing, and, as a last resource, she put one arm out of the window, and one foot up the chimney."

    voice "alice108"
    alice "(Now I can do no more, whatever happens. What will become of me?)"

    # stop growing, show at max w/ breathing
    voice "n1159"
    "Luckily for Alice, the little magic bottle had now had its full effect, and she grew no larger:"
    voice "n1160"
    "Still it was very uncomfortable, and, as there seemed to be no sort of chance of her ever getting out of the room again, no wonder she felt unhappy."
    voice "alice109"
    alice "(It was much pleasanter at home, when one wasn’t always growing larger and smaller, and being ordered about by mice and rabbits)"
    voice "alice110"
    alice "(I almost wish I hadn’t gone down that rabbit-hole—and yet—and yet—it’s rather curious, you know, this sort of life!)"
    voice "alice111"
    alice "(I do wonder what can have happened to me! When I used to read fairy-tales, I fancied that kind of thing never happened, and now here I am in the middle of one!)"
    voice "alice112"
    alice "(There ought to be a book written about me, that there ought! And when I grow up, I’ll write one—but I’m grown up now, at least there’s no room to grow up any more here)"
    voice "alice113"
    alice "(But then, shall I never get any older than I am now? That’ll be a comfort, one way—never to be an old woman—but then—always to have lessons to learn! Oh, I shouldn’t like that!)"
    voice "alice114"
    alice "(Oh, you foolish Alice!)"
    voice "alice115"
    alice "(How can you learn lessons in here?)"
    voice "alice116"
    alice "(Why, there’s hardly room for you, and no room at all for any lesson-books!)"
    voice "n1161"
    "And so she went on, taking first one side and then the other, and making quite a conversation of it altogether; but after a few minutes she heard a voice outside, and stopped to listen."

    voice "rabbit05"
    rabbit "Mary Ann! Mary Ann!"
    voice "rabbit06"
    rabbit "Fetch me my gloves this moment!"

    play sound "sfx/upstairs.mp3"
    voice "n1162"
    "Then came a little pattering of feet on the stairs."
    voice "n1163"
    "Alice knew it was the Rabbit coming to look for her, and she trembled till she shook the house, quite forgetting that she was now about a thousand times as large as the Rabbit, and had no reason to be afraid of it."

    play sound "sfx/door_closed.mp3"
    voice "n1164"
    "Presently the Rabbit came up to the door, and tried to open it; but, as the door opened inwards, and Alice’s elbow was pressed hard against it, that attempt proved a failure."
    voice "rabbit07"
    rabbit "Then I’ll go round and get in at the window."
    voice "alice117"
    alice "(That you won’t!)"
    voice "n1165"
    "After waiting till she fancied she heard the Rabbit just under the window."
    play sound "sfx/snatch.mp3"
    voice "n1166"
    "She suddenly spread out her hand, and made a snatch in the air."
    play sound "sfx/shatter.mp3"
    voice "n1167"
    "She did not get hold of anything, but she heard a little shriek and a fall, and a crash of broken glass, from which she concluded that it was just possible it had fallen into a cucumber-frame, or something of the sort."
    voice "n1168"
    "Next came an angry voice—"
    voice "rabbit08"
    rabbit "Pat! Pat! Where are you?"
    voice "n1169"
    "And then a voice she had never heard before:"
    voice "pat1"
    pat "Sure then I’m here! Digging for apples, yer honour!"
    voice "rabbit09"
    rabbit "Digging for apples, indeed!"
    voice "rabbit10"
    rabbit "Here! Come and help me out of this!"
    "..."
    play sound "sfx/shatter.mp3"
    "(Sounds of more broken glass)"
    voice "rabbit11"
    rabbit "Now tell me, Pat, what’s that in the window?"
    voice "pat2"
    pat "Sure, it’s an arrumm, yer honour!"
    voice "rabbit12"
    rabbit "An arm, you goose! Who ever saw one that size? Why, it fills the whole window!"
    voice "pat3"
    pat "Sure, it does, yer honour: but it’s an arm for all that."
    voice "rabbit13"
    rabbit "Well, it’s got no business there, at any rate: go and take it away!"
    voice "n1170"
    "There was a long silence after this, and Alice could only hear whispers now and then; such as:"
    voice "pat4"
    pat "Sure, I don’t like it, yer honour, at all, at all!"
    voice "rabbit14"
    rabbit "Do as I tell you, you coward!"
    play sound "sfx/snatch.mp3"
    voice "n1171"
    "And at last she spread out her hand again, and made another snatch in the air."

    play sound "sfx/shatter.mp3"
    voice "n1172"
    "This time there were two little shrieks, and more sounds of broken glass."
    voice "alice118"
    alice "(What a number of cucumber-frames there must be!)"
    voice "alice119"
    alice "(I wonder what they’ll do next! As for pulling me out of the window, I only wish they could! I’m sure I don’t want to stay in here any longer!)"
    voice "n1173"
    "She waited for some time without hearing anything more: at last came a rumbling of little cartwheels, and the sound of a good many voices all talking together:"
    voice "a01"
    anon "Where’s the other ladder?" # A
    voice "b01"
    anon "Why, I hadn’t to bring but one; Bill’s got the other." # B
    voice "a02"
    anon "Bill! fetch it here, lad!" # A
    voice "b02"
    anon "Here, put 'em up at this corner." # B
    voice "a03"
    anon "No, tie 'em together first—they don’t reach half high enough yet" # A
    voice "c01"
    anon "Oh! they’ll do well enough; don’t be particular." # C
    voice "a04"
    anon "Here, Bill! catch hold of this rope." # A
    voice "c02"
    anon "Will the roof bear?" # C
    voice "b03"
    anon "Mind that loose slate." # B
    voice "a05"
    anon "Oh, it’s coming down! Heads below!" # A

    play sound "sfx/shatter.mp3"
    "..."
    voice "a06"
    anon "Now, who did that?" # A
    voice "b04"
    anon "It was Bill, I fancy." # B
    voice "c03"
    anon "Who’s to go down the chimney?" # C
    voice "b05"
    anon "Nay, I shan’t! You do it!" # B
    voice "c04"
    anon "That I won’t, then!" # C
    voice "a07"
    anon "Bill’s to go down." # A
    voice "b06"
    anon "Here, Bill! the master says you’re to go down the chimney!" # B
    voice "alice120"
    alice "(Oh! So Bill’s got to come down the chimney, has he?)"
    voice "alice121"
    alice "(Shy, they seem to put everything upon Bill! I wouldn’t be in Bill’s place for a good deal: this fireplace is narrow, to be sure; but I think I can kick a little!)"
    voice "n1174"
    "She drew her foot as far down the chimney as she could, and waited till she heard a little animal (she couldn’t guess of what sort it was) scratching and scrambling about in the chimney close above her:"
    voice "alice122"
    alice "(This is Bill!)"
    play sound "sfx/snatch.mp3"
    voice "n1175"
    "She gave one sharp kick, and waited to see what would happen next."
    voice "n1176"
    "The first thing she heard was a general chorus of:"
    voice "everyone5"
    everyone "There goes Bill!"
    voice "n1177"
    "Then the Rabbit’s voice along—"
    voice "rabbit15"
    rabbit "Catch him, you by the hedge!"
    play sound "sfx/shatter.mp3"
    "..."
    voice "n1178"
    "Then silence, and then another confusion of voices—"
    voice "a08"
    anon "Hold up his head." # A
    voice "b07"
    anon "Brandy now." # B
    voice "c05"
    anon "Don’t choke him." # C
    voice "a09"
    anon "How was it, old fellow? What happened to you? Tell us all about it!" # A
    voice "n1179"
    "Last came a little feeble, squeaking voice:"
    voice "bill1"
    bill "Well, I hardly know—No more, thank ye; I’m better now—but I’m a deal too flustered to tell you—all I know is, something comes at me like a Jack-in-the-box, and up I goes like a sky-rocket!"
    voice "a10"
    anon "So you did, old fellow!" # A
    voice "rabbit16"
    rabbit "We must burn the house down!"
    voice "n1180"
    "Alice called out as loud as she could:"
    voice "alice123"
    alice "If you do, I’ll set Dinah at you!"

    "..."
    voice "n1181"
    "There was a dead silence instantly."
    voice "alice124"
    alice "(I wonder what they will do next! If they had any sense, they’d take the roof off)"
    voice "n1182"
    "After a minute or two, they began moving about again."
    voice "rabbit17"
    rabbit "A barrowful will do, to begin with."
    voice "alice125"
    alice "(A barrowful of what?)"
    voice "n1183"
    "She had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face."
    voice "alice126"
    alice "(I’ll put a stop to this)"
    #"she said to herself, and shouted out, "
    voice "alice127"
    alice "You’d better not do that again!"
    voice "n1184"
    "Which produced another dead silence."

    show popup at popup onlayer screens
    show pebble_cake at popup onlayer screens
    voice "n1185"
    "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the floor, and a bright idea came into her head."
    voice "alice128"
    alice "(If I eat one of these cakes, it’s sure to make some change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose)"
    hide pebble_cake onlayer screens
    hide popup onlayer screens

    show alice at breathing:
        easein 10.0 zoom 1.0
    voice "n1186"
    "So she swallowed one of the cakes, and was delighted to find that she began shrinking directly."

    scene rabbit_house:
        xalign 0.2 zoom 1.3 yalign 1.0

    show bill guinea at breathing:
        pos (0.25, 0.92) zoom 0.8
    show alice surprised at breathing:
        pos (0.85, 0.79) zoom alice_scale
    voice "n1187"
    "As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside."
    voice "n1188"
    "The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle."

    show alice at breathing:
        linear 1.0 xpos 2.0
    voice "n1189"
    "They all made a rush at Alice the moment she appeared; but she ran off as hard as she could, and soon found herself safe in a thick wood."

    jump ch4_forest

label setup_forest:
    scene black:
        xtile 10 xoffset -1000
    show trees at parallax(-900) as trees4:
        matrixcolor BrightnessMatrix(-0.3)
        xoffset 1310 xtile 10 yoffset -400
    show trees at parallax(-900) as trees3:
        matrixcolor BrightnessMatrix(-0.2)
        xoffset 550 xtile 10 yoffset -400
    show trees at parallax(-600) as trees2:
        matrixcolor BrightnessMatrix(-0.1)
        xoffset 200 xtile 10 yoffset -400
    show trees at parallax(-300) as trees1:
        xoffset 900 xtile 10 yoffset -400
    show grass at parallax:
        matrixcolor BrightnessMatrix(-0.25)
        yoffset 550 xoffset 900 xtile 10

    return

label ch4_forest:
    call setup_forest
    camera:
        perspective True
        xpos -215 ypos 490 zpos -500 xoffset 0

    show alice thinking at breathing:
        pos (0.3, 0.85) zoom 0.14
    show thistle:
        pos (0.10, 0.85)
        anchor (0.5, 1.0)
        zoom 0.3
    show puppy:
        pos (0.89, 0.85)
        anchor (0.5, 1.0)
        zoom 1.0
    voice "alice129"
    alice "The first thing I’ve got to do, is to grow to my right size again; and the second thing is, to find my way into that lovely garden."
    voice "alice130"
    alice "I think that will be the best plan."
    voice "n1190"
    "It sounded an excellent plan, no doubt, and very neatly and simply arranged; the only difficulty was, that she had not the smallest idea how to set about it; and while she was peering about anxiously among the trees, a little sharp bark just over her head made her look up in a great hurry."

    camera:
        linear 2.0 xpos 0 ypos 425 zpos -335
    #scene huge_dog # todo replace with normal sized dog
    play sound "sfx/bark.mp3"
    show alice surprised at breathing
    voice "n1191"
    "An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her."
    voice "alice131"
    alice "Poor little thing!"
    voice "n1192"
    "She tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing."

    play sound "sfx/bark.mp3"
    show puppy:
        easein 1.0 yoffset -200
        easeout 1.0 yoffset 0
    voice "n1193"
    "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air off all its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it."
    camera:
        linear 2.0 xpos -275 ypos 425 zpos -335
    show alice at breathing:
        linear 0.5 xpos 0.05
    show puppy:
        yoffset 0
        linear 0.7 xpos 0.7
        linear 0.7 xpos 0.38 ypos 0.75 zrotate -40
        linear 0.7 xpos 0.0 ypos 0.75 zrotate -80
        linear 0.7 xpos -0.42 ypos 0.75 zrotate -120
        linear 0.7 xpos -0.71 ypos 0.75 zrotate -160
        linear 0.2 xpos -0.71 ypos 0.75 zrotate 0 xzoom -1.0
    voice "n1194"
    "Then Alice dodged behind a great thistle, to keep herself from being run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it."
    show alice at breathing:
        linear 0.5 xpos 0.17
    voice "n1195"
    "Then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again."
    camera:
        linear 2.0 xpos -560 ypos 425 zpos -335
    show puppy:
        ypos 0.85 xpos -0.66 xzoom -1.0 zrotate 0 
        ease 1.0 xpos -0.56
        ease 1.0 xpos -0.46
        ease 1.0 xpos -0.36
        easeout 1.0 xpos -0.66
        repeat 3
    play sound "sfx/bark.mp3"
    #queue sound "sfx/bark.mp3"
    #queue sound "sfx/bark.mp3"
    voice "n1196"
    "Then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way off, panting, with its tongue hanging out of its mouth, and its great eyes half shut."
    voice "n1197"
    "This seemed to Alice a good opportunity for making her escape; so she set off at once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance."
label ch4_grass:

    # hacky way to save setup for next chapter
    call setup_caterpillar
    jump ch4_caterpillar

label setup_caterpillar:
    scene sky:
        xpos 0.0 zpos -6000 zzoom True


    show soil:
        anchor (0.0, 0.0)
        xrotate 90 yoffset -512 zpos -1100 ypos 1.0 

    show blades at windy_no_anchor:
        anchor (0.5, 1.0)
        pos (800, 1.0)
        zpos -1100
        zoom 0.5

    show alice normal at breathing:
        pos (800, 1.0) zoom 0.22 zpos -1000 

    show buttercup at windy_no_anchor:
        anchor (0.5, 1.0)
        pos (650, 1.0)
        zoom 0.3
        zpos -950

    show caterpillar at breathing:
        pos (1090, 0.88) zoom 0.3 zpos -900

    show mushroom at Position(xpos = 1090, ypos = 1.0):
        anchor (0.5, 1.0)
        zoom 0.45
        zpos -880
    show blades as blades2 at windy_no_anchor:
        anchor (0.5, 1.0)
        pos (800, 1.14)
        zpos -860
        zoom 0.5
    return
label ch4_caterpillar:

    camera:
        perspective True
        xpos 730 ypos 815 zpos -1460 xoffset -center_offset
    voice "alice132"
    alice "And yet what a dear little puppy it was!"
    voice "n1198"
    "She leant against a buttercup to rest herself, and fanned herself with one of the leaves:"
    voice "alice133"
    alice "I should have liked teaching it tricks very much, if—if I’d only been the right size to do it!"
    voice "alice134"
    alice "Oh dear! I’d nearly forgotten that I’ve got to grow up again!"
    voice "alice135"
    alice "Let me see—how is it to be managed?"
    voice "alice136"
    alice "I suppose I ought to eat or drink something or other; but the great question is, what?"
    voice "n1199"
    "The great question certainly was, what?"

    camera:
        linear 4.0 xpos 1000 
    voice "n1200"
    "Alice looked all round her at the flowers and the blades of grass, but she did not see anything that looked like the right thing to eat or drink under the circumstances."


    voice "n1201"
    "There was a large mushroom growing near her, about the same height as herself; and when she had looked under it, and on both sides of it, and behind it, it occurred to her that she might as well look and see what was on the top of it."

    camera:
        linear 4.0 xpos 1000 ypos 635 zpos -1275
    voice "n1202"
    "She stretched herself up on tiptoe, and peeped over the edge of the mushroom, and her eyes immediately met those of a large caterpillar, that was sitting on the top with its arms folded, quietly smoking a long hookah, and taking not the smallest notice of her or of anything else."

label chapter5:
    $ persistent.started_story = True
    scene black
    camera: # revert camera
        perspective False
        zpos 0
    voice "n1203"
    "{size=+40}Chapter V: \n{/size}Advice from a Caterpillar"

    play music "audio/rinne sad.mp3" fadein 1.0 fadeout 1.0

    #jump ch5_sky

    call setup_caterpillar

    camera:
        perspective True
        xpos 1000 ypos 635 zpos -1275 xoffset -center_offset
    voice "n1204"
    "The Caterpillar and Alice looked at each other for some time in silence: at last the Caterpillar took the hookah out of its mouth, and addressed her in a languid, sleepy voice."

    voice "caterpillar01"
    caterpillar "Who are you?"
    voice "n1205"
    "This was not an encouraging opening for a conversation."
    show alice surprised at breathing
    voice "alice137"
    alice "I—I hardly know, sir, just at present—at least I know who I was when I got up this morning, but I think I must have been changed several times since then."

    voice "caterpillar02"
    caterpillar "What do you mean by that?"
    voice "caterpillar03"
    caterpillar "Explain yourself!"
    voice "alice138"
    alice "I can’t explain myself, I’m afraid, sir, because I’m not myself, you see."

    voice "caterpillar04"
    caterpillar "I don’t see."
    voice "alice139"
    alice "I’m afraid I can’t put it more clearly, for I can’t understand it myself to begin with; and being so many different sizes in a day is very confusing."

    voice "caterpillar05"
    caterpillar "It isn’t."
    show alice joking at breathing
    voice "alice140"
    alice "Well, perhaps you haven’t found it so yet, but when you have to turn into a chrysalis—you will some day, you know—and then after that into a butterfly, I should think you’ll find it a little queer, won’t you?"

    voice "caterpillar06"
    caterpillar "Not a bit."
    show alice normal at breathing
    voice "alice141"
    alice "Well, perhaps your feelings may be different. All I know is, it would feel very queer to me."

    voice "caterpillar07"
    caterpillar "You!" # said the Caterpillar contemptuously.
    voice "caterpillar08"
    caterpillar "Who are you?"
    show alice disturbed at breathing
    voice "n1206"
    "Which brought them back again to the beginning of the conversation."
    voice "n1207"
    "Alice felt a little irritated at the Caterpillar’s making such very short remarks, and she drew herself up and said, very gravely:"
    voice "alice142"
    alice "I think, you ought to tell me who you are, first."

    voice "caterpillar09"
    caterpillar "Why?"

    show alice at breathing:
        zpos -1000
        linear 2.0 xoffset -400
    voice "n1208"
    "Here was another puzzling question; and as Alice could not think of any good reason, and as the Caterpillar seemed to be in a very unpleasant state of mind, she turned away."

    voice "caterpillar10"
    caterpillar "Come back!"
    voice "caterpillar11"
    caterpillar "I’ve something important to say!"

    show alice normal at breathing:
        zpos -1000
        linear 2.0 xoffset 0
    voice "n1209"
    "This sounded promising, certainly: Alice turned and came back again."
    voice "caterpillar12"
    caterpillar "Keep your temper."

    "..."
    show alice disturbed at breathing
    voice "alice143"
    alice "Is that all?"
    voice "n1210"
    "Alice swallowed down her anger as well as she could."
    voice "caterpillar13"
    caterpillar "No."
    show alice thinking at breathing
    voice "n1211"
    "Alice thought she might as well wait, as she had nothing else to do, and perhaps after all it might tell her something worth hearing."
    play sound "voice/caterpillar_vape.mp3"
    "..."
    voice "n1212"
    "For some minutes it puffed away without speaking, but at last it unfolded its arms, took the hookah out of its mouth again."
    voice "caterpillar14"
    caterpillar "So you think you’re changed, do you?"
    voice "alice144"
    alice "I’m afraid I am, sir."
    voice "alice145"
    alice "I can’t remember things as I used—and I don’t keep the same size for ten minutes together!"

    voice "caterpillar15"
    caterpillar "Can’t remember what things?"
    voice "alice146"
    alice "Well, I’ve tried to say 'How doth the little busy bee', but it all came different!"

    voice "caterpillar16"
    caterpillar "Repeat, 'You are old, Father William.'"
    voice "n1213"
    "Alice folded her hands, and began:"
    voice "alice147"
    alice "'You are old, Father William',\nthe young man said,\n{space=30}And your hair has become very white;\nAnd yet you incessantly stand on your head—\n{space=30}Do you think, at your age, it is right?'"
    voice "alice148"
    alice "'In my youth',\nFather William replied to his son,\n{space=30}'I feared it might injure the brain;\nBut, now that I’m perfectly sure I have none,\n{space=30}Why, I do it again and again.'"
    voice "alice149"
    alice "'You are old', said the youth,\n'as I mentioned before,\n{space=30}And have grown most uncommonly fat;\nYet you turned a back-somersault\nin at the door—\n{space=30}Pray, what is the reason of that?'"
    voice "alice150"
    alice "'In my youth', said the sage,\nas he shook his grey locks,\n{space=30}'I kept all my limbs very supple\nBy the use of this ointment—\none shilling the box—\n{space=30}Allow me to sell you a couple?'"
    voice "alice151"
    alice "'You are old', said the youth,\n'and your jaws are too weak\n{space=30}For anything tougher than suet;\nYet you finished the goose,\nwith the bones and the beak—\n{space=30}Pray how did you manage to do it?'"
    voice "alice152"
    alice "'In my youth', said his father, \n'I took to the law,\n{space=30}And argued each case with my wife;\nAnd the muscular strength, \nwhich it gave to my jaw,\n{space=30}Has lasted the rest of my life.'"
    voice "alice153"
    alice "'You are old', said the youth, \n'one would hardly suppose\n{space=30}That your eye was as steady as ever;\nYet you balanced an eel \non the end of your nose—\n{space=30}What made you so awfully clever?'"
    voice "alice154"
    alice "'I have answered three questions, \nand that is enough',\n{space=30}Said his father; 'don’t give yourself airs!\nDo you think I can listen all day to such stuff?\n{space=30}Be off, or I’ll kick you down stairs!'"

    voice "caterpillar17"
    caterpillar "That is not said right."
    show alice surprised at breathing
    voice "alice155"
    alice "Not quite right, I’m afraid." # said alice timidly;
    voice "alice156"
    alice "Some of the words have got altered."

    voice "caterpillar18"
    caterpillar "It is wrong from beginning to end."
    show alice normal at breathing
    "..."
    voice "n1214"
    "And there was silence for some minutes."
    voice "caterpillar19"
    caterpillar "What size do you want to be?"
    show alice joking at breathing
    voice "alice157"
    alice "Oh, I’m not particular as to size, only one doesn’t like changing so often, you know."
    voice "caterpillar20"
    caterpillar "I don’t know."
    show alice thinking at breathing
    voice "n1215"
    "Alice said nothing: she had never been so much contradicted in all her life before, and she felt that she was losing her temper."
    voice "caterpillar21"
    caterpillar "Are you content now?"
    show alice disturbed at breathing 
    voice "alice158"
    alice "Well, I should like to be a little larger, sir, if you wouldn’t mind."
    voice "alice159"
    alice "Three inches is such a wretched height to be."
    voice "caterpillar22"
    caterpillar "It is a very good height indeed!"
    voice "n1216"
    "Said the Caterpillar angrily, rearing itself upright as it spoke (it was exactly three inches high)"
    show alice thinking at breathing
    voice "alice160"
    alice "But I’m not used to it!"
    voice "n1217"
    "Pleaded poor Alice in a piteous tone. And she thought of herself:"
    voice "alice161"
    alice "(I wish the creatures wouldn’t be so easily offended!)"
    voice "caterpillar23"
    caterpillar "You’ll get used to it in time."
    play sound "voice/caterpillar_vape.mp3"
    voice "n1218"
    "The caterpillar put the hookah into its mouth and began smoking again."
    voice "n1219"
    "This time Alice waited patiently until it chose to speak again."

    play sound "<silence 2.0>"
    queue sound "voice/caterpillar_yawn.mp3"
    voice "n1220"
    "In a minute or two the Caterpillar took the hookah out of its mouth and yawned once or twice, and shook itself."

    show caterpillar at breathing:
        zpos -900
        linear 2.0 ypos 1.0
        linear 20.0 zpos -1200
    voice "n1221"
    "Then it got down off the mushroom, and crawled away in the grass."
    voice "caterpillar24"
    caterpillar "One side will make you grow taller, and the other side will make you grow shorter."
    voice "alice162"
    alice "One side of what? The other side of what?"
    voice "caterpillar25"
    caterpillar "Of the mushroom."
    voice "n1222"
    "In another moment it was out of sight."

    hide caterpillar
    voice "n1223"
    "Alice remained looking thoughtfully at the mushroom for a minute, trying to make out which were the two sides of it; and as it was perfectly round, she found this a very difficult question."
    voice "n1224"
    "However, at last she stretched her arms round it as far as they would go, and broke off a bit of the edge with each hand."

    camera:
        linear 0.5 xpos 800 ypos 815 zpos -1500
    show alice excited at breathing
    voice "alice163"
    alice "And now which is which?"
    voice "n1225"
    "She nibbled a little of the right-hand bit to try the effect:"

    show alice excited at breathing:
        zpos -1000
        easein_expo 10.0 yzoom 0.1
    voice "n1226"
    "The next moment she felt a violent blow underneath her chin: it had struck her foot!"


    voice "n1227"
    "She was a good deal frightened by this very sudden change, but she felt that there was no time to be lost, as she was shrinking rapidly; so she set to work at once to eat some of the other bit."
    voice "n1228"
    "Her chin was pressed so closely against her foot, that there was hardly room to open her mouth; but she did it at last, and managed to swallow a morsel of the lefthand bit."
    voice "alice164"
    alice "Come, my head’s free at last!"
    show alice normal at breathing:
        zoom 0.2
        zpos -1000
        yzoom 0.1
        easeout_expo 10.0 yzoom 5.0
    voice "n1229"
    "Alice was delighted, which changed into alarm in another moment, when she found that her shoulders were nowhere to be found: all she could see, when she looked down, was an immense length of neck, which seemed to rise like a stalk out of a sea of green leaves that lay far below her."

    # switch scene to sky
label ch5_sky:

    play music "audio/rinne alice.mp3" fadein 1.0 fadeout 1.0

    scene sky:
        # center sky
        anchor (0.5, 0.5)
        xpos 0.5 ypos 0.5
        zoom 1.1
    camera:
        perspective True
        xpos 0 ypos 0 zpos 0 xoffset 0


    show cloud as cloud1:
        anchor (0.5, 0.5)
        xpos 0.0 ypos 0.2 zpos -1200

    show cloud as cloud2:
        anchor (0.5, 0.5)
        xpos 1.0 ypos 0.0 zpos -800

    show cloud as cloud3:
        anchor (0.5, 0.5)
        xpos 1.2 ypos 0.7 zpos -600
    voice "alice165"
    alice "What can all that green stuff be?"
    
    camera:
        easein 3.0 zrotate -5.0 xpos -30 ypos 30
        easeout 3.0 zrotate 0.0 xpos 0 ypos 0
        easein 3.0 zrotate 5.0 xpos 30 ypos 30
        easeout 3.0 zrotate 0.0 ypos 0 ypos 0
        repeat
    voice "alice166"
    alice "And where have my shoulders got to?"
    voice "alice167"
    alice "And oh, my poor hands, how is it I can’t see you?"
    voice "n1230"
    "She was moving them about as she spoke, but no result seemed to follow, except a little shaking among the distant green leaves."
    voice "n1231"
    "As there seemed to be no chance of getting her hands up to her head, she tried to get her head down to them, and was delighted to find that her neck would bend about easily in any direction, like a serpent."

    show pigeon:
        zpos -1400 xpos 2.0
        easein 8.0 zpos 0.0 xpos 0.0

    show angry at angrily:
        zpos -1400 xpos 2.0
        xoffset 525 yoffset 478
        easein 8.0 zpos 0.0 xpos 0.0

    voice "n1232"
    "She had just succeeded in curving it down into a graceful zigzag, and was going to dive in among the leaves, which she found to be nothing but the tops of the trees under which she had been wandering, when a sharp hiss made her draw back in a hurry: a large pigeon had flown into her face, and was beating her violently with its wings."

    voice "pigeon01"
    pigeon "Serpent!"
    voice "alice168"
    alice "I’m not a serpent! Let me alone!"

    voice "pigeon02"
    pigeon "Serpent, I say again!"
    voice "pigeon03"
    pigeon "I’ve tried every way, and nothing seems to suit them!"
    voice "alice169"
    alice "I haven’t the least idea what you’re talking about."
    voice "pigeon04"
    pigeon "I’ve tried the roots of trees, and I’ve tried banks, and I’ve tried hedges, but those serpents! There’s no pleasing them!"
    voice "n1233"
    "Alice was more and more puzzled, but she thought there was no use in saying anything more till the pigeon had finished."
    voice "pigeon05"
    pigeon "As if it wasn’t trouble enough hatching the eggs, but I must be on the look-out for serpents night and day!"
    voice "pigeon06"
    pigeon "Why, I haven’t had a wink of sleep these three weeks!"
    voice "alice170"
    alice "I’m very sorry you’ve been annoyed."
    voice "pigeon07"
    pigeon "And just as I’d taken the highest tree in the wood, and just as I was thinking I should be free of them at last, they must needs come wriggling down from the sky! Ugh, Serpent!" # ontinued the Pigeon, raising its voice to a shriek
    voice "alice171"
    alice "But I’m not a serpent, I tell you!"
    voice "alice172"
    alice "I’m a—I’m a—"
    voice "pigeon08"
    pigeon "Well! What are you?"
    voice "pigeon09"
    pigeon "I can see you’re trying to invent something!"
    voice "alice173"
    alice "I—I’m a little girl..."
    voice "n1234"
    "Said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day."
    voice "pigeon10"
    pigeon "A likely story indeed!"
    voice "pigeon11"
    pigeon "I’ve seen a good many little girls in my time, but never one with such a neck as that!"
    voice "pigeon12"
    pigeon "No, no! You’re a serpent; and there’s no use denying it."
    voice "pigeon13"
    pigeon "I suppose you’ll be telling me next that you never tasted an egg!"
    voice "alice174"
    alice "I have tasted eggs, certainly, but little girls eat eggs quite as much as serpents do, you know."
    voice "pigeon14"
    pigeon "I don’t believe it, but if they do, why then they’re a kind of serpent, that’s all I can say."
    voice "n1235"
    "This was such a new idea to Alice, that she was quite silent for a minute or two."
    "..."
    voice "pigeon15"
    pigeon "You’re looking for eggs, I know that well enough; and what does it matter to me whether you’re a little girl or a serpent?"
    voice "alice175"
    alice "It matters a good deal to me, but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want yours: I don’t like them raw."
    voice "pigeon16"
    pigeon "Well, be off, then!"
    voice "n1236"
    "Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it."
    voice "n1237"
    "After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling first at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height."

    call setup_forest
    call reset_camera
    camera:
        perspective True
        xpos 0.5 xoffset -center_offset zrotate 0

    #stop music fadeout 1.0
    play music "audio/rinne song of little birds.mp3" fadein 1.0 fadeout 1.0
    voice "n1238"
    "It was so long since she had been anything near the right size, that it felt quite strange at first; but she got used to it in a few minutes, and began talking to herself, as usual."

    show alice happy at breathing:
        pos (0.5, 0.9) zoom 1.0
    voice "alice176"
    alice "Come, there’s half my plan done now!"
    voice "alice177"
    alice "How puzzling all these changes are!" 
    voice "alice178"
    alice "I’m never sure what I’m going to be, from one minute to another!"
    voice "alice179"
    alice "However, I’ve got back to my right size: the next thing is, to get into that beautiful garden—how is that to be done, I wonder?"
    
    
    show alice normal at breathing
    voice "n1239"
    "She came suddenly upon an open place, with a little house in it about four feet high."
    voice "alice180"
    alice "Whoever lives there, it’ll never do to come upon them this size: why, I should frighten them out of their wits!"
    show alice at breathing:
        linear 5.0 zoom 0.5
    voice "n1240"
    "So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high."

label chapter6:


    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1241"
    "{size=+40}Chapter VI: \n{/size}Pig and Pepper"

    play music "audio/rinne song of little birds.mp3" if_changed

    call setup_forest

    show footmen_fish at breathing:
        pos (-0.5, 0.9) zoom 0.5
        linear 4.0 xpos 0.3

    camera:
        perspective True
        xpos 0.5 xoffset -center_offset

    voice "n1242"
    "For a minute or two she stood looking at the house, and wondering what to do next, when suddenly a footman in livery came running out of the wood—(she considered him to be a footman because he was in livery: otherwise, judging by his face only, she would have called him a fish)—and rapped loudly at the door with his knuckles."

    play sound "sfx/knockknockknock.mp3"
    show footmen_frog at breathing:
        pos (0.7, 0.9) zoom 0.5
    
    voice "n1243"
    "It was opened by another footman in livery, with a round face, and large eyes like a frog; and both footmen, Alice noticed, had powdered hair that curled all over their heads."
    voice "n1244"
    "She felt very curious to know what it was all about, and crept a little way out of the wood to listen."
    voice "n1245"
    "The Fish-Footman began by producing from under his arm a great letter, nearly as large as himself, and this he handed over to the other, saying, in a solemn tone:"
    voice "fishfoot1"
    fishfoot "For the Duchess. An invitation from the Queen to play croquet."
    voice "n1246"
    "The Frog-Footman repeated, in the same solemn tone, only changing the order of the words a little:"
    voice "frogfoot1"
    frogfoot "From the Queen. An invitation for the Duchess to play croquet."
    
    # remove animations
    hide footmen_fish
    hide footmen_frog
    show footmen_fish:
        anchor (0.5, 1.0)
        xpos 0.3 ypos 0.9 zoom 0.5
        zrotate 20

    show footmen_frog:
        anchor (0.5, 1.0)
        xpos 0.7 ypos 0.9 zoom 0.5
        zrotate -20

    voice "n1247"
    "Then they both bowed low, and their curls got entangled together."
    voice "n1248"
    "Alice laughed so much at this, that she had to run back into the wood for fear of them hearing her."
    
    hide footmen_fish
    hide footmen_frog
    show footmen_frog at breathing:
        pos (0.7, 0.9) zoom 0.5
    voice "n1249"
    "And when she next peeped out the Fish-Footman was gone, and the other was sitting on the ground near the door, staring stupidly up into the sky."

    show alice thinking at breathing:
        pos (0.3, 0.9) zoom alice_scale
    play sound "sfx/knockknockknock.mp3"
    voice "n1250"
    "Alice went timidly up to the door, and knocked."
    voice "frogfoot2"
    frogfoot "There’s no sort of use in knocking, and that for two reasons. First, because I’m on the same side of the door as you are; secondly, because they’re making such a noise inside, no one could possibly hear you."

    #play sound "sfx/shatter.mp3"
    voice "n1251"
    "And certainly there was a most extraordinary noise going on within—a constant howling and sneezing, and every now and then a great crash, as if a dish or kettle had been broken to pieces."
    show alice disturbed at breathing
    voice "alice181"
    alice "Please, then, how am I to get in?"
    voice "frogfoot3"
    frogfoot "There might be some sense in your knocking, if we had a door between us. For instance, if you were inside, you might knock, and I could let you out, you know."
    voice "n1252"
    "He was looking up into the sky all the time he was speaking, and this Alice thought decidedly uncivil."
    show alice thinking at breathing
    voice "alice182"
    alice "(But perhaps he can’t help it, his eyes are so very nearly at the top of his head. But at any rate he might answer questions)"
    show alice happy at breathing
    camera:
        ease cam_transition zpos -200
    voice "alice183"
    alice "*loud* How am I to get in?"
    voice "frogfoot4"
    frogfoot "I shall sit here, till tomorrow—"

    play sound "<silence 2.0>"
    queue sound "sfx/shatter.mp3"
    show plate: # at center
        anchor(0.5, 0.5)
        xpos 1.5 ypos 0.4 zoom 0.5
        linear 2.0 xpos -0.5
    voice "n1253"
    "At this moment the door of the house opened, and a large plate came skimming out, straight at the Footman’s head: it just grazed his nose, and broke to pieces against one of the trees behind him."

    voice "frogfoot5"
    frogfoot "—or next day, maybe."

    #"The Footman continued in the same tone, exactly as if nothing had happened."
    show alice pout at breathing
    camera:
        ease cam_transition zpos -400 xpos 0.33
    voice "alice184"
    alice "*louder* How am I to get in?" # asked Alice again, in a louder tone.
    camera:
        ease cam_transition zpos -400 xpos 0.64 ypos -135 zrotate -10 # frog weird
    voice "frogfoot6"
    frogfoot "Are you to get in at all? That’s the first question, you know."
    camera:
        ease cam_transition zpos -400 xpos 0.33 ypos 0 zrotate 10 # alice disturbed
    show alice disturbed at breathing
    voice "n1254"
    "It was, no doubt: only Alice did not like to be told so."
    camera:
        ease cam_transition zpos -400 xpos 0.33 ypos 0 zrotate 0 # alice normal
    voice "alice185"
    alice "(It’s really dreadful, the way all the creatures argue. It’s enough to drive one crazy!)"
    camera:
        ease cam_transition zpos 0 xpos 0.5 ypos 0 zrotate 0 # neutral
    voice "n1255"
    "The Footman seemed to think this a good opportunity for repeating his remark, with variations."
    camera:
        ease cam_transition zpos -400 xpos 0.64 ypos -135 zrotate -10 # frog weird
    voice "frogfoot7"
    frogfoot "I shall sit here, on and off, for days and days."
    show alice pout at breathing
    camera:
        ease cam_transition zpos -400 xpos 0.33 ypos 0 zrotate 10 # alice disturbed
    voice "alice186"
    alice "But what am I to do?"
    camera:
        ease cam_transition zpos -400 xpos 0.64 ypos -135 zrotate 0 # frog normal
    voice "frogfoot8"
    frogfoot "Anything you like." # said the Footman, and began whistling.
    camera:
        ease cam_transition zpos -400 xpos 0.33 ypos 0 zrotate 0 # alice normal
    voice "alice187"
    alice "Oh, there’s no use in talking to him, he’s perfectly idiotic!"

    play sound "sfx/door_open.mp3"
    voice "n1256"
    "And she opened the door and went in."

label ch6_kitchen:
    scene kitchen

    play music "audio/rinne oak general store.mp3" fadein 1.0 fadeout 1.0

    camera:
        perspective True

        xpos 0 ypos 0 zpos 0 xoffset -center_offset
        linear 30.0 xpos 1480

    define alice_kitchen_pos = 0
    define duchess_kitchen_pos = 540
    define cook_kitchen_pos = 1115
    define cat_kitchen_pos = 1735
    define cat_cam_z_zom = -300
    define alice_duchess_kitchen_pos = 270
    define cook_scale = 0.6
    show alice normal at breathing:
        pos (alice_kitchen_pos, 0.9) zoom alice_scale
    show cook at breathing:
        pos (cook_kitchen_pos, 0.9) zoom cook_scale
    show cat:
        align (0.5, 1.0)
        xpos cat_kitchen_pos ypos 0.59 zoom 0.63
    show duchess at breathing:
        pos (duchess_kitchen_pos, 0.9) zoom duchess_scale
    show baby normal:
        anchor (0.5, 1.0)
        xpos duchess_kitchen_pos ypos 0.75 zoom 0.7 zpos 30
        linear 1.0 xoffset -10 yoffset -10 rotate 2
        linear 1.0 xoffset 10 yoffset 10 rotate -2
        linear 1.0 xoffset -10 yoffset 10 rotate 2
        linear 1.0 xoffset 10 yoffset -10 rotate -2
        repeat
    
    voice "n1257"
    "The door led right into a large kitchen, which was full of smoke from one end to the other: the Duchess was sitting on a three-legged stool in the middle, nursing a baby; the cook was leaning over the fire, stirring a large cauldron which seemed to be full of soup."
    voice "alice188"
    alice "(There’s certainly too much pepper in that soup!)" # Alice said to herself, as well as she could for sneezing.
    voice "n1258"
    "There was certainly too much of it in the air. Even the Duchess sneezed occasionally; and as for the baby, it was sneezing and howling alternately without a moment’s pause."
    voice "n1259"
    "The only things in the kitchen that did not sneeze, were the cook, and a large cat which was sitting on the hearth and grinning from ear to ear."

    camera:
        ease cam_transition xpos cat_kitchen_pos zpos cat_cam_z_zom
    voice "alice189"
    alice "Please would you tell me, why your cat grins like that?" # said Alice, a little timidly, for she was not quite sure whether it was good manners for her to speak first

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    voice "duchess01"
    duchess "It’s a Cheshire cat, and that’s why. Pig!"

    camera:
        ease cam_transition xpos alice_duchess_kitchen_pos zpos 0
    show alice surprised at breathing:
        ease 0.3 yoffset -100
        ease 0.3 yoffset 0
    voice "n1260"
    "She said the last word with such sudden violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:"

    show alice thinking at breathing:
        yoffset 0
    voice "alice190"
    alice "I didn’t know that Cheshire cats always grinned; in fact, I didn’t know that cats could grin."

    voice "duchess02"
    duchess "They all can, and most of ’em do."
    voice "alice191"
    alice "I don’t know of any that do."

    show alice normal at breathing
    voice "n1261"
    "Alice said very politely, feeling quite pleased to have gotten into a conversation."

    voice "duchess03"
    duchess "You don’t know much, and that’s a fact."
    show alice disturbed at breathing
    voice "n1262"
    "Alice did not at all like the tone of this remark, and thought it would be as well to introduce some other subject of conversation."
    
    show plate as plate1:
        anchor(0.5, 0.5)
        xpos cook_kitchen_pos ypos 0.4 zoom 0.5 zrotate 20
        linear 2.0 xpos duchess_kitchen_pos

    show plate as plate2:
        anchor(0.5, 0.5)
        xpos cook_kitchen_pos ypos 0.5 zoom 0.5 zrotate -20
        pause 0.5
        linear 2.0 xpos duchess_kitchen_pos

    show plate as plate3:
        anchor(0.5, 0.5)
        xpos cook_kitchen_pos ypos 0.6 zoom 0.5
        pause 1
        linear 2.0 xpos duchess_kitchen_pos
    voice "n1263"
    "While she was trying to fix on one, the cook took the cauldron of soup off the fire, and at once set to work throwing everything within her reach at the Duchess and the baby—the fire-irons came first; then followed a shower of saucepans, plates, and dishes."

    hide plate1
    hide plate2
    hide plate3
    voice "n1264"
    "The Duchess took no notice of them even when they hit her; and the baby was howling so much already, that it was quite impossible to say whether the blows hurt it or not."
    
    show alice pout at breathing
    voice "alice192"
    alice "Oh, please mind what you’re doing!"
    #"Cried Alice, jumping up and down in an agony of terror."#
    voice "n1265"
    "Alice was jumping up and down in an agony of terror."#
    show alice surprised at breathing
    voice "alice193"
    alice "Oh, there goes his precious nose..."

    show saucepan:
        anchor(0.5, 0.5)
        xpos cook_kitchen_pos ypos 0.6 zoom 1.0
        linear 2.0 xpos -600
    voice "n1266"
    "An unusually large saucepan flew close by it, and very nearly carried it off."

    voice "duchess04"
    duchess "If everybody minded their own business, the world would go round a deal faster than it does." # the Duchess said in a hoarse growl, "
    hide saucepan

    show alice joking at breathing
    voice "alice194"
    alice "Which would not be an advantage. Just think what work it would make with the day and night! You see the earth takes twenty-four hours to turn round on its axis—"

    voice "duchess05"
    duchess "Talking of axes, chop off her head!"

    show alice pout at breathing

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0
    voice "n1267"
    "Alice glanced rather anxiously at the cook, to see if she meant to take the hint; but the cook was busily stirring the soup, and seemed not to be listening, so she went on again:"

    show alice thinking at breathing
    camera:
        ease cam_transition xpos alice_kitchen_pos zpos 0
    voice "alice195"
    alice "Twenty-four hours, I think; or is it twelve? I—"

    voice "duchess06"
    duchess "Oh, don’t bother me, I never could abide figures!" 
    voice "n1268"
    "And with that she began nursing her child again, singing a sort of lullaby to it as she did so, and giving it a violent shake at the end of every line:"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    voice "duchess07"
    duchess "Speak roughly to your little boy,\n{space=30}And beat him when he sneezes:\nHe only does it to annoy,\n{space=30}Because he knows it teases."

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0

    #"CHORUS.\n(In which the cook and the baby joined)"
    voice "everyone6"
    everyone "Wow! wow! wow!"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    voice "n1269"
    "While the Duchess sang the second verse of the song, she kept tossing the baby violently up and down, and the poor little thing howled so, that Alice could hardly hear the words:"

    voice "duchess08"
    duchess "I speak severely to my boy,\n{space=30}I beat him when he sneezes;\nFor he can thoroughly enjoy\n{space=30}The pepper when he pleases!"

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0  
    voice "everyone6"
    everyone "Wow! wow! wow!"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    voice "duchess09"
    duchess "Here! you may nurse it a bit, if you like!" 
    
    show baby normal:
        ease 1.0 xpos alice_kitchen_pos ypos 0.75
    voice "n1270"
    "The Duchess said to Alice, flinging the baby at her as she spoke."
    show baby normal:
        xpos alice_kitchen_pos ypos 0.75
        linear 1.0 xoffset -10 yoffset -10 rotate 2
        linear 1.0 xoffset 10 yoffset 10 rotate -2
        linear 1.0 xoffset -10 yoffset 10 rotate 2
        linear 1.0 xoffset 10 yoffset -10 rotate -2
        repeat
    voice "duchess10"
    duchess "I must go and get ready to play croquet with the Queen."
    voice "n1271"
    "The duchess hurried out of the room."
    show duchess:
        linear 3.0 xpos 3000

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0
    voice "n1272"
    "The cook threw a frying-pan after her as she went out, but it just missed her."

    camera:
        ease cam_transition xpos alice_kitchen_pos zpos 0
    voice "n1273"
    "Alice caught the baby with some difficulty, as it was a queer-shaped little creature, and held out its arms and legs in all directions."
    show alice surprised at breathing
    voice "alice196"
    alice "Just like a star-fish."
    voice "n1274"
    "The poor little thing was snorting like a steam-engine when she caught it, and kept doubling itself up and straightening itself out again, so that altogether, for the first minute or two, it was as much as she could do to hold it."

    scene black
    camera:
        perspective False
        xpos 0 zpos 0 xoffset 0
    voice "n1275"
    "As soon as she had made out the proper way of nursing it, (which was to twist it up into a sort of knot, and then keep tight hold of its right ear and left foot, so as to prevent its undoing itself,) she carried it out into the open air."


    call setup_forest
    call reset_camera

    show alice pout at breathing:
        pos (0.5, 0.9) zoom alice_scale
    show baby normal:
        anchor (0.5, 1.0)
        xpos 0.5 ypos 0.75 zoom 0.7
        linear 1.0 xoffset -10 yoffset -10 rotate 2
        linear 1.0 xoffset 10 yoffset 10 rotate -2
        linear 1.0 xoffset -10 yoffset 10 rotate 2
        linear 1.0 xoffset 10 yoffset -10 rotate -2
        repeat
    show tree at parallax(300):
        xpos 1156
    camera:
        perspective True
        xpos 0.5 xoffset -center_offset

    voice "alice197"
    alice "(If I don’t take this child away with me, they’re sure to kill it in a day or two)"
    voice "alice198"
    alice "Wouldn’t it be murder to leave it behind?"
    voice "n1276"
    "The little thing grunted in reply (it had left off sneezing by this time)"
    voice "alice199"
    alice "Don’t grunt, that’s not at all a proper way of expressing yourself."
    show alice surprised at breathing
    voice "n1277"
    "The baby grunted again, and Alice looked very anxiously into its face to see what was the matter with it."
    show baby half
    camera:
        ease cam_transition zpos -300
    voice "n1278"
    "There could be no doubt that it had a very turn-up nose, much more like a snout than a real nose; also not like the look of the thing at all."
    voice "alice200"
    alice "But perhaps it was only sobbing."
    voice "n1279"
    "She looked into its eyes again, to see if there were any tears."
    voice "n1280"
    "No, there were no tears."
    show alice pout at breathing
    voice "alice201"
    alice "If you’re going to turn into a pig, my dear, I’ll have nothing more to do with you. Mind now!"
    voice "n1281"
    "The poor little thing sobbed again (or grunted, it was impossible to say which), and they went on for some while in silence."
    voice "alice202"
    alice "Now, what am I to do with this creature when I get it home?"
    voice "n1282"
    "Then it grunted again, so violently, that she looked down into its face in some alarm."
    show alice surprised at breathing
    show baby pig
    camera:
        ease cam_transition zpos -300 zrotate -10 ypos 135
    voice "n1283"
    "This time there could be no mistake about it: it was neither more nor less than a pig, and she felt that it would be quite absurd for her to carry it further."

    hide baby
    camera:
        ease cam_transition zpos 0 zrotate 0 ypos 0
    voice "n1284"
    "So she set the little creature down, and felt quite relieved to see it trot away quietly into the wood."

    play music "audio/rinne lilly.mp3" fadein 1.0 fadeout 1.0
    show alice joking at breathing
    voice "alice203"
    alice "If it had grown up, it would have made a dreadfully ugly child: but it makes rather a handsome pig, I think."
    voice "n1285"
    "And she began thinking over other children she knew, who might do very well as pigs."
    camera:
        ease cam_transition zpos 0 zrotate 0
    voice "alice204"
    alice "If one only knew the right way to change them—"
    show alice surprised at breathing
    camera:
        ease cam_transition xpos 0.74
    define cat_pos = 0.83
    define cat_pos_y = 0.41
    define cat_zoom = 0.35
    show cat:
        anchor (0.5, 1.0)
        xpos cat_pos ypos cat_pos_y zpos 300 zoom cat_zoom
    voice "n1286"
    "She got a little startled by seeing the Cheshire Cat sitting on a bough of a tree a few yards off."

    voice "n1287"
    "The Cat only grinned when it saw Alice."
    voice "n1288"
    "It looked good-natured, she thought: still it had very long claws and a great many teeth, so she felt that it ought to be treated with respect."
    voice "alice205"
    alice "*timidly* Cheshire Puss..." 
    #"She began, rather timidly, as 
    voice "n1289"
    "She did not at all know whether it would like the name: however, it only grinned a little wider."
    show alice normal at breathing
    voice "alice206"
    alice "Come, it’s pleased so far."
    voice "alice207"
    alice "Would you tell me, please, which way I ought to go from here?"

    voice "cat01"
    cat "That depends a good deal on where you want to get to."
    voice "alice208"
    alice "I don’t much care where—"

    voice "cat02"
    cat "Then it doesn’t matter which way you go."
    show alice disturbed at breathing
    voice "alice209"
    alice "—so long as I get somewhere."

    voice "cat03"
    cat "Oh, you’re sure to do that, if you only walk long enough."
    voice "n1290"
    "Alice felt that this could not be denied, so she tried another question."
    show alice normal at breathing
    voice "alice210"
    alice "What sort of people live about here?"

    voice "cat04"
    cat "In that direction, lives a Hatter: and in that direction, lives a March Hare. Visit either you like: they’re both mad."
    voice "alice211"
    alice "But I don’t want to go among mad people."

    voice "cat05"
    cat "Oh, you can’t help that. We’re all mad here. I’m mad. You’re mad."
    show alice disturbed at breathing 
    voice "alice212"
    alice "How do you know I’m mad?"

    voice "cat06"
    cat "You must be, or you wouldn’t have come here."
    voice "n1291"
    "Alice didn’t think that proved it at all; however, she went on:"
    show alice joking at breathing
    voice "alice213"
    alice "And how do you know that you’re mad?"

    voice "cat07"
    cat "To begin with, a dog’s not mad. You grant that?"
    show alice thinking at breathing
    voice "alice214"
    alice "I suppose so."

    voice "cat08"
    cat "Well, then, you see, a dog growls when it’s angry, and wags its tail when it’s pleased. Now I growl when I’m pleased, and wag my tail when I’m angry. Therefore I’m mad."
    show alice normal at breathing
    voice "alice215"
    alice "I call it purring, not growling."

    voice "cat09"
    cat "Call it what you like."
    voice "cat10"
    cat "Do you play croquet with the Queen today?"
    voice "alice216"
    alice "I should like it very much, but I haven’t been invited yet."

    voice "cat11"
    cat "You’ll see me there."

    hide cat
    show alice normal at breathing
    voice "n1292"
    "The Cat vanished."
    voice "n1293"
    "Alice was not much surprised at this, she was getting so used to queer things happening."
    voice "n1294"
    "While she was looking at the place where it had been, it suddenly appeared  again." # the cat appeared again

    show cat:
        anchor (0.5, 1.0)
        xpos cat_pos ypos cat_pos_y zpos 300 zoom cat_zoom
    voice "cat12"
    cat "By the way, what became of the baby?"
    voice "cat13"
    cat "I’d nearly forgotten to ask."
    show alice surprised at breathing
    voice "alice217"
    alice "It turned into a pig."
    show alice thinking at breathing
    voice "cat14"
    cat "I thought it would." # said the cat and VANISHED again

    hide cat
    voice "n1295"
    "The Cat vanished again."
    voice "n1296"
    "Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March Hare was said to live."
    voice "alice218"
    alice "I’ve seen hatters before, the  March Hare will be much the most interesting, and perhaps as this is May it won’t be raving mad—at least not so mad as it was in March."

label ch6_cat:
    show cat:
        anchor (0.5, 1.0)
        xpos cat_pos ypos cat_pos_y zpos 300 zoom cat_zoom
    voice "n1297"
    "As she said this, she looked up, and there was the Cat again, sitting on a branch of a tree."

    voice "cat15"
    cat "Did you say pig, or fig?"
    show alice disturbed at breathing
    voice "alice219"
    alice "I said pig, and I wish you wouldn’t keep appearing and vanishing so suddenly: you make one quite giddy."

    voice "cat16"
    cat "All right."

    hide cat
    define cat_t = 1.5
    image cat_animated: 
        "cat.png" with Dissolve(cat_t, alpha=True)
        pause cat_t
        "cat2.png" with Dissolve(cat_t, alpha=True)
        #pause cat_t
        #"cat3.png" with Dissolve(cat_t, alpha=True)
        pause cat_t
        "cat4.png" with Dissolve(cat_t, alpha=True)
        pause cat_t
        "cat5.png" with Dissolve(cat_t, alpha=True)
        pause cat_t
        "cat6.png" with Dissolve(cat_t, alpha=True)

    show cat_animated:
        anchor (0.5, 1.0)
        xpos cat_pos ypos cat_pos_y zpos 300 zoom cat_zoom
    voice "n1298"
    "This time it vanished quite slowly, beginning with the end of the tail, and ending with the grin, which remained some time after the rest of it had gone."
    show alice happy at breathing
    voice "alice220"
    alice "Well! I’ve often seen a cat without a grin, but a grin without a cat! It’s the most curious thing I ever saw in my life!"

    scene hare_house
    call reset_camera
    voice "n1299"
    "She had not gone much farther before she came in sight of the house of the March Hare: she thought it must be the right house, because the chimneys were shaped like ears and the roof was thatched with fur."
    voice "n1300"
    "It was so large a house, that she did not like to go nearer till she had nibbled some more of the lefthand bit of mushroom, and raised herself to about two feet high: even then she walked up towards it rather timidly."    
    voice "alice221"
    alice "Suppose it should be raving mad after all! I almost wish I’d gone to see the Hatter instead!"

label chapter7:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1301"
    "{size=+40}Chapter VII: \n{/size}A Mad Tea-Party"

    play music "audio/rinne lilly.mp3" if_changed

    scene hare_house
    camera:
        perspective True
        xpos 10 ypos 0 zpos 0 xoffset -center_offset
        linear 10.0 xpos 800

    define alice_tea_pos = 10
    define hare_tea_pos = 500
    define dormouse_tea_pos = 800
    define dormouse_tea_cam_pos = 760
    define hatter_tea_pos = 1000
    define hare_scale = 0.9
    define hatter_scale = 0.5
    define dormouse_scale = 0.44
    show alice normal zorder 100 at breathing:
        pos (-285, 0.9) zoom alice_scale

    show hare at breathing:
        pos (hare_tea_pos, 0.79) zoom hare_scale
    show dormouse sleep at breathing:
        pos (dormouse_tea_pos, 0.71) zoom dormouse_scale
    show hatter normal at breathing:
        pos (hatter_tea_pos, 1.02) zoom hatter_scale

    image hare_house_front_mask = AlphaMask("hare_house", "hare_house_front")
    show hare_house_front_mask zorder 50
    voice "n1302"
    "There was a table set out under a tree in front of the house, and the March Hare and the Hatter were having tea at it: a Dormouse was sitting between them, fast asleep, and the other two were using it as a cushion, resting their elbows on it, and talking over its head."
    voice "alice222"
    alice "(Very uncomfortable for the Dormouse, only, as it’s asleep, I suppose it doesn’t mind)"
    voice "n1303"
    "The table was a large one, but the three were all crowded together at one corner of it."
    voice "everyone8"
    everyone "No room! No room!" 

    camera:
        ease cam_transition xpos 10
    voice "alice223"
    alice "There’s plenty of room!"

    camera:
        ease cam_transition xpos alice_tea_pos
    
    show alice normal zorder 0 at breathing:
        pos (alice_tea_pos, 0.9)
    voice "n1304"
    "She sat down in a large arm-chair at one end of the table."

    camera:
        ease cam_transition xpos hare_tea_pos zpos -415
    voice "hare01"
    hare "Have some wine."

    camera:
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "n1305"
    "Alice looked all round the table, but there was nothing on it but tea."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice surprised at breathing
    voice "alice224"
    alice "I don’t see any wine."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415
    voice "hare02"
    hare "There isn’t any."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice disturbed at breathing
    voice "alice225"
    alice "Then it wasn’t very civil of you to offer it." # said Alice angrily

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415
    voice "hare03"
    hare "It wasn’t very civil of you to sit down without being invited."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice226"
    alice "I didn’t know it was your table, it’s laid for a great many more than three."


    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter01"
    hatter "Your hair wants cutting."
    voice "n1306"
    "He had been looking at Alice for some time with great curiosity, and this was his first speech."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice pout at breathing
    voice "alice227"
    alice "You should learn not to make personal remarks, it’s very rude."
    voice "n1307"
    "The Hatter opened his eyes very wide on hearing this." # ; but all he said was"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter02"
    hatter "Why is a raven like a writing-desk?"

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice normal at breathing
    voice "alice228"
    alice "(Come, we shall have some fun now! I’m glad they’ve begun asking riddles)"
    voice "alice229"
    alice "I believe I can guess that."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare04"
    hare "Do you mean that you think you can find out the answer to it?"

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice230"
    alice "Exactly so."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    show alice pout at breathing
    voice "hare05"
    hare "Then you should say what you mean."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice231"
    alice "I do, at least—at least I mean what I say—that’s the same thing, you know."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter03"
    hatter "Not the same thing a bit! Why, you might just as well say that ‘I see what I eat’ is the same thing as ‘I eat what I see’!"

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare06"
    hare "You might just as well say, that ‘I like what I get’ is the same thing as ‘I get what I like’!"

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "dormouse01"
    dormouse "You might just as well say, that ‘I breathe when I sleep’ is the same thing as ‘I sleep when I breathe’!"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter04"
    hatter "It is the same thing with you."
    show alice thinking at breathing
    voice "n1308"
    "And here the conversation dropped, and the party sat silent for a minute, while Alice thought over all she could remember about ravens and writing-desks, which wasn’t much."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "n1309"
    "The hatter was the first to break the silence."
    voice "hatter05"
    hatter "What day of the month is it?"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "n1310"
    "He had taken his watch out of his pocket, and was looking at it uneasily, shaking it every now and then, and holding it to his ear." # turning to alice
    voice "n1311"
    "Alice considered it a little..."
    voice "alice232"
    alice "The fourth."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter06"
    hatter "Two days wrong!"
    voice "n1312"
    "He looked angrily at the March Hare."
    voice "hatter07"
    hatter "I told you butter wouldn’t suit the works!"
    
    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare07"
    hare "It was the best butter."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter08"
    hatter "Yes, but some crumbs must have got in as well, you shouldn’t have put it in with the bread-knife."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "n1313"
    "The March Hare took the watch and looked at it gloomily: then he dipped it into his cup of tea, and looked at it again: but he could think of nothing better to say than his first remark."

    voice "hare08"
    hare "It was the best butter, you know."
    voice "n1314"
    "Alice had been looking over his shoulder with some curiosity."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice excited at breathing
    voice "alice233"
    alice "What a funny watch!"
    voice "alice234"
    alice "It tells the day of the month, and it doesn’t tell what o’clock it is!"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter09"
    hatter "Why should it?" # muttered the Hatter.
    voice "hatter10"
    hatter "Does your watch tell you what year it is?"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice joking at breathing
    voice "alice235"
    alice "Of course not, but that’s because it stays the same year for such a long time together."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter11"
    hatter "Which is just the case with mine."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "n1315"
    "Alice felt dreadfully puzzled."
    voice "n1316"
    "The Hatter’s remark seemed to have no sort of meaning in it, and yet it was certainly English."
    voice "alice236"
    alice "I don’t quite understand you."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter12"
    hatter "The Dormouse is asleep again."

    camera:
        ease cam_transition xpos 840 zpos -415 ypos 5
    voice "n1317"
    "He poured a little hot tea upon its nose."
    voice "n1318"
    "The Door-mouse shook its head impatiently, and said, without opening its eyes:"
    
    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "dormouse02"
    dormouse "Of course, of course; just what I was going to remark myself."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "n1319"
    "The hatter turned to Alice again."
    voice "hatter13"
    hatter "Have you guessed the riddle yet?"

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice237"
    alice "No, I give it up. What’s the answer?"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter14"
    hatter "I haven’t the slightest idea."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare09"
    hare "Nor I."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice disturbed at breathing
    voice "alice238"
    alice "I think you might do something better with the time, than waste it in asking riddles that have no answers."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter15"
    hatter "If you knew Time as well as I do, you wouldn’t talk about wasting it. It’s him."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice239"
    alice "I don’t know what you mean."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter16"
    hatter "Of course you don’t! I dare say you never even spoke to Time!"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice240"
    alice "Perhaps not, but I know I have to beat time when I learn music."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter17"
    hatter "Ah! That accounts for it. He won’t stand beating. Now, if you only kept on good terms with him, he’d do almost anything you liked with the clock."
    voice "hatter18"
    hatter "For instance, suppose it were nine o’clock in the morning, just time to begin lessons: you’d only have to whisper a hint to Time, and round goes the clock in a twinkling! Half-past one, time for dinner!"

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare10"
    hare "(I only with wish it was...)"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "alice241"
    alice "That would be grand, certainly, but then—I shouldn’t be hungry for it, you know."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter19"
    hatter "Not at first, perhaps, but you could keep it to half-past one as long as you liked."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice242"
    alice "Is that the way you manage?"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "n1321"
    "The Hatter shook his head mournfully."
    voice "hatter20"
    hatter "Not I! We quarrelled last March—just before he went mad, you know—"
    voice "n1322"
    "The Hatter pointed with his tea spoon at the March Hare."
    voice "hatter21"
    hatter "It was at the great concert given by the Queen of Hearts, and I had to sing\n‘Twinkle, twinkle, little bat!\nHow I wonder what you’re at!’"
    voice "hatter22"
    hatter "You know the song, perhaps?"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice243"
    alice "I’ve heard something like it."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter23"
    hatter "It goes on, you know, in this way:"
    voice "hatter24"
    hatter "Up above the world you fly,\nLike a tea-tray in the sky.\nTwinkle, twinkle—"
    voice "n1323"
    "Here the Dormouse shook itself, and began singing in its sleep:"

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "dormouse03"
    dormouse "Twinkle, twinkle, twinkle, twinkle—"
    voice "n1324"
    "And went on so long that they had to pinch it to make it stop."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter25"
    hatter "Well, I’d hardly finished the first verse, when the Queen jumped up and bawled out, ‘He’s murdering the time! Off with his head!’"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice surprised at breathing
    voice "alice244"
    alice "How dreadfully savage!"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter26"
    hatter "And ever since that, he won’t do a thing I ask! It’s always six o’clock now."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "n1325"
    "A bright idea came into Alice’s head."
    show alice happy at breathing
    voice "alice245"
    alice "Is that the reason so many tea-things are put out here?"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter27"
    hatter "Yes, that’s it, it’s always tea-time, and we’ve no time to wash the things between whiles."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice246"
    alice "Then you keep moving round, I suppose?"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter28"
    hatter "Exactly so, as the things get used up."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "alice247"
    alice "But what happens when you come to the beginning again?"

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare11"
    hare "Suppose we change the subject. I’m getting tired of this. I vote the young lady tells us a story."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice248"
    alice "I’m afraid I don’t know one."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "everyone9"
    everyone "Then the Dormouse shall! Wake up, Dormouse!"
    voice "n1326"
    "And they pinched it on both sides at once."

    show dormouse tired at breathing
    voice "n1327"
    "The Dormouse slowly opened his eyes."

    voice "dormouse04"
    dormouse "I wasn’t asleep, I heard every word you fellows were saying."

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare12"
    hare "Tell us a story!"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice excited at breathing
    voice "alice249"
    alice "Yes, please do!"

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter29"
    hatter "And be quick about it, or you’ll be asleep again before it’s done."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130

    voice "dormouse05"
    dormouse "Once upon a time there were three little sisters, and their names were Elsie, Lacie, and Tillie; and they lived at the bottom of a well—"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "alice250"
    alice "What did they live on?"
    voice "n1328"
    "Alice always took a great interest in questions of eating and drinking."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    show popup at popup onlayer screens
    show treacle at popup onlayer screens
    voice "dormouse06"
    dormouse "They lived on treacle."

    "..."
    hide treacle onlayer screens
    hide popup onlayer screens

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice disturbed at breathing
    voice "alice251"
    alice "They couldn’t have done that, you know, they’d have been ill."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "dormouse07"
    dormouse "So they were, very ill..."

    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "n1329"
    "Alice tried to fancy to herself what such an extraordinary ways of living would be like, but it puzzled her too much, so she went on:"
    show alice thinking at breathing
    voice "alice252"
    alice "But why did they live at the bottom of a well?"

    camera: 
        ease cam_transition xpos hare_tea_pos zpos -415 ypos 5
    voice "hare13"
    hare "Take some more tea."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice disturbed at breathing
    voice "alice253"
    alice "I’ve had nothing yet, so I can’t take more." # Alice replied in an offended tone.
    #voice "n1330"
    #"Alice replied in an offended tone."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter30"
    hatter "You mean you can’t take less. It’s very easy to take more than nothing."


    camera:  
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    voice "alice254"
    alice "Nobody asked your opinion."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter31"
    hatter "Who’s making personal remarks now?" # the Hatter asked triumphantly.


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "n1331"
    "Alice did not quite know what to say to this: so she helped herself to some tea and bread-and-butter, and then turned to the Dormouse, and repeated her question."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "n1332"
    "The Dormouse again took a minute or two to think about it."

    voice "dormouse08"
    dormouse "It was a treacle-well."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice pout at breathing
    voice "alice255"
    alice "There’s no such thing!"
    voice "n1334"
    "Alice was beginning very angrily, but the Hatter and the March Hare went."

    camera: 
        ease cam_transition xpos 530 zpos -30 ypos 30
    voice "everyone10"
    everyone "Sh! sh!"

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130

    voice "dormouse09"
    dormouse "If you can’t be civil, you’d better finish the story for yourself."


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice surprised at breathing
    voice "alice256"
    alice "No, please go on! I won’t interrupt again. I dare say there may be one."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130

    voice "dormouse10"
    dormouse "One, indeed!"
    voice "dormouse11"
    dormouse "And so these three little sisters—they were learning to draw, you know—"


    camera: 
        ease cam_transition xpos alice_tea_pos zpos -415 ypos 5
    show alice thinking at breathing
    voice "alice257"
    alice "What did they draw?"

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos zpos -505 ypos 130
    voice "dormouse12"
    dormouse "Treacle."

    camera: 
        ease cam_transition xpos hatter_tea_pos zpos -415 ypos 5
    voice "hatter32"
    hatter "I want a clean cup, let’s all move one place on."

label ch7_reorder:

    define hatter_tea_pos2 = 1210
    define hatter_cam_pos2 = 1215
    define alice_tea_pos2 = hare_tea_pos
    define hare_tea_pos2 = dormouse_tea_pos
    define dormouse_tea_pos2 = hatter_tea_pos
    define dormouse_tea_cam_pos2 = 945
    show hatter normal zorder 100 at breathing:
        xpos hatter_tea_pos2
    show alice zorder 0 at breathing:
        xpos alice_tea_pos2
    show hare zorder 1 at breathing:
        xpos hare_tea_pos2
    show dormouse zorder 2 at breathing:
        xpos dormouse_tea_pos2 ypos 0.74


    camera: 
        ease cam_transition xpos 855 zpos -130 ypos 30
    voice "n1335"
    "He moved on as he spoke, and the Dormouse followed him: the March Hare moved into the Dormouse’s place, and Alice rather unwillingly took the place of the March Hare. The Hatter was the only one who got any advantage from the change: and Alice was a good deal worse off than before, as the March Hare had just upset the milk-jug into his plate."

    camera: 
        ease cam_transition xpos alice_tea_pos2
    voice "n1336"
    "Alice did not wish to offend the Dormouse again, so she began very cautiously:"

    camera: 
        ease cam_transition xpos alice_tea_pos2 zpos -495 ypos 30
    voice "alice258"
    alice "But I don’t understand. Where did they draw the treacle from?"

    camera: 
        ease cam_transition xpos hatter_cam_pos2 zpos -425 ypos 5
    voice "hatter33"
    hatter "You can draw water out of a water-well, so I should think you could draw treacle out of a treacle-well—eh, stupid?"

    camera: 
        ease cam_transition xpos alice_tea_pos2 zpos -495 ypos 30
    show alice pout at breathing
    voice "alice259"
    alice "But they were in the well."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos2 zpos -495 ypos 215

    voice "dormouse13"
    dormouse "Of course they were, well in."
    voice "n1337"
    "This answer so confused poor Alice, that she let the Dormouse go on for some time without interrupting it."

    voice "dormouse14"
    dormouse "They were learning to draw..."
    voice "n1338"
    "The Dormouse went on, yawning and rubbing its eyes, for it was getting very sleepy."
    # todo close eyes
    voice "dormouse15"
    dormouse "...and they drew all manner of things—everything that begins with an M———"

    show dormouse sleep at breathing
    "..."

    camera: 
        ease cam_transition xpos alice_tea_pos2 zpos -495 ypos 30
    show alice thinking at breathing
    voice "alice260"
    alice "Why with an M?"

    camera: 
        ease cam_transition xpos hare_tea_pos2 zpos -425 ypos 5
    voice "hare14"
    hare "Why not?"
    voice "n1339"
    "Alice was silent."

    camera: 
        ease cam_transition xpos dormouse_tea_cam_pos2 zpos -495 ypos 215
    voice "n1340"
    "The Dormouse had closed its eyes by this time, and was going off into a doze; but, on being pinched by the Hatter, it woke up again with a little shriek, and went on:"
    # wake up
    show dormouse tired at breathing
    voice "dormouse16"
    dormouse "—that begins with an M, such as mouse-traps, and the moon, and memory, and muchness—you know you say things are “much of a muchness”—did you ever see such a thing as a drawing of a muchness?"
    
    camera: 
        ease cam_transition xpos alice_tea_pos2 zpos -495 ypos 30
    show alice surprised at breathing
    voice "alice261"
    alice "Really, now you ask me, I don’t think—"

    camera: 
        ease cam_transition xpos hatter_cam_pos2 zpos -425 ypos 5
    voice "hatter34"
    hatter "Then you shouldn’t talk."

    hide alice
    voice "n1341"
    "This piece of rudeness was more than Alice could bear: she got up in great disgust, and walked off; the Dormouse fell asleep instantly, and neither of the others took the least notice of her going, though she looked back once or twice, half hoping that they would call after her: the last time she saw them, they were trying to put the Dormouse into the teapot."

    call setup_forest
    call reset_camera
    camera:
        perspective True
        xpos 0.5 xoffset -center_offset

    show alice disturbed at breathing:
        pos (0.5, 0.9) zoom alice_scale
    voice "alice262"
    alice "At any rate I’ll never go there again!"
    voice "alice263"
    alice "It’s the stupidest tea-party I ever was at in all my life!"
    voice "n1342"
    "Just as she said this, she noticed that one of the trees had a door leading right into it."

    show alice surprised at breathing
    voice "alice264"
    alice "(That’s very curious!)"
    voice "alice265"
    alice "(But everything’s curious today. I think I may as well go in at once)"
    voice "n1343"
    "And she went in."

    scene black
    call setup_hallway
    call reset_camera

    camera:
        perspective True
        xpos alice_hall_table_pos1 zpos -45.0 xoffset -center_offset
    
    show alice normal at breathing zorder 100:
        xpos alice_hall_table_pos1 zoom alice_hall_default_zoom zpos -45.0 ypos 1.0

    show three_legged_table_key zorder 50:
        align (0.5, 1.0) xpos three_legged_table_xpos zoom three_legged_table_zoom zpos three_legged_table_zpos ypos three_legged_table_ypos

    voice "n1344"
    "Once more she found herself in the long hall, and close to the little glass table."

    voice "alice266"
    alice "Now, I’ll manage better this time."

    camera:
        ease 3 xpos alice_hall_curtain_pos ypos 255 zpos -595
    show alice normal at breathing:
        ease 3 xpos alice_hall_curtain_pos zpos -400.0

    voice "n1345"
    "She began by taking the little golden key, and unlocking the door that led into the garden."
    
    show alice normal at breathing:
        xpos alice_hall_curtain_pos zpos -400.0
        ease 3 zoom 0.25
    play sound "sfx/unlock.mp3"
    voice "n1346"
    "Then she went to work nibbling at the mushroom (she had kept a piece of it in her pocket) till she was about a foot high: then she walked down the little passage: and then—she found herself at last in the beautiful garden, among the bright flower-beds and the cool fountains."

label chapter8:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1347"
    "{size=+40}Chapter VIII: \n{/size}The Queen's Croquet-Ground"

    play music "audio/rinne rosalia garden.mp3"

    #scene garden at windy
    scene bluesky at parallax(-4000)
    show hills at parallax(-4000)
    show roses at parallax(-400) as rosesbg1:
        xtile 10 zoom 0.5 ypos 0.54 xoffset 300
    show roses at parallax(-300) as rosesbg2:
        xtile 10 zoom 0.5 ypos 0.54
    show grass at parallax:
        yoffset 550 xoffset -900 xtile 5
    show rosetree at parallax:
        xpos -0.15
    show tree at parallax(300) zorder 1000:
        xpos -0.69
    show roses at parallax(300) zorder 1000 as roses1:
        xpos -0.4 yoffset 390
    show roses at parallax(250) zorder 900 as roses2:
        xpos 0.0 yoffset 440
    show roses at parallax(300) zorder 1000 as roses3:
        xpos 0.4 yoffset 390
    #show garden_front_mask zorder 1000 at windy_mask

    define alice_garden = -0.5
    define card_zoom = 0.75
    define card2_garden = 0.15
    define card5_garden = 0.33
    define card7_garden = 0.57

    define card2_garden_y = 0.83
    define card5_garden_y = 0.77
    define card7_garden_y = 0.8

    define card2_garden_z = 0
    define card5_garden_z = -50
    define card7_garden_z = -20

    camera:
        perspective True
        xpos alice_garden xoffset -center_offset
        ease 10.0 xpos 0.33
    
    show card5 at breathing:
        pos (card5_garden, card5_garden_y) zoom card_zoom
        zpos card5_garden_z
    show card7 at breathing:
        pos (card7_garden, card7_garden_y) zoom card_zoom
        zpos card7_garden_z
    show card2 at breathing:
        pos (card2_garden, card2_garden_y) zoom card_zoom
        zpos card2_garden_z

    show alice normal at breathing:
        pos (alice_garden, 0.8) zoom alice_scale

    

    voice "n1348"
    "A large rose-tree stood near the entrance of the garden: the roses growing on it were white, but there were three gardeners at it, busily painting them red."
    voice "n1349"
    "Alice thought this a very curious thing, and she went nearer to watch them, and just as she came up to them..."

    camera:
        ease cam_transition xpos card2_garden zoom 2.0 ypos 700
    voice "two1"
    two "Look out now, Five! Don’t go splashing paint over me like that!"
    camera:
        ease cam_transition xpos card5_garden zoom 2.0 ypos 700
    voice "five1"
    five "I couldn’t help it, Seven jogged my elbow."
    # On which seven looked up and said
    camera:
        ease cam_transition xpos card7_garden zoom 2.0 ypos 700
    voice "seven1"
    seven "That’s right, Five! Always lay the blame on others!"

    camera:
        ease cam_transition xpos card5_garden zoom 2.0 ypos 700
    voice "five2"
    five "You’d better not talk!" 
    voice "five3"
    five "I heard the Queen say only yesterday you deserved to be beheaded!"

    camera:
        ease cam_transition xpos card2_garden zoom 2.0 ypos 700
    voice "two2"
    two "What for?"

    camera:
        ease cam_transition xpos card7_garden zoom 2.0 ypos 700
    voice "seven2"
    seven "That’s none of your business, Two!"

    camera:
        ease cam_transition xpos card5_garden zoom 2.0 ypos 700
    voice "five4"
    five "Yes, it is his business! And I’ll tell him—it was for bringing the cook tulip-roots instead of onions."

    camera:
        ease cam_transition xpos card7_garden zoom 2.0 ypos 700
    voice "n1350"
    "Seven flung down his brush..."
    voice "seven3"
    seven "Well, of all the unjust things—"

    camera:
        ease cam_transition xpos alice_garden zoom 2.0 ypos 700
    voice "n1351"
    "His eye chanced to fall upon Alice, as she stood watching them, and he checked himself suddenly: the others looked round also, and all of them bowed low."
    show alice surprised at breathing
    voice "alice267"
    alice "Would you tell me, why you are painting those roses?"

    camera:
        ease cam_transition xpos card2_garden zoom 2.0 ypos 700
    voice "n1352"
    "Five and Seven said nothing, but looked at Two."
    voice "two3"
    two "Why the fact is, you see, Miss, this here ought to have been a red rose-tree, and we put a white one in by mistake; and if the Queen was to find it out, we should all have our heads cut off, you know."
    voice "two4"
    two "So you see, Miss, we’re doing our best, afore she comes, to—" # "Two began in a low voice,
    camera:
        ease cam_transition xpos card5_garden zoom 2.0 ypos 700
    voice "n1353"
    "At this moment Five, who had been anxiously looking across the garden, called out:"
    voice "five5"
    five "The Queen! The Queen!"

    # flip cards:
    show card5:
        xpos card5_garden ypos card5_garden_y zpos card5_garden_z zoom card_zoom
        linear 1.0 xrotate -100
    show card2:
        xpos card2_garden ypos card2_garden_y zpos card2_garden_z zoom card_zoom
        linear 1.0 xrotate -100
    show card7:
        xpos card7_garden ypos card7_garden_y zpos card7_garden_z zoom card_zoom
        linear 1.0 xrotate -100
    pause 1.0
    hide card5
    hide card2
    hide card7

    show card_back as cardback5 zorder 6:
        anchor (0.5, 1.0)
        xpos card5_garden ypos card5_garden_y zpos card5_garden_z zoom card_zoom
        xrotate -100
        linear 1.0 xrotate -180
    show card_back as cardback2 zorder 8:
        anchor (0.5, 1.0)
        xpos card2_garden ypos card2_garden_y zpos card2_garden_z zoom card_zoom
        xrotate -100
        linear 1.0 xrotate -180
    show card_back as cardback7 zorder 7:
        anchor (0.5, 1.0)
        xpos card7_garden ypos card7_garden_y zpos card7_garden_z zoom card_zoom
        xrotate -100
        linear 1.0 xrotate -180
    
    voice "n1354"
    "And the three gardeners instantly threw themselves flat upon their faces."

    camera:
        ease cam_transition zoom 1.0 ypos 0 xpos 1.4
    voice "n1355"
    "There was a sound of many footsteps, and Alice looked round, eager to see the Queen."

    define garden_p1_start = 3.0
    define garden_p2_start = 2.5
    define garden_p1_mid = 1.61
    define garden_p2_mid = 1.14
    define garden_p1_end = 0.3
    define garden_p2_end = -0.2

    show soldier9 as soldier2:
        anchor (0.5, 1.0)
        xpos garden_p2_start ypos 0.8 zpos -50
        ease 1.0 xpos garden_p2_mid
    show soldier9 as soldier1:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8
        ease 1.0 xpos garden_p1_mid
    voice "n1356"
    "First came ten soldiers carrying clubs; these were all shaped like the three gardeners, oblong and flat, with their hands and feet at the corners." # 9
    show soldier9 as soldier2:
        ease 1.0 xpos garden_p2_end
    show soldier9 as soldier1:
        ease 1.0 xpos garden_p1_end
    
    show ace as court2:
        anchor (0.5, 1.0)
        xpos garden_p2_start ypos 0.8 zpos -50
        ease 1.0 xpos garden_p2_mid
    show ace as court1:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8
        ease 1.0 xpos garden_p1_mid
    voice "n1357"
    "Next the ten courtiers; these were ornamented all over with diamonds, and walked two and two, as the soldiers did." # ace?
    
    hide soldier2
    hide soldier1
    show ace as court2:
        ease 1.0 xpos garden_p2_end
    show ace as court1:
        ease 1.0 xpos garden_p1_end
    show child10 as child2:
        anchor (0.5, 1.0)
        xpos garden_p2_start ypos 0.8 zpos -50 zoom 1.2
        ease 1.0 xpos garden_p2_mid
    show child10 as child1:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8 zoom 1.2
        ease 1.0 xpos 1.45 # move child a bit closer
    voice "n1358"
    "After these came the royal children; there were ten of them, and the little dears came jumping merrily along hand in hand, in couples: they were all ornamented with hearts." # 10 ?
    
    hide court2
    hide court1
    show child10 as child2:
        ease 1.0 xpos garden_p2_end
    show child10 as child1:
        ease 1.0 xpos garden_p1_end

    show normalqueen:
        anchor (0.5, 1.0)
        xpos garden_p2_start ypos 0.8 zpos -50
        ease 1.0 xpos garden_p2_mid
    show normalking:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8
        ease 1.0 xpos garden_p1_mid
    show rabbit normal at breathing:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8 zoom rabbit_scale
        ease 1.0 xpos 1.3

    voice "n1359"
    "Next came the guests, mostly Kings and Queens, and among them Alice recognised the White Rabbit: it was talking in a hurried nervous manner, smiling at everything that was said, and went by without noticing her."
    
    hide child2
    hide child1
    show normalqueen:
        ease 1.0 xpos garden_p2_end
    show normalking:
        ease 1.0 xpos garden_p1_end
    show rabbit normal at breathing:
        ease 1.0 xpos garden_p1_end
    show knave:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8
        ease 1.0 xpos 1.3

    voice "n1360"
    "Then followed the Knave of Hearts, carrying the King’s crown on a crimson velvet cushion."

    hide normalqueen
    hide normalking
    hide rabbit
    show knave:
        ease 1.0 xpos garden_p1_end
    show queen normal at breathing:
        anchor (0.5, 1.0)
        xpos garden_p2_start ypos 0.8 zpos -50 zoom queen_scale
        ease 1.0 xpos garden_p2_mid
    show king at breathing:
        anchor (0.5, 1.0)
        xpos garden_p1_start ypos 0.8 zoom king_scale
        ease 1.0 xpos garden_p1_mid

    voice "n1361"
    "And, last of all this grand procession, came THE KING AND QUEEN OF HEARTS."

    # hide all
    hide knave
    hide queen
    hide king
    # move camera to alice instant
    define alice_garden2 = 0.04
    show alice thinking zorder 100 at breathing:
        xpos alice_garden2
    camera:
        xpos alice_garden2

    voice "n1362"
    "Alice was rather doubtful whether she ought not to lie down on her face like the three gardeners, but she could not remember ever having heard of such a rule at processions."
    voice "alice268"
    alice "(What would be the use of a procession, if people had all to lie down upon their faces, so that they couldn’t see it?)"
    voice "n1363"
    "So she stood still where she was, and waited."

    voice "n1364"
    "When the procession came opposite to Alice, they all stopped and looked at her."

    define queen_garden = 0.6
    define king_garden = 1.1
    define knave_garden = 0.8

    # show queen near the gardeners
    show knave at breathing:
        pos (knave_garden, 0.8)
        zpos -100
    show queen normal zorder 10 at breathing:
        pos (queen_garden, 0.8) zoom queen_scale
        zpos -20
    show king at breathing:
        pos (king_garden, 0.8) zoom king_scale


    camera:
        ease cam_transition xpos queen_garden

    # the Queen said severely
    voice "queen01"
    queen "Who is this?"

    camera:
        ease cam_transition xpos knave_garden zoom 2.0 ypos 700
    voice "n1365"
    "She said it to the Knave of Hearts, who only bowed and smiled in reply."

    camera:
        ease cam_transition xpos queen_garden zoom 2.0 ypos 700
    voice "queen02"
    queen "Idiot!"

    voice "n1366"
    "The Queen tossed her head impatiently and turned to Alice."
    camera:
        ease cam_transition xpos queen_garden zoom 1.0 ypos 0
    voice "queen03"
    queen "What’s your name, child?"

    camera:
        ease cam_transition xpos alice_garden2 zoom 1.0 ypos 0
    show alice normal at breathing
    voice "alice269"
    alice "My name is Alice, so please your Majesty." # saif alice politely
    voice "alice270"
    alice "(Why, they’re only a pack of cards, after all. I needn’t be afraid of them!)"

    camera:
        ease cam_transition xpos queen_garden zoom 1.0 ypos 0
    voice "queen04"
    queen "And who are these?"

    camera:
        ease cam_transition xpos card5_garden zoom 1.0 ypos 0
    voice "n1367"
    "The Queen pointed to the three gardeners who were lying round the rose-tree; for, you see, as they were lying on their faces, and the pattern on their backs was the same as the rest of the pack, she could not tell whether they were gardeners, or soldiers, or courtiers, or three of her own children."

    camera:
        ease cam_transition xpos alice_garden2 zoom 1.0 ypos 0
    show alice surprised at breathing
    voice "alice271"
    alice "How should I know? It’s no business of mine."

    camera:
        ease cam_transition xpos queen_garden zoom 1.0 ypos 0
    voice "n1368"
    "The Queen turned crimson with fury, and, after glaring at her for a moment like a wild beast, screamed:"
    show queen angry at breathing
    voice "queen05"
    queen "Off with her head! Off—"

    camera:
        ease cam_transition xpos alice_garden2 zoom 1.0 ypos 0
    show alice pout at breathing
    voice "alice272"
    alice "Nonsense!" #  said Alice, very loudly and decidedly, and the Queen was silent.
    show queen normal at breathing
    "..."

    camera:
        ease cam_transition xpos king_garden zoom 1.0 ypos 0
    voice "n1369"
    "The King laid his hand upon her arm, and timidly said:"
    voice "king01"
    king "Consider, my dear: she is only a child!"

    camera:
        ease cam_transition xpos queen_garden zoom 1.0 ypos 0
    voice "n1370"
    "The Queen turned angrily away from him, and said to the Knave:"
    show queen angry at breathing
    voice "queen06"
    queen "Turn them over!"
    show queen normal at breathing
    # move knave
    show knave:
        ease 0.5 xpos card5_garden
        ease 1.0 xpos card2_garden
        ease 1.0 xpos card7_garden
        ease 1.0 xpos knave_garden
    
    pause 0.5
    # flip cards back
    show card_back as cardback5 zorder 6:
        anchor (0.5, 1.0)
        xpos card5_garden ypos card5_garden_y zpos card5_garden_z zoom card_zoom
        xrotate -180
        linear 1.0 xrotate -72
    show card_back as cardback2 zorder 8:
        anchor (0.5, 1.0)
        xpos card2_garden ypos card2_garden_y zpos card2_garden_z zoom card_zoom
        xrotate -180
        pause 1.0
        linear 1.0 xrotate -72
    show card_back as cardback7 zorder 7:
        anchor (0.5, 1.0)
        xpos card7_garden ypos card7_garden_y zpos card7_garden_z zoom card_zoom
        xrotate -180
        pause 2.0
        linear 1.0 xrotate -72

    pause 1.0

    hide cardback5
    show card5 zorder 6:
        anchor (0.5, 1.0)
        xpos card5_garden ypos card5_garden_y zpos card5_garden_z zoom card_zoom
        xrotate -72
        linear 1.0 xrotate 0
    pause 1.0

    hide cardback2
    show card2 zorder 8:
        anchor (0.5, 1.0)
        xpos card2_garden ypos card2_garden_y zpos card2_garden_z zoom card_zoom
        xrotate -72
        linear 1.0 xrotate 0

    pause 1.0

    hide cardback7
    show card7 zorder 7:
        anchor (0.5, 1.0)
        xpos card7_garden ypos card7_garden_y zpos card7_garden_z zoom card_zoom
        xrotate -72
        linear 1.0 xrotate 0
    
    camera:
        ease cam_transition xpos card5_garden zoom 1.0 ypos 0
    voice "n1371"
    "The Knave did so, very carefully, with one foot."
    show queen angry at breathing
    voice "queen07"
    queen "Get up!" # said the Queen, in a shrill, loud voice,
    show queen normal at breathing
    voice "n1372"
    "The three gardeners instantly jumped up, and began bowing to the King, the Queen, the royal children, and everybody else."
    show queen angry at breathing
    voice "queen08"
    queen "Leave off that!" # screamed the Queen.
    show queen normal at breathing
    voice "queen09"
    queen "You make me giddy."

    voice "n1373"
    "And then, turning to the rose-tree, she went on:"
    voice "queen10"
    queen "What have you been doing here?"
    voice "two5"
    two "May it please your Majesty, we were trying—" # said Two, in a very humble tone, going down on one knee as he spoke
    show queen happy at breathing
    voice "queen11"
    queen "I see!"
    voice "n1374"
    "The queen had meanwhile been examining the roses."
    show queen angry at breathing
    voice "queen12"
    queen "Off with their heads!"
    # queen disappear
    show queen normal at breathing:
        zoom queen_scale
        linear 1.0 xpos 2.0
    show king at breathing:
        zoom king_scale
        linear 1.0 xpos 2.0
    show knave at breathing:
        linear 1.0 xpos 2.0
    
    show card5:
        ease 0.5 xpos -0.15
    show card7:
        ease 0.5 xpos -0.04
    show card2:
        ease 0.5 xpos -0.26

    camera:
        ease cam_transition xpos alice_garden2 zoom 1.0 ypos 0
    voice "n1375"
    "And the procession moved on, three of the soldiers remaining behind to execute the unfortunate gardeners, who ran to Alice for protection."
    hide queen
    hide king
    hide knave
    show alice surprised at breathing
    voice "alice273"
    alice "You shan’t be beheaded!"

    define alice_garden3 = -0.37

    show alice normal at breathing:
        ease 0.5 xpos -0.37
    hide card5
    hide card7
    hide card2
    voice "n1376"
    "Alice put them into a large flower-pot that stood near. "

    show soldier9:
        anchor (0.5, 1.0)
        xpos 1.0 ypos 0.8
        ease 1.0 xpos 0.3
        pause 1.0
        ease 1.0 xpos 0.5
    voice "n1377"
    "The three soldiers wandered about for a minute or two, looking for them, and then quietly marched off after the others."

    define queen_garden2 = 1.0

    camera:
        ease cam_transition xpos queen_garden2
    show queen normal at breathing:
        pos (queen_garden2, 0.8) zoom queen_scale
    voice "queen13"
    queen "Are their heads off?"

    camera:
        ease cam_transition xpos 0.5
    voice "soldiers1"
    soldiers "Their heads are gone, if it please your Majesty!" # shouted in reply

    camera:
        ease cam_transition xpos queen_garden2
    show queen happy at breathing
    voice "queen14"
    queen "That’s right!" # shouted
    show alice surprised at breathing
    voice "queen15"
    queen "Can you play croquet?"

    camera:
        ease cam_transition xpos alice_garden3
    voice "n1378"
    "The soldiers were silent, and looked at Alice, as the question was evidently meant for her."
    voice "alice274"
    alice "Yes!"

    camera:
        ease cam_transition xpos queen_garden2
    voice "queen16"
    queen "Come on, then!" #  roared the Queen

    # move queen away
    define alice_garden4 = 0.3
    show queen happy at breathing:
        linear 1.0 xpos 3.0
    show soldier9:
        linear 1.0 xpos 2.5
    show alice thinking at breathing:
        pos (alice_garden4, 0.8) zoom alice_scale

    camera:
        ease cam_transition xpos alice_garden4
    voice "n1379"
    "Alice joined the procession, wondering very much what would happen next."

    show rabbit normal zorder 200 at breathing:
        pos (0.57, 0.85) zoom rabbit_scale
    voice "rabbit18"
    rabbit "It’s—it’s a very fine day!" # timid voice
    voice "n1380"
    "She was walking by the White Rabbit, who was peeping anxiously into her face."
    voice "alice275"
    alice "Very, —where’s the Duchess?"
    voice "rabbit19"
    rabbit "Hush! Hush!" # low and hurried tone
    voice "n1381"
    "The rabbit looked anxiously over his shoulder as he spoke, and then raised himself upon tiptoe, put his mouth close to her ear, and whispered:"
    voice "rabbit20"
    rabbit "She’s under sentence of execution."
    voice "alice276"
    alice "What for?"
    voice "rabbit21"
    rabbit "Did you say ‘What a pity!’?"
    show alice disturbed at breathing
    voice "alice277"
    alice "No, I didn’t, I don’t think it’s at all a pity. I said ‘What for?’"
    voice "rabbit22"
    rabbit "She boxed the Queen’s ears—"

    show alice joking at breathing
    voice "n1382"
    "Alice gave a little scream of laughter."
    voice "rabbit23"
    rabbit "Oh, hush! The Queen will hear you! You see, she came rather late, and the Queen said—"

    jump ch8_croquet
label setup_croquet:

    scene bluesky at parallax(-4000)
    show hills at parallax(-4000)
    show grass at parallax:
        yoffset 550 xoffset -900 xtile 10
    show tree at parallax(300) zorder 10 as tree1:
        xpos -0.59
    show tree at parallax(300) zorder 10 as tree2:
        xpos 1.88 xzoom -1.0

    return
label ch8_croquet:

    call setup_croquet

    # setup character
    define queen_croquet = 0.0
    define alice_croquet = 1.3
    define cat_croquet = 1.55
    show queen normal at breathing:
        pos (queen_croquet, 0.9) zoom queen_scale
    show alice normal at breathing:
        pos (alice_croquet, 0.9) zoom alice_scale

    camera:
        perspective True
        xpos 0 ypos 0 zpos 0 xoffset -center_offset

    show queen angry at breathing
    voice "queen17"
    queen "Get to your places!"
    show queen normal at breathing
    voice "n1383"
    "Shouted the Queen in a voice of thunder, and people began running about in all directions, tumbling up against each other; however, they got settled down in a minute or two, and the game began."

    camera:
        ease cam_transition xpos alice_croquet
    voice "n1384"
    "Alice thought she had never seen such a curious croquet-ground in her life; it was all ridges and furrows; the balls were live hedgehogs, the mallets live flamingoes, and the soldiers had to double themselves up and to stand on their hands and feet, to make the arches."

    show alice happy at breathing
    voice "n1385"
    "The chief difficulty Alice found at first was in managing her flamingo: she succeeded in getting its body tucked away, comfortably enough, under her arm, with its legs hanging down, but generally, just as she had got its neck nicely straightened out, and was going to give the hedgehog a blow with its head, it would twist itself round and look up in her face, with such a puzzled expression that she could not help bursting out laughing."
    voice "n1386"
    "And when she had got its head down, and was going to begin again, it was very provoking to find that the hedgehog had unrolled itself, and was in the act of crawling away."
    voice "n1387"
    "Besides all this, there was generally a ridge or furrow in the way wherever she wanted to send the hedgehog to, and, as the doubled-up soldiers were always getting up and walking off to other parts of the ground, Alice soon came to the conclusion that it was a very difficult game indeed."

    camera:
        ease cam_transition xpos queen_croquet
    voice "n1388"
    "The players all played at once without waiting for turns, quarrelling all the while, and fighting for the hedgehogs; and in a very short time the Queen was in a furious passion, and went stamping about:"
    camera:
        ease cam_transition xpos queen_croquet zoom 2.0 ypos 700
    show queen angry at breathing
    voice "queen18"
    queen "Off with his head!"
    camera:
        ease cam_transition xpos queen_croquet zoom 1.0 ypos 0
    show queen happy  at breathing
    voice "n1389"
    "Or"
    camera:
        ease cam_transition xpos queen_croquet zoom 2.0 ypos 700
    show queen angry  at breathing
    voice "queen19"
    queen "Off with her head!" 
    camera:
        ease cam_transition xpos queen_croquet zoom 1.0 ypos 0
    show queen happy  at breathing
    voice "n1390"
    "About once in a minute."

    camera:
        zoom 1.0 ypos 0
        ease cam_transition xpos alice_croquet
    show alice surprised at breathing
    voice "n1391"
    "Alice began to feel very uneasy: to be sure, she had not as yet had any dispute with the Queen, but she knew that it might happen any minute."
    voice "alice278"
    alice "(And then, what would become of me? They’re dreadfully fond of beheading people here; the great wonder is, that there’s any one left alive!)"

    # cat appear slowly
    camera:
        ease 10.0 xpos cat_croquet

    show cat6:
        anchor (0.5, 1.0)
        xpos cat_croquet ypos 0.5 zoom cat_scale xoffset 120 # offset to center head
        alpha 0.0
        linear 10.0 alpha 1.0
    voice "n1392"
    "She was looking about for some way of escape, and wondering whether she could get away without being seen, when she noticed a curious appearance in the air: it puzzled her very much at first, but, after watching it a minute or two, she made it out to be a grin."
    show alice happy at breathing
    voice "alice279"
    alice "(It’s the Cheshire Cat: now I shall have somebody to talk to)"

    voice "cat17"
    cat "How are you getting on?" # said the Cat, as soon as there was mouth enough for it to speak with.

    show cat5:
        anchor (0.5, 1.0)
        xpos cat_croquet ypos 0.5 zoom cat_scale xoffset 120 # offset to center head
        alpha 0.0
        linear 10.0 alpha 1.0
    show alice normal at breathing
    voice "n1393"
    "Alice waited till the eyes appeared, and then nodded."
    voice "alice280"
    alice "(It’s no use speaking to it, till its ears have come, or at least one of them)"

    show cat4:
        anchor (0.5, 1.0)
        xpos cat_croquet ypos 0.5 zoom cat_scale xoffset 120 # offset to center head
        alpha 0.0
        linear 10.0 alpha 1.0
    voice "n1394"
    "In another minute the whole head appeared, and then Alice put down her flamingo, and began an account of the game, feeling very glad she had someone to listen to her."
    voice "n1395"
    "The Cat seemed to think that there was enough of it now in sight, and no more of it appeared."
    show alice disturbed at breathing
    voice "alice281"
    alice "I don’t think they play at all fairly, and they all quarrel so dreadfully one can’t hear oneself speak—and they don’t seem to have any rules in particular; at least, if there are, nobody attends to them—"
    voice "alice282"
    alice "And you’ve no idea how confusing it is all the things being alive; for instance, there’s the arch I’ve got to go through next walking about at the other end of the ground—and I should have croqueted the Queen’s hedgehog just now, only it ran away when it saw mine coming!"

    # let it appear full
    hide cat6
    hide cat5
    show cat4 at breathing:
        pos (cat_croquet, 0.5) zoom cat_scale
        xoffset 120
        alpha 1.0

    voice "cat18"
    cat "How do you like the Queen?"

    define queen_croquet2 = 1.03
    show queen normal at breathing:
        ease 1.0 xpos queen_croquet2
    show alice disturbed at breathing
    voice "alice283"
    alice "Not at all, she’s so extremely—"
    camera:
        ease cam_transition zoom 2.0 ypos 820 xpos 1.16 
    show alice thinking at breathing
    voice "n1396"
    "Just then she noticed that the Queen was close behind her, listening: so she went on:"
    show alice happy at breathing
    voice "alice284"
    alice "—likely to win, that it’s hardly worth while finishing the game."

    show queen happy at breathing:
        pause 1.0
        ease 1.0 xpos queen_croquet
    voice "n1397"
    "The Queen smiled and passed on."

    define king_croquet = 1.8
    define king_croquet2 = 1.06
    show king behind alice at breathing:
        pos (king_croquet, 0.9) zoom king_scale
    camera:
        ease cam_transition xpos cat_croquet ypos 0 zoom 1.0
    show alice normal at breathing
    voice "king02"
    king "Who are you talking to?" # said the King, going up to Alice
    voice "n1398"
    "The king was looking at the Cat’s head with great curiosity."
    voice "alice285"
    alice "It’s a friend of mine—a Cheshire Cat, allow me to introduce it."
    voice "king03"
    king "I don’t like the look of it at all, however, it may kiss my hand if it likes."

    voice "cat19"
    cat "I’d rather not."

    show king scared at breathing:
        linear 1.0 xpos king_croquet2
    voice "king04"
    king "Don’t be impertinent, and don’t look at me like that!"

    camera:
        ease cam_transition xpos alice_croquet ypos 0 zoom 1.0
    voice "n1399"
    "He got behind Alice as he spoke."
    show alice thinking at breathing
    voice "alice286"
    alice "A cat may look at a king, I’ve read that in some book, but I don’t remember where."

    voice "king05"
    king "Well, it must be removed."

    show queen normal at breathing:
        xpos 0.57
    camera:
        ease cam_transition xpos 0.84 ypos 0 zoom 1.0
    voice "n1400"
    "The King called the Queen, who was passing at the moment:"
    voice "king06"
    king "My dear! I wish you would have this cat removed!"

    camera:
        ease cam_transition xpos 0.57 ypos 700 zoom 2.0
    voice "n1401"
    "The Queen had only one way of settling all difficulties, great or small."
    show queen angry at breathing
    voice "queen20"
    queen "Off with his head!"
    show queen normal at breathing
    voice "n1402"
    "She said, without even looking round."

    camera:
        ease cam_transition xpos king_croquet2 ypos 700 zoom 2.0
    show king at breathing:
        pause 1.5
        linear 1.0 xpos 0.0
    voice "king07"
    king "I’ll fetch the executioner myself." # said the King eagerly, and he hurried off.

    camera:
        ease cam_transition xpos cat_croquet ypos 0 zoom 1.0
    voice "n1403"
    "Alice thought she might as well go back, and see how the game was going on, as she heard the Queen’s voice in the distance, screaming with passion."
    show alice normal at breathing
    voice "n1404"
    "She had already heard her sentence three of the players to be executed for having missed their turns, and she did not like the look of things at all, as the game was in such confusion that she never knew whether it was her turn or not."

    hide queen
    hide king

    show alice normal at breathing:
        ease 1.0 xpos 0.84
    camera:
        ease 1.5 xpos 0.84 ypos 0 zoom 1.0
    voice "n1405"
    "So she went in search of her hedgehog."
    voice "n1406"
    "The hedgehog was engaged in a fight with another hedgehog, which seemed to Alice an excellent opportunity for croqueting one of them with the other:" 

    show alice at breathing:
        ease 1.0 xpos -0.42
    camera:
        ease 1.5 xpos -0.42 ypos 0 zoom 1.0
    voice "n1407"
    "The only difficulty was, that her flamingo was gone across to the other side of the garden, where Alice could see it trying in a helpless sort of way to fly up into a tree."

    # setup king and queen when returning
    define king_croquet3 = 1.98
    define queen_croquet3 = 1.73
    show soldier9 behind alice at breathing:
        pos (1.46, 0.9)
    show king scared at breathing:
        pos (king_croquet3, 0.9) zoom king_scale
    show queen normal at breathing:
        pos (queen_croquet3, 0.9) zoom queen_scale

    show alice at breathing:
        ease 1.0 xpos 0.84
    camera:
        ease 1.5 xpos 0.84 ypos 0 zoom 1.0
    hide tree2 # otherwise is in the way of king
    show cat4 at breathing:
        pos (cat_croquet, 0.4) zoom cat_scale
        xoffset 120
        alpha 1.0

    voice "n1408"
    "By the time she had caught the flamingo and brought it back, the fight was over, and both the hedgehogs were out of sight."
    show alice thinking at breathing
    voice "alice287"
    alice "(But it doesn’t matter much, as all the arches are gone from this side of the ground)"

    show alice normal at breathing:
        ease 1.0 xpos alice_croquet

    
    camera:
        ease 1.5 xpos alice_croquet ypos 0 zoom 1.0
    voice "n1409"
    "So she tucked it away under her arm, that it might not escape again, and went back for a little more conversation with her friend."

    camera:
        ease 1.5 xpos cat_croquet ypos 0 zoom 1.0


    voice "n1410"
    "When she got back to the Cheshire Cat, she was surprised to find quite a large crowd collected round it: there was a dispute going on between the executioner, the King, and the Queen, who were all talking at once, while all the rest were quite silent, and looked very uncomfortable."
    voice "n1411"
    "The moment Alice appeared, she was appealed to by all three to settle the question, and they repeated their arguments to her, though, as they all spoke at once, she found it very hard indeed to make out exactly what they said."
    voice "n1412"
    "The executioner’s argument was, that you couldn’t cut off a head unless there was a body to cut it off from: that he had never had to do such a thing before, and he wasn’t going to begin at his time of life."
    voice "n1413"
    "The King’s argument was, that anything that had a head could be beheaded, and that you weren’t to talk nonsense."
    voice "n1414"
    "The Queen’s argument was, that if something wasn’t done about it in less than no time she’d have everybody executed, all round."
    voice "n1415"
    "(It was this last remark that had made the whole party look so grave and anxious)"

    # Alice could think of nothing else to say but
    show alice surprised at breathing
    voice "alice288"
    alice "It belongs to the Duchess: you’d better ask her about it."
    voice "queen21"
    queen "She’s in prison, fetch her here."

    show soldier9:
        linear 1.0 xpos 3.0
    show alice normal at breathing
    voice "n1416"
    "And the executioner went off like an arrow."

    show cat4:
        xpos cat_croquet zoom cat_scale
        xoffset 120
        linear 3.0 alpha 0.0
    voice "n1417"
    "The Cat’s head began fading away the moment he was gone, and, by the time he had come back with the Duchess, it had entirely disappeared; so the King and the executioner ran wildly up and down looking for it, while the rest of the party went back to the game."

label chapter9:
    $ persistent.started_story = True
    scene black
    camera:
        perspective False
        xpos 0 ypos 0 zpos 0 xoffset 0
    voice "n1418"
    "{size=+40}Chapter IX: \n{/size}The Mock Turtle's Story"

    play music "audio/rinne oak general store.mp3" fadein 1.0 fadeout 1.0

    #jump ch9_gryphon

    call setup_croquet

    # setup character
    define alice_nine = 1.3
    define duchess_nine = 1.5
    show alice normal at breathing:
        pos (alice_nine, 0.9) zoom alice_scale
    show duchess happy at breathing behind alice:
        pos (duchess_nine, 0.9) zoom duchess_scale zpos -40.0

    camera:
        perspective True
        xpos 1.4 ypos 0 zpos 0 xoffset -center_offset

    voice "duchess11"
    duchess "You can’t think how glad I am to see you again, you dear old thing!"
    voice "n1419"
    "The Duchess tucked her arm affectionately into Alice’s, and they walked off together."
    voice "n1420"
    "Alice was very glad to find her in such a pleasant temper, and thought to herself that perhaps it was only the pepper that had made her so savage when they met in the kitchen."

    show alice thinking at breathing
    camera:
        ease cam_transition xpos alice_nine ypos 1000 zoom 2.0
    voice "alice289"
    alice "(When I’m a Duchess, I won’t have any pepper in my kitchen at all)"
    voice "alice290"
    alice "(Soup does very well without—Maybe it’s always pepper that makes people hot-tempered, and vinegar that makes them sour—and camomile that makes them bitter—and—and barley-sugar and such things that make children sweet-tempered)"
    voice "alice291"
    alice "(I only wish people knew that: then they wouldn’t be so stingy about it, you know—)"

    show alice pout at breathing
    voice "n1421"
    "She had quite forgotten the Duchess by this time, and was a little startled when she heard her voice close to her ear."
    camera:
        ease cam_transition xpos 1.4 ypos 1000 zoom 2.0
    voice "duchess12"
    duchess "You’re thinking about something, my dear, and that makes you forget to talk. I can’t tell you just now what the moral of that is, but I shall remember it in a bit."

    show alice normal at breathing
    voice "alice292"
    alice "Perhaps it hasn’t one."

    voice "duchess13"
    duchess "Tut, tut, child!"
    voice "duchess14"
    duchess "Everything’s got a moral, if only you can find it."

    show alice disturbed at breathing
    show duchess happy at breathing:
        ease 0.5 xpos 1.45 zpos -20.0
    voice "n1422"
    "And she squeezed herself up closer to Alice’s side as she spoke."
    voice "n1423"
    "Alice did not much like keeping so close to her: first, because the Duchess was very ugly; and secondly, because she was exactly the right height to rest her chin upon Alice’s shoulder, and it was an uncomfortably sharp chin."
    show alice normal at breathing
    voice "alice293"
    alice "The game’s going on rather better now."

    voice "duchess15"
    duchess "’Tis so, and the moral of that is—‘Oh, ’tis love, ’tis love, that makes the world go round!’"
    show alice joking at breathing
    voice "alice294"
    alice "Somebody said, that it’s done by everybody minding their own business!"
    show alice normal at breathing
    voice "duchess16"
    duchess "Ah, well! It means much the same thing, and the moral of that is—‘Take care of the sense, and the sounds will take care of themselves’."
    
    show duchess happy at breathing:
        ease 0.5 xpos 1.42 zpos -20.0
    #"Said the Duchess, digging her sharp little chin into Alice’s shoulder."
    voice "n1424"
    "The Duchess started digging her sharp little chin into Alice’s shoulder."
    show alice thinking at breathing
    voice "alice295"
    alice "(How fond she is of finding morals in things!)"
    "..."
    voice "duchess17"
    duchess "I dare say you’re wondering why I don’t put my arm round your waist, the reason is, that I’m doubtful about the temper of your flamingo. Shall I try the experiment?"
    show alice joking at breathing
    voice "alice296"
    alice "He might bite." # Alice cautiously replied, not feeling at all anxious to have the experiment tried.
    show alice normal at breathing
    voice "n1425"
    "Alice did not feel at all anxious to have the experiment tried."
    voice "duchess18"
    duchess "Very true, flamingoes and mustard both bite. And the moral of that is—‘Birds of a feather flock together’."
    show alice disturbed at breathing
    voice "alice297"
    alice "Only mustard isn’t a bird."
    voice "duchess19"
    duchess "Right, as usual, what a clear way you have of putting things!"
    show alice thinking at breathing
    voice "alice298"
    alice "It’s a mineral, I think."
    voice "duchess20"
    duchess "Of course it is, there’s a large mustard-mine near here."
    voice "n1426"
    "The Duchess seemed ready to agree to everything that Alice said."
    voice "duchess21"
    duchess "And the moral of that is—‘The more there is of mine, the less there is of yours’."
    show alice excited at breathing
    voice "alice299"
    alice "Oh, I know!"
    voice "alice300"
    alice "It’s a vegetable. It doesn’t look like one, but it is."

    voice "duchess22"
    duchess "I quite agree with you, and the moral of that is—‘Be what you would seem to be’"
    show alice thinking at breathing
    voice "duchess23"
    duchess "—or if you’d like it put more simply—‘Never imagine yourself not to be otherwise than what it might appear to others that what you were or might have been was not otherwise than what you had been would have appeared to them to be otherwise’."
    show alice surprised at breathing
    voice "alice301"
    alice "I think I should understand that better, if I had it written down: but I can’t quite follow it as you say it."
    show alice thinking at breathing
    voice "duchess24"
    duchess "That’s nothing to what I could say if I chose."
    show alice disturbed at breathing
    voice "alice302"
    alice "Pray don’t trouble yourself to say it any longer than that."

    voice "duchess25"
    duchess "Oh, don’t talk about trouble!"
    voice "duchess26"
    duchess "I make you a present of everything I’ve said as yet."
    voice "alice303"
    alice "(A cheap sort of present!)"
    voice "alice304"
    alice "(I’m glad they don’t give birthday presents like that!)"
    show alice thinking at breathing
    voice "n1427"
    "She did not venture to say it out loud."

    voice "duchess27"
    duchess "Thinking again?"
    voice "n1428"
    "The Duchess asked, with another dig of her sharp little chin."
    show alice pout at breathing
    voice "alice305"
    alice "I’ve a right to think."
    voice "n1429"
    "She was beginning to feel a little worried."
    voice "duchess28"
    duchess "Just about as much right, as pigs have to fly; and the m—"
    show alice surprised at breathing
    voice "n1430"
    "But here, to Alice’s great surprise, the Duchess’s voice died away, even in the middle of her favourite word ‘moral’ and the arm that was linked into hers began to tremble."
    
    show queen normal at breathing:
        pos (0.8, 0.9) zoom queen_scale
    camera:
        ease cam_transition xpos 1.05 ypos 0 zoom 1.0
    voice "n1431"
    "Alice looked up, and there stood the Queen in front of them, with her arms folded, frowning like a thunderstorm."

    voice "duchess29"
    duchess "A fine day, your Majesty!" # the Duchess began in a low, weak voice.
    show queen angry at breathing
    voice "queen22"
    queen "Now, I give you fair warning, either you or your head must be off, and that in about half no time! Take your choice!"
    #"Shouted the Queen, stamping on the ground as she spoke."
    voice "n1432"
    "The Queen was stamping on the ground as she spoke."
    show queen normal at breathing
    show duchess:
        linear 1.0 xpos 2.0
    voice "n1433"
    "The Duchess took her choice, and was gone in a moment."
    show queen happy at breathing
    voice "queen23"
    queen "Let’s go on with the game."
    show queen normal at breathing
    voice "n1434"
    "The Queen said to Alice; and Alice was too much frightened to say a word, but slowly followed her back to the croquet-ground."

    voice "n1435"
    "The other guests had taken advantage of the Queen’s absence, and were resting in the shade: however, the moment they saw her, they hurried back to the game, the Queen merely remarking that a moment’s delay would cost them their lives."
    voice "n1436"
    "All the time they were playing the Queen never left off quarrelling with the other players, and shouting “Off with his head!” or “Off with her head!”."
    voice "n1437"
    "Those whom she sentenced were taken into custody by the soldiers, who of course had to leave off being arches to do this, so that by the end of half an hour or so there were no arches left, and all the players, except the King, the Queen, and Alice, were in custody and under sentence of execution."
    voice "n1438"
    "Then the Queen left off, quite out of breath, and said to Alice:"

    hide duchess
    voice "queen24"
    queen "Have you seen the Mock Turtle yet?"
    show alice thinking at breathing
    voice "alice306"
    alice "No, I don’t even know what a Mock Turtle is."
    show queen happy at breathing
    voice "queen25"
    queen "It’s the thing Mock Turtle Soup is made from."
    show queen normal at breathing
    voice "alice307"
    alice "I never saw one, or heard of one."
    voice "queen26"
    queen "Come on, then, and he shall tell you his history."

    # start walk
    show alice thinking at breathing:
        linear 10.0 xpos 0.0 # start from 1.3
    show queen normal at breathing:
        linear 10.0 xpos -0.5 # start from 0.8
    camera:
        linear 10.0 xpos -0.25 ypos 0 zoom 1.0
    voice "n1439"
    "As they walked off together, Alice heard the King say in a low voice, to the company generally:"
    voice "king08"
    king "You are all pardoned."
    voice "alice308"
    alice "(Come, that’s a good thing!)"
    voice "n1440"
    "Alice had felt quite unhappy at the number of executions the Queen had ordered."

    jump ch9_gryphon
label setup_cliff:
    scene bluesky at parallax(-4000)
    show hills at parallax(-4000)
    show grass at parallax:
        yoffset 550 xoffset -900 xtile 10
    show rock at parallax:
        xpos -0.6 ypos 0.84
    show tree at parallax(300) zorder 10:
        xpos 1.88

    return
label ch9_gryphon:
    call setup_cliff

    define gryphon_scale = 0.75

    show gryphon at breathing:
        pos (0.2, 0.95) xzoom -1.0 zoom gryphon_scale
    show queen normal at breathing:
        pos (1.23, 0.9) zoom queen_scale
    show alice normal at breathing:
        pos (1.7, 0.9) zoom alice_scale

    
    camera:
        perspective True
        xpos 1535 ypos 0 zpos 0 zoom 1.0 xoffset -center_offset
        ease 5.0 xpos 935
    voice "n1441"
    "They very soon came upon a Gryphon, lying fast asleep in the sun."
    # "(If you don’t know what a Gryphon is, look at the picture)"
    show queen angry at breathing
    voice "queen27"
    queen "Up, lazy thing!"
    show queen normal at breathing
    voice "queen28"
    queen "And take this young lady to see the Mock Turtle, and to hear his history."
    show queen happy at breathing
    voice "queen29"
    queen "I must go back and see after some executions I have ordered."
    show queen happy at breathing:
        linear 1.0 xpos 2.0
    show alice thinking at breathing:
        ease 3.0 xpos 1.2
    voice "n1442"
    "She walked off, leaving Alice alone with the Gryphon."
    voice "n1443"
    "Alice did not quite like the look of the creature, but on the whole she thought it would be quite as safe to stay with it as to go after that savage Queen: so she waited."
    voice "n1444"
    "The Gryphon sat up and rubbed its eyes: then it watched the Queen till she was out of sight: then it chuckled."
    voice "gryphon01"
    gryphon "What fun!"
    voice "alice309"
    alice "What is the fun?"

    voice "gryphon02"
    gryphon "Why, she. It’s all her fancy, that: they never executes nobody, you know. Come on!"
    show alice disturbed at breathing
    voice "alice310"
    alice "(Everybody says ‘come on!’ here. I never was so ordered about in all my life, never!)"

    define turtle_pos = -0.63
    define gyphon_pos = 0.39
    define alice_turtle = 0.26

    show gryphon at breathing behind alice:
        xzoom 1.0 xpos 1.34
    show turtle at breathing:
        pos (turtle_pos, 0.89)
    camera:
        linear 10.0 xpos -425
    stop music fadeout 10.0
    voice "n1445"
    "They had not gone far before they saw the Mock Turtle in the distance, sitting sad and lonely on a little ledge of rock, and, as they came nearer, Alice could hear him sighing as if his heart would break."
    voice "n1446"
    "She pitied him deeply."
    voice "alice311"
    alice "What is his sorrow?"
    #"She asked the Gryphon, and the Gryphon answered, very nearly in the same words as before."
    voice "gryphon03"
    gryphon "It’s all his fancy, that: he hasn’t got no sorrow, you know. Come on!"

    show gryphon at breathing:
        linear 1.0 xpos gyphon_pos
    show alice normal at breathing:
        linear 1.0 xpos alice_turtle
    camera:
        linear 1.0 xpos -120
    voice "n1447"
    "So they went up to the Mock Turtle, who looked at them with large eyes full of tears, but said nothing."

    voice "gryphon04"
    gryphon "This here young lady, she wants for to know your history, she do."
    voice "mock01"
    mock "I’ll tell it her, sit down, both of you, and don’t speak a word till I’ve finished."
    voice "n1448"
    "So they sat down, and nobody spoke for some minutes."
    show alice thinking at breathing:
        xpos alice_turtle
    "..."
    voice "alice312"
    alice "(I don’t see how he can ever finish, if he doesn’t begin)"
    voice "n1449"
    "But she waited patiently."

    play music "audio/rinne sad.mp3" fadein 1.0

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock02"
    mock "Once, *deep sigh* I was a real Turtle."
    #"Said the Mock Turtle at last, with a deep sigh."
    voice "n1450"
    "These words were followed by a very long silence, broken only by an occasional exclamation of:"
    camera:
        ease cam_transition xpos -60 ypos 875 zoom 2.0 # gryphon
    voice "gryphon05"
    gryphon "Hjckrrh!" 
    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "n1451"
    "And the constant heavy sobbing of the Mock Turtle." 
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "n1452"
    "Alice was very nearly getting up and saying, “Thank you, sir, for your interesting story”, but she could not help thinking there must be more to come, so she sat still and said nothing."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock03"
    mock "When we were little, we went to school in the sea."
    voice "mock04"
    mock "The master was an old Turtle—we used to call him Tortoise—"
    
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice313"
    alice "Why did you call him Tortoise, if he wasn’t one?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock05"
    mock "We called him Tortoise because he taught us, really you are very dull!" # angrily

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon06"
    gryphon "You ought to be ashamed of yourself for asking such a simple question."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice pout at breathing
    voice "n1453"
    "They both sat silent and looked at poor Alice, who felt ready to sink into the earth."
    voice "n1454"
    "At last the Gryphon said to the Mock Turtle:"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon07"
    gryphon "Drive on, old fellow! Don’t be all day about it!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock06"
    mock "Yes, we went to school in the sea, though you mayn’t believe it—"
    
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice disturbed at breathing
    voice "alice314"
    alice "I never said I didn’t!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock07"
    mock "You did."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon08"
    gryphon "Hold your tongue!"

    camera:
        ease cam_transition xpos -120 ypos 0 zoom 1.0 # NEUTRAL
    "..."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock08"
    mock "We had the best of educations—in fact, we went to school every day—"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice315"
    alice "I’ve been to a day-school, too, you needn’t be so proud as all that."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock09"
    mock "With extras?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "alice316"
    alice "Yes, we learned French and music."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock10"
    mock "And washing?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice disturbed at breathing
    voice "alice317"
    alice "Certainly not!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock11"
    mock "Ah! then yours wasn’t a really good school."
    # said the Mock Turtle in a tone of great relief.
    voice "mock12"
    mock "Now at ours they had at the end of the bill, ‘French, music, and washing—extra’."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice318"
    alice "You couldn’t have wanted it much, living at the bottom of the sea."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock13"
    mock "I couldn’t afford to learn it. I only took the regular course."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice319"
    alice "What was that?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock14"
    mock "Reeling and Writhing, of course, to begin with, and then the different branches of Arithmetic—Ambition, Distraction, Uglification, and Derision."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice320"
    alice "I never heard of ‘Uglification’. What is it?"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "n1455"
    "The Gryphon lifted up both its paws in surprise."
    voice "gryphon09"
    gryphon "What! Never heard of uglifying!"
    voice "gryphon10"
    gryphon "You know what to beautify is, I suppose?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice321"
    alice "Yes, it means to make anything prettier." # doubtfully

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon11"
    gryphon "Well, then, if you don’t know what to uglify is, you are a simpleton."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice pout at breathing
    voice "n1456"
    "Alice did not feel encouraged to ask any more questions about it, so she turned to the Mock Turtle:"
    show alice normal at breathing
    voice "alice322"
    alice "What else had you to learn?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock15"
    mock "Well, there was Mystery, ancient and modern, with Seaography: then Drawling—the Drawling-master was an old conger-eel, that used to come once a week: he taught us Drawling, Stretching, and Fainting in Coils."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice323"
    alice "What was that like?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock16"
    mock "Well, I can’t show it you myself."
    voice "mock17"
    mock "I’m too stiff. And the Gryphon never learnt it."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon12"
    gryphon "Hadn’t time, I went to the Classics master, though. He was an old crab, he was."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock18"
    mock "I never went to him, he taught Laughing and Grief, they used to say." # with a sigh

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon13"
    gryphon "So he did, so he did."
    camera:
        ease cam_transition xpos -120 ypos 0 zoom 1.0 # NEUTRAL
    voice "n1457"
    "They both sighed and hid their faces in their paws."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice324"
    alice "And how many hours a day did you do lessons?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock19"
    mock "Ten hours the first day, nine the next, and so on."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice happy at breathing
    voice "alice325"
    alice "What a curious plan!"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon14"
    gryphon "That’s the reason they’re called lessons, because they lessen from day to day."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "n1458"
    "This was quite a new idea to Alice, and she thought it over a little before she made her next remark."
    voice "alice326"
    alice "Then the eleventh day must have been a holiday?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock20"
    mock "Of course it was."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice joking at breathing
    voice "alice327"
    alice "And how did you manage on the twelfth?" # eagerly

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon15"
    gryphon "That’s enough about the lessons, tell her something about the games now."


label chapter10:
    $ persistent.started_story = True
    scene black
    camera:
        perspective False
        xpos 0 ypos 0 zpos 0 zoom 1.0 xoffset 0
    voice "n1459"
    "{size=+40}Chapter X: \n{/size}The Lobster Quadrille"

    play music "audio/rinne sad.mp3" if_changed

    # scene setup
    call setup_cliff

    show alice normal at breathing:
        pos (alice_turtle, 0.9) zoom alice_scale
    show gryphon at breathing behind alice:
        pos (gyphon_pos, 0.95) zoom gryphon_scale
    show turtle at breathing:
        pos (turtle_pos, 0.89)

    camera:
        perspective True
        xpos -120 ypos 0 zoom 1.0 xoffset -center_offset
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "n1460"
    "The Mock Turtle sighed deeply, and drew the back of one flapper across his eyes."
    voice "n1461"
    "He looked at Alice, and tried to speak, but for a minute or two sobs choked his voice."
    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon16"
    gryphon "Same as if he had a bone in his throat."
    voice "n1462"
    "The gryphon started shaking him and punching him in the back."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "n1463"
    "At last the Mock Turtle recovered his voice, and, with tears running down his cheeks, he went on again:"
    voice "mock21"
    mock "You may not have lived much under the sea—"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice surprised at breathing
    voice "alice328"
    alice "I haven’t."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock22"
    mock "And perhaps you were never even introduced to a lobster—"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # 
    show alice thinking at breathing
    voice "alice329"
    alice "I once tasted—" #  but checked herself hastily, and said
    show alice surprised at breathing
    voice "alice330"
    alice "No, never."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock23"
    mock "—so you can have no idea what a delightful thing a Lobster Quadrille is!"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice331"
    alice "No, indeed. What sort of a dance is it?"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon17"
    gryphon "Why, you first form into a line along the sea-shore—"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock24"
    mock "Two lines!" # cried the mock turtle
    voice "mock25"
    mock "Seals, turtles, salmon, and so on; then, when you’ve cleared all the jelly-fish out of the way—"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon18"
    gryphon "That generally takes some time."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock26"
    mock "—you advance twice—"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon19"
    gryphon "Each with a lobster as a partner!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock27"
    mock "Of course, advance twice, set to partners—"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon20"
    gryphon "—change lobsters, and retire in same order."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock28"
    mock "Then, you know, you throw the—"
    
    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    # leap into air
    show gryphon at breathing:
        ease 0.5 yoffset -200
        ease 0.5 yoffset 0
    voice "gryphon21"
    gryphon "The lobsters!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock29"
    mock "—as far out to sea as you can—"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon22"
    gryphon "Swim after them!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle

    # capering wildly about
    show turtle at breathing:
        pause 0.5
        ease 0.2 xoffset -50
        ease 0.4 xoffset 50
        ease 0.2 xoffset 0
    voice "mock30"
    mock "Turn a somersault in the sea!"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon23"
    gryphon "Change lobsters again!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock31"
    mock "Back to land again, and that’s all the first figure."

    camera:
        ease cam_transition xpos -120 ypos 0 zoom 1.0 # NEUTRAL
    voice "n1464"
    "The two creatures, who had been jumping about like mad things all this time, sat down again very sadly and quietly, and looked at Alice."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "alice332"
    alice "It must be a very pretty dance." # timidly

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock32"
    mock "Would you like to see a little of it?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "alice333"
    alice "Very much indeed."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "n1465"
    "The mock turtle turned to the gryphon:" # added
    voice "mock33"
    mock "Come, let’s try the first figure!"
    # "Said the Mock Turtle to the Gryphon."
    voice "mock34"
    mock "We can do without lobsters, you know. Which shall sing?"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon24"
    gryphon "Oh, you sing. I’ve forgotten the words."

    play music "audio/rinne oak general store.mp3" fadein 1.0 fadeout 1.0

    camera:
        ease cam_transition xpos -120 ypos 0 zoom 1.0 # NEUTRAL

    show turtle at breathing:
        linear 2.0 xoffset 1000 yoffset 100
        xzoom -1.0
        linear 2.0 xoffset 200
        xzoom 1.0
        repeat
    show gryphon at breathing:
        linear 2.0 xoffset -430
        xzoom -1.0 xoffset -1400
        linear 2.0 xoffset -970
        xzoom 1.0 xoffset 0
        repeat
    voice "n1467"
    "So they began solemnly dancing round and round Alice, every now and then treading on her toes when they passed too close, and waving their forepaws to mark the time, while the Mock Turtle sang this, very slowly and sadly:—"
    voice "mock35"
    mock " “Will you walk a little faster?” said a whiting to a snail.\n
    “There’s a porpoise close behind us, and he’s treading on my tail.”"
    voice "mock36"
    mock " See how eagerly the lobsters and the turtles all advance!\n
    They are waiting on the shingle—will you come and join the dance?"
    voice "mock37"
    mock " Will you, won’t you, will you, won’t you, will you join the dance?\n
    Will you, won’t you, will you, won’t you, won’t you join the dance?"
    voice "mock38"
    mock " “You can really have no notion how delightful it will be\n
    When they take us up and throw us, with the lobsters, out to sea!”"
    voice "mock39"
    mock " But the snail replied “Too far, too far!” and gave a look askance—\n
    Said he thanked the whiting kindly, but he would not join the dance."
    voice "mock40"
    mock " Would not, could not, would not, could not, would not join the dance.\n
    Would not, could not, would not, could not, could not join the dance."
    voice "mock41"
    mock " “What matters it how far we go?” his scaly friend replied.\n
    “There is another shore, you know, upon the other side."
    voice "mock42"
    mock " The further off from England the nearer is to France—\n
    Then turn not pale, beloved snail, but come and join the dance."
    voice "mock43"
    mock " Will you, won’t you, will you, won’t you, will you join the dance?\n
    Will you, won’t you, will you, won’t you, won’t you join the dance?”"

    show turtle at breathing:
        xzoom 1.0
        ease 1.0 xoffset 0 yoffset 0
    show gryphon at breathing:
        xzoom 1.0
        ease 1.0 xoffset 0 yoffset 0
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice happy at breathing
    voice "alice334"
    alice "Thank you, it’s a very interesting dance to watch."
    voice "n1468"
    "Alice was feeling very glad that it was over at last."
    voice "alice335"
    alice "And I do so like that curious song about the whiting!"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock44"
    mock "Oh, as to the whiting, they—you’ve seen them, of course?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "alice336"
    alice "Yes, I’ve often seen them at dinn—"
    show alice surprised at breathing
    voice "n1469"
    "She checked herself hastily."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock45"
    mock "I don’t know where Dinn may be, but if you’ve seen them so often, of course you know what they’re like."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    
    voice "alice337"
    alice "I believe so."
    voice "alice338"
    alice "They have their tails in their mouths—and they’re all over crumbs."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock46"
    mock "You’re wrong about the crumbs, crumbs would all wash off in the sea."
    voice "mock47"
    mock "But they have their tails in their mouths; and the reason is— *yawn* —Tell her about the reason and all that."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon25"
    gryphon "The reason is, that they would go with the lobsters to the dance."
    voice "gryphon26"
    gryphon "So they got thrown out to sea."
    voice "gryphon27"
    gryphon "So they had to fall a long way."
    voice "gryphon28"
    gryphon "So they got their tails fast in their mouths."
    voice "gryphon29"
    gryphon "So they couldn’t get them out again."
    voice "gryphon30"
    gryphon "That’s all."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "alice339"
    alice "Thank you, it’s very interesting. I never knew so much about a whiting before."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon31"
    gryphon "I can tell you more than that, if you like. Do you know why it’s called a whiting?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice340"
    alice "I never thought about it. Why?"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon32"
    gryphon "It does the boots and shoes." # solemnly

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    
    show alice disturbed at breathing
    voice "n1470"
    "Alice was thoroughly puzzled."
    show alice surprised at breathing
    voice "alice341"
    alice "Does the boots and shoes!?" # wondering

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon33"
    gryphon "Why, what are your shoes done with? I mean, what makes them so shiny?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "n1471"
    "Alice looked down at them, and considered a little before she gave her answer."
    voice "alice342"
    alice "They’re done with blacking, I believe."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon34"
    gryphon "Boots and shoes under the sea, are done with a whiting. Now you know." # deep voice

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice surprised at breathing
    voice "alice343"
    alice "And what are they made of?" # asked with great curiosity

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon35"
    gryphon "Soles and eels, of course, any shrimp could have told you that."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice344"
    alice "If I’d been the whiting, I’d have said to the porpoise, ‘Keep back, please: we don’t want you with us!’" # still in thoughts

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock48"
    mock "They were obliged to have him with them, no wise fish would go anywhere without a porpoise."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice surprised at breathing
    voice "alice345"
    alice "Wouldn’t it really?" # surprised

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock49"
    mock "Of course not, why, if a fish came to me, and told me he was going a journey, I should say ‘With what porpoise?’"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice disturbed at breathing
    voice "alice346"
    alice "Don’t you mean ‘purpose’?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    show angry at angrily:
        xpos turtle_pos ypos 0.89 xoffset 390 yoffset -620 zoom 0.7
    voice "mock50"
    mock "*offended* I mean what I say."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon36"
    gryphon "Come, let’s hear some of your adventures." 
    hide angry
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice347"
    alice "I could tell you my adventures—beginning from this morning, but it’s no use going back to yesterday, because I was a different person then."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock51"
    mock "Explain all that."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon37"
    gryphon "No, no! The adventures first, explanations take such a dreadful time." # impatient

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "n1472"
    "So Alice began telling them her adventures from the time when she first saw the White Rabbit."
    # get close
    show turtle at breathing:
        ease 1.0 xoffset 555 yoffset 0
    show gryphon at breathing:
        ease 1.0 xoffset 180 yoffset 0
    voice "n1473"
    "She was a little nervous about it just at first, but the two creatures got so close to her, one on each side, and opened their eyes and mouths so very wide, that she gained courage as she went on."
    voice "n1474"
    "Her listeners were perfectly quiet till she got to the part about her repeating “You are old, Father William” to the Caterpillar, and the words all coming different, and then the Mock Turtle drew a long breath, and said:"
    show turtle at breathing:
        ease 0.5 xoffset 0 yoffset 0
    show gryphon at breathing:
        ease 0.5 xoffset 0 yoffset 0
    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock52"
    mock "That’s very curious."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon38"
    gryphon "It’s all about as curious as it can be."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock53"
    mock "It all came different!"
    voice "mock54"
    mock "I should like to hear her try and repeat something now. Tell her to begin."
    voice "n1475"
    "He looked at the Gryphon as if he thought it had some kind of authority over Alice."
    
    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon39"
    gryphon "Stand up and repeat ‘Tis the voice of the sluggard’"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice pout at breathing
    voice "alice348"
    alice "(How the creatures order one about, and make one repeat lessons!)"
    voice "alice349"
    alice "(I might as well be at school at once)"
    show alice thinking at breathing
    voice "n1476"
    "However, she got up, and began to repeat it, but her head was so full of the Lobster Quadrille, that she hardly knew what she was saying, and the words came very queer indeed:—"
    voice "alice350"
    alice "’Tis the voice of the Lobster; \n{space=30}I heard him declare,
    \n“You have baked me too brown, \n{space=30}I must sugar my hair.”
    \nAs a duck with its eyelids, \n{space=30}so he with his nose
    \nTrims his belt and his buttons, \n{space=30}and turns out his toes."

    # later editions continue with
    #a lice "When the sands are all dry, he is gay as a lark,\n
    #And will talk in contemptuous tones of the Shark,"
    #a lice "But, when the tide rises and sharks are around,\n
    #His voice has a timid and tremulous sound."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon40"
    gryphon "That’s different from what I used to say when I was a child."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock55"
    mock "Well, I never heard it before, but it sounds uncommon nonsense."
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice pout at breathing
    voice "n1477"
    "Alice said nothing; she had sat down with her face in her hands, wondering if anything would ever happen in a natural way again."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock56"
    mock "I should like to have it explained."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon41"
    gryphon "She can’t explain it. Go on with the next verse."

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock57"
    mock "But about his toes?" # persistet
    voice "mock58"
    mock "How could he turn them out with his nose, you know?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice thinking at breathing
    voice "alice351"
    alice "It’s the first position in dancing."
    voice "n1478"
    "She was dreadfully puzzled by the whole thing, and longed to change the subject."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon42"
    gryphon "Go on with the next verse, it begins ‘I passed by his garden’."

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    voice "n1479"
    "Alice did not dare to disobey, though she felt sure it would all come wrong, and she went on in a trembling voice:—"
    voice "alice352"
    alice "I passed by his garden, \n{space=30}and marked, with one eye,
    \nHow the Owl and the Panther \n{space=30}were sharing a pie.
    \nThe Panther took pie-crust, \n{space=30}and gravy, and meat,
    \nWhile the Owl had the dish \n{space=30}as its share of the treat."
    voice "alice353"
    alice "When the pie was all finished, \n{space=30}the Owl, as a boon,
    \nWas kindly permitted \n{space=30}to pocket the spoon:
    \nWhile the Panther received \n{space=30}knife and fork with a growl,
    \nAnd concluded the banquet—"


    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock59"
    mock "What is the use of repeating all that stuff, if you don’t explain it as you go on? It’s by far the most confusing thing I ever heard!"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon43"
    gryphon "Yes, I think you’d better leave off."
    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice normal at breathing
    voice "n1480"
    "Alice was only too glad to do so."

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon44"
    gryphon "Shall we try another figure of the Lobster Quadrille?"
    voice "gryphon45"
    gryphon "Or would you like the Mock Turtle to sing you a song?"

    camera:
        ease cam_transition xpos 540 ypos 1020 zoom 2.0 # alice
    show alice happy at breathing
    voice "alice354"
    alice "Oh, a song, please, if the Mock Turtle would be so kind." # alice replied eagerly

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon46"
    gryphon "Hm! No accounting for tastes! Sing her ‘Turtle Soup’, will you, old fellow?"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    stop music fadeout 1.0
    voice "n1481"
    "The Mock Turtle sighed deeply, and began, in a voice sometimes choked with sobs, to sing this:—"
    play music "audio/rinne sad.mp3" fadein 1.0 fadeout 1.0
    voice "mock60"
    mock "Beautiful Soup, so rich and green,\nWaiting in a hot tureen!"
    voice "mock61"
    mock "Who for such dainties would not stoop?\nSoup of the evening, beautiful Soup!"
    voice "mock62"
    mock "Soup of the evening, beautiful Soup!\n
    {space=30}Beau—ootiful Soo—oop!\n
    {space=30}Beau—ootiful Soo—oop!"
    voice "mock63"
    mock "Soo—oop of the e—e—evening,\n
    {space=30}Beautiful, beautiful Soup!"
    voice "mock64"
    mock "Beautiful Soup! Who cares for fish,\n
    Game, or any other dish?"
    voice "mock65"
    mock "Who would not give all else for two p\n
    ennyworth only of beautiful Soup?"
    voice "mock66"
    mock "Pennyworth only of beautiful Soup?\n
    {space=30}Beau—ootiful Soo—oop!\n
    {space=30}Beau—ootiful Soo—oop!"
    voice "mock67"
    mock "Soo—oop of the e—e—evening,\n
    Beautiful, beauti—FUL SOUP!"

    camera:
        ease cam_transition xpos -60 ypos 975 zoom 2.0 # gryphon
    voice "gryphon47"
    gryphon "Chorus again!" # cried

    camera:
        ease cam_transition xpos -120 ypos 0 zoom 1.0 # NEUTRAL
    voice "n1482"
    "The Mock Turtle had just begun to repeat it, when a cry of “The trial’s beginning!” was heard in the distance."

    show gryphon at breathing:
        xzoom -1.0 xpos -0.3
    voice "gryphon48"
    gryphon "Come on!" # cried

    show alice disturbed at breathing:
        pause 2.5
        linear 7.5 xpos 1.54
    show gryphon at breathing:
        linear 10.0 xpos 1.21
    camera:
        zoom 1.0 ypos 0
        linear 10.0 xpos 1530
    voice "n1483"
    "The Gryphon took Alice by the hand, and hurried off, without waiting for the end of the song."
    voice "alice355"
    alice "What trial is it?"
    voice "n1484"
    "Alice panted as she ran."
    voice "gryphon49"
    gryphon "Come on!"
    voice "n1485"
    "He ran faster, while more and more faintly came, carried on the breeze that followed them, the melancholy words:—"

    camera:
        ease cam_transition xpos -700 ypos 1600 zoom 2.0 # turtle
    voice "mock68"
    mock "Soo—oop of the e—e—evening,\n
    {space=30}Beautiful, beautiful Soup!"

label chapter11:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1486"
    "{size=+40}Chapter XI: \n{/size}Who Stole the Tarts?"

    jump ch11_court

label setup_court:
    # geometry
    show court_wall as wall1:
        align (0.0, 1.0) zpos -1000 zoom 1.25

    show court_floor as floor1:
        align (0.5, 0.5) pos(1024, 1.0) xrotate 90.0 zoom 2.0
    show court_floor as floor2:
        align (0.5, 0.5) pos(3072, 1.0) xrotate 90.0 zoom 2.0
    show court_floor as floor3:
        align (0.5, 0.5) pos(5120, 1.0) xrotate 90.0 zoom 2.0

    show court_wall as wallLeft:
        align (1.0, 1.0) pos (2.72, 1.0) zpos 1915.0 zoom 1.25 yrotate 90
    show court_wall as wallRight:
        align (1.0, 1.0) pos (8.13, 1.0) zpos 1915.0 zoom 1.25 yrotate 90


    show jurybox at anchor zorder 10:
        ypos 1.0 xpos court_jury zpos -800 zoom 1.6

    show tarts at anchor zorder 100:
        ypos 1.0 xpos 2585 zpos -65 zoom 0.67

    #show throne as throne1 at anchor:
    #    ypos 1.0 xpos 4185 zpos -920

    #show throne as throne2 at anchor:
    #    ypos 1.0 xpos 3625 zpos -920
    
    # people
    define court_king = 4185
    define court_queen = 3625
    define court_jury = 2285
    define court_bill = 2470
    define court_lory = 2025
    define court_alice = 875
    define court_rabbit = 4635
    define court_witness = 3905
    define court_dormouse = 875
    define court_dormouse2 = 5255
    define court_hare = 600
    define court_knave = 5195

    show king at breathing:
        ypos 1.03 xpos court_king zpos -900
        zoom king_scale

    show queen normal at breathing:
        ypos 1.03 xpos court_queen zpos -900
        zoom queen_scale

    show desc at anchor:
        ypos 1.0 xpos 3905 zpos -850 zoom 1.4

    show rabbit court at breathing:
        ypos 1.0 xpos court_rabbit zpos -800
        zoom rabbit_scale

    show soldier9 as soldier1 at anchor:
        ypos 1.0 xpos 5095 zpos -520
        zoom 1.0

    show knave at anchor:
        ypos 1.0 xpos court_knave zpos -400
        zoom 1.0

    show soldier9 as soldier2 at anchor:
        ypos 1.0 xpos 5480 zpos -365
        zoom 1.0

    # jurors
    show bill at breathing zorder 5:
        ypos 1.0 xpos court_bill zpos -850 zoom 1.0

    show lory at breathing zorder 5:
        ypos 0.75 xpos court_lory zpos -850 zoom 0.4

    # observers
    show gryphon at breathing zorder 5:
        ypos 1.0 xpos 650 zpos -800 zoom gryphon_scale xzoom -1.0

    show alice normal at breathing zorder 10:
        ypos 1.0 xpos court_alice zpos -700 zoom alice_scale

    return

label ch11_court:
    call setup_court
    play music "audio/rinne lilly.mp3" fadein 1.0 fadeout 1.0
    camera:
        perspective True
        xpos 3905 xoffset -center_offset
    voice "n1487"
    "The King and Queen of Hearts were seated on their throne when they arrived, with a great crowd assembled about them—all sorts of little birds and beasts, as well as the whole pack of cards:"
    camera:
        ease cam_transition xpos 4730
    voice "n1488"
    "The Knave was standing before them, in chains, with a soldier on each side to guard him; and near the King was the White Rabbit, with a trumpet in one hand, and a scroll of parchment in the other."
    camera:
        ease cam_transition xpos 2560 ypos 300 # tarts
    voice "n1489"
    "In the very middle of the court was a table, with a large dish of tarts upon it: they looked so good, that it made Alice quite hungry to look at them—"
    voice "alice356"
    alice "(I wish they’d get the trial done and hand round the refreshments!)"
    voice "n1490"
    "But there seemed to be no chance of this, so she began looking at everything about her, to pass away the time."
    voice "n1491"
    "Alice had never been in a court of justice before, but she had read about them in books, and she was quite pleased to find that she knew the name of nearly everything there."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000
    voice "alice357"
    alice "(That’s the judge, because of his great wig)"
    voice "n1492"
    "The judge, by the way, was the King; and as he wore his crown over the wig, he did not look at all comfortable, and it was certainly not becoming." # (look at the frontispiece if you want to see how he did it,)

    camera:
        ease cam_transition xpos court_jury ypos 0 zpos -500
    voice "alice358"
    alice "(And that’s the jury-box and those twelve creatures—"
    voice "n1493"
    "(she was obliged to say “creatures,” you see, because some of them were animals, and some were birds)"
    voice "alice359"
    alice "(I suppose they are the jurors)"
    voice "n1494"
    "She said this last word two or three times over to herself, being rather proud of it: for she thought, and rightly too, that very few little girls of her age knew the meaning of it at all."
    voice "n1495"
    "However, “jury-men” would have done just as well."
    voice "n1496"
    "The twelve jurors were all writing very busily on slates."

    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500
    show alice thinking at breathing
    voice "alice360"
    alice "*whispering* What are they doing? They can’t have anything to put down yet, before the trial’s begun." # Alice whispered to the Gryphon. “”

    voice "gryphon50"
    gryphon "*whispering* They’re putting down their names, for fear they should forget them before the end of the trial."
    show alice disturbed at breathing
    voice "alice361"
    alice "Stupid things!" # Alice began in a loud, indignant voice, but she stopped hastily, for the White Rabbit cried out, 
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -500
    
    voice "rabbit24"
    rabbit "Silence in the court!"
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -500
    show alice thinking at breathing
    voice "n1497"
    "The King put on his spectacles and looked anxiously round, to make out who was talking."

    camera:
        ease cam_transition xpos court_jury ypos 0 zpos -500
    voice "n1498"
    "Alice could see, as well as if she were looking over their shoulders, that all the jurors were writing down “stupid things!” on their slates, and she could even make out that one of them didn’t know how to spell “stupid” and that he had to ask his neighbour to tell him."
    voice "alice362"
    alice "(A nice muddle their slates’ll be in before the trial’s over!)"
    
    show alice disturbed at breathing zorder 1:
        ease 1.0 zpos -900 xpos 1525
    voice "n1499"
    "One of the jurors had a pencil that squeaked."

    show alice disturbed at breathing zorder 1:
        ease 1.0 zpos -900 xpos court_bill
    voice "n1500"
    "This of course, Alice could not stand, and she went round the court and got behind him, and very soon found an opportunity of taking it away."

    show alice normal at breathing zorder 1:
        ease 1.0 zpos -900 xpos court_alice
    voice "n1501"
    "She did it so quickly that the poor little juror (it was Bill, the Lizard) could not make out at all what had become of it; so, after hunting all about for it, he was obliged to write with one finger for the rest of the day; and this was of very little use, as it left no mark on the slate."

    # reset alice pos
    show alice normal at breathing zorder 10:
        ypos 1.0 xpos 875 zpos -700 zoom alice_scale
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000
    voice "king09"
    king "Herald, read the accusation!"
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    
    play sound "sfx/fanfare.mp3"
    voice "n1502"
    "On this the White Rabbit blew three blasts on the trumpet, and then unrolled the parchment scroll, and read as follows:—"
    voice "rabbit25"
    rabbit "The Queen of Hearts, she made some tarts,
    \n{space=30}All on a summer day:
    \nThe Knave of Hearts, he stole those tarts,
    \n{space=30}And took them quite away!"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000
    voice "king10"
    king "Consider your verdict."
    #"The King said to the jury."
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000
    voice "rabbit26"
    rabbit "Not yet, not yet! There’s a great deal to come before that!"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000
    voice "king11"
    king "Call the first witness."

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000
    play sound "sfx/fanfare.mp3"
    voice "n1503"
    "The White Rabbit blew three blasts on the trumpet."
    voice "rabbit27"
    rabbit "First witness!"

    show hatter normal at breathing:
        ypos 1.0 xpos court_witness zoom hatter_scale zpos -350
    camera:
        ease cam_transition xpos court_witness ypos 0 zpos 0
    voice "n1504"
    "The first witness was the Hatter."
    voice "n1505"
    "He came in with a teacup in one hand and a piece of bread-and-butter in the other."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter35"
    hatter "I beg pardon, your Majesty, for bringing these in: but I hadn’t quite finished my tea when I was sent for."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king12"
    king "You ought to have finished. When did you begin?"

    # dormouse and march hare
    show dormouse tired at breathing zorder 15:
        ypos 1.0 xpos court_dormouse zoom dormouse_scale zpos -600 xzoom -1.0
    show hare at breathing zorder 20:
        ypos 1.0 xpos court_hare zoom hare_scale zpos -500
    
    camera:
        ease cam_transition xpos court_hare ypos 365 zpos -500 # hare
    voice "n1506"
    "The Hatter looked at the March Hare, who had followed him into the court, arm-in-arm with the Dormouse."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter36"
    hatter "Fourteenth of March, I think it was."

    camera:
        ease cam_transition xpos court_hare ypos 365 zpos -500 # hare
    voice "hare15"
    hare "Fifteenth."
    
    camera:
        ease cam_transition xpos court_dormouse ypos 700 zpos -880 # dormouse
    voice "dormouse17"
    dormouse "Sixteenth."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king13"
    king "Write that down."

    camera:
        ease cam_transition xpos court_jury ypos 0 zpos -500 # jury
    voice "n1507"
    "The jury eagerly wrote down all three dates on their slates, and then added them up, and reduced the answer to shillings and pence."
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king14"
    king "Take off your hat."
    
    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter37"
    hatter "It isn’t mine."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king15"
    king "Stolen!"

    camera:
        ease cam_transition xpos court_jury ypos 0 zpos -500 # jury
    voice "n1508"
    "The king turned to the jury, who instantly made a memorandum of the fact."
    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter38"
    hatter "I keep them to sell. I’ve none of my own. I’m a hatter."
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    show hatter scared at breathing
    voice "n1509"
    "Here the Queen put on her spectacles, and began staring at the Hatter, who turned pale and fidgeted."
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king16"
    king "Give your evidence and don’t be nervous, or I’ll have you executed on the spot."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "n1510"
    "This did not seem to encourage the witness at all: he kept shifting from one foot to the other, looking uneasily at the Queen, and in his confusion he bit a large piece out of his teacup instead of the bread-and-butter."

    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    show alice thinking at breathing:
        easeout 30.0 zoom 0.7
    voice "n1511"
    "Just at this moment Alice felt a very curious sensation, which puzzled her a good deal until she made out what it was: she was beginning to grow larger again, and she thought at first she would get up and leave the court; but on second thoughts she decided to remain where she was as long as there was room for her."

    camera:
        ease cam_transition xpos court_dormouse ypos 700 zpos -880 # dormouse
    voice "dormouse18"
    dormouse "I wish you wouldn’t squeeze so. I can hardly breathe." # dormouse whi is sitting next to her

    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    voice "alice363"
    alice "I can’t help it, I’m growing." # meekly

    camera:
        ease cam_transition xpos court_dormouse ypos 700 zpos -880 # dormouse
    voice "dormouse19"
    dormouse "You’ve no right to grow here..."
    
    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    voice "alice364"
    alice "Don’t talk nonsense, you know you’re growing too."
    
    camera:
        ease cam_transition xpos court_dormouse ypos 700 zpos -880 # dormouse
    voice "dormouse20"
    dormouse "Yes, but I grow at a reasonable pace, not in that ridiculous fashion."
    
    show dormouse sleep at breathing:
        ease 10 ypos 1.0 xpos court_dormouse2 zpos -260 zoom dormouse_scale xzoom 1.0
    voice "n1512"
    "He got up very sulkily and crossed over to the other side of the court."

    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    voice "n1513"
    "All this time the Queen had never left off staring at the Hatter, and, just as the Dormouse crossed the court, she said to one of the officers of the court:"
    voice "queen30"
    queen "Bring me the list of the singers in the last concert!"

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "n1514"
    "On which the wretched Hatter trembled so, that he shook both his shoes off."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king17"
    king "*angry* Give your evidence, or I’ll have you executed, whether you’re nervous or not."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter39"
    hatter "*trembling* I’m a poor man, your Majesty, —and I hadn’t begun my tea—not above a week or so—and what with the bread-and-butter getting so thin—and the twinkling of the tea—"
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king18"
    king "The twinkling of the what?"

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter40"
    hatter "It began with the tea."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king19"
    king "Of course twinkling begins with a T!"
    voice "king20"
    king "Do you take me for a dunce? Go on!"
    
    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter41"
    hatter "I’m a poor man, and most things twinkled after that—only the March Hare said—"

    camera:
        ease cam_transition xpos court_hare ypos 365 zpos -500 # hare
    voice "hare16"
    hare "I didn’t!" # interrupted in great hurry

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter42"
    hatter "You did!"

    camera:
        ease cam_transition xpos court_hare ypos 365 zpos -500 # hare
    voice "hare17"
    hare "I deny it!"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king21"
    king "He denies it, —leave out that part."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter43"
    hatter "Well, at any rate, the Dormouse said—"
    
    camera:
        ease cam_transition xpos court_dormouse2 ypos 700 zpos -580 # dormouse2
    voice "n1515"
    "The Hatter went on, looking anxiously round to see if he would deny it too: but the Dormouse denied nothing, being fast asleep."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter44"
    hatter "After that, I cut some more bread-and-butter—"

    camera:
        ease cam_transition xpos court_lory ypos 0 zpos -1000
    voice "lory6"
    lory "But what did the Dormouse say?" # one of the jurors

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter45"
    hatter "That I can’t remember."
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king22"
    king "You must remember, or I’ll have you executed."
    voice "n1516"
    "The miserable Hatter dropped his teacup and bread-and-butter, and went down on one knee."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter46"
    hatter "I’m a poor man, your Majesty."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king23"
    king "You’re a very poor speaker."
    voice "n1517"
    "Here one of the guinea-pigs cheered, and was immediately suppressed by the officers of the court."
    voice "n1518"
    "(As that is rather a hard word, I will just explain to you how it was done. They had a large canvas bag, which tied up at the mouth with strings: into this they slipped the guinea-pig, head first, and then sat upon it)"

    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    show alice happy at breathing
    voice "alice365"
    alice "(I’m glad I’ve seen that done. I’ve so often read in the newspapers, at the end of trials, “There was some attempts at applause, which was immediately suppressed by the officers of the court,” and I never understood what it meant till now)"
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king24"
    king "If that’s all you know about it, you may stand down."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter47"
    hatter "I can’t go no lower, I’m on the floor, as it is."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king25"
    king "Then you may sit down."
    voice "n1519"
    "Here the other guinea-pig cheered, and was suppressed."

    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    voice "alice366"
    alice "(Come, that finished the guinea-pigs! Now we shall get on better)"

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    voice "hatter48"
    hatter "I’d rather finish my tea."
    voice "n1520"
    "The hatter looked anxiously at the Queen, who was reading the list of singers."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king26"
    king "You may go."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # hatter
    show hatter scared at breathing:
        linear 3.0 xpos 500
    voice "n1521"
    "The Hatter hurriedly left the court, without even waiting to put his shoes on."

    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # king
    voice "queen31"
    queen "—and just take his head off outside!" # the Queen added to one of the officers:
    hide hatter

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # neutral
    voice "n1522"
    "But the Hatter was out of sight before the officers could get to the door."
    "..."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king27"
    king "Call the next witness!"

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # neutral
    show cook at breathing:
        ypos 1.0 xpos court_witness zoom cook_scale zpos -350
    voice "n1523"
    "The next witness was the Duchess’s cook."
    voice "n1524"
    "She carried the pepper-box in her hand, and Alice guessed who it was, even before she got into the court, by the way the people near the door began sneezing all at once."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king28"
    king "Give your evidence."

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # cook
    voice "cook1"
    cook "Shan’t."

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "n1525"
    "The King looked anxiously at the White Rabbit:"
    voice "rabbit28"
    rabbit "*whispering* Your Majesty must cross-examine this witness."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king29"
    king "Well, if I must, I must."
    voice "n1527"
    "After folding his arms and frowning at the cook till his eyes were nearly out of sight, he said in a deep voice:"
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king30"
    king "What are tarts made of?"

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # cook
    voice "cook2"
    cook "Pepper, mostly."

    camera:
        ease cam_transition xpos court_dormouse2 ypos 700 zpos -580 # dormouse2
    voice "dormouse21"
    dormouse "Treacle." # sleepy voice
    
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    show queen angry at breathing
    voice "queen32"
    queen "*shriek* Collar that Dormouse! Behead that Dormouse! Turn that Dormouse out of court! Suppress him! Pinch him! Off with his whiskers!"

    hide dormouse
    hide cook

    camera:
        ease cam_transition xpos court_witness ypos 0 zpos -500 # neutral
    voice "n1528"
    "For some minutes the whole court was in confusion, getting the Dormouse turned out, and, by the time they had settled down again, the cook had disappeared."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    show queen normal at breathing
    voice "king31"
    king "Never mind!" # said the King, with an air of great relief. 
    voice "king32"
    king "Call the next witness."
    camera:
        ease cam_transition xpos 3905 ypos 0 zpos -1000
    voice "n1529"
    "And he added in an undertone to the Queen:"
    voice "king33"
    king "Really, my dear, you must cross-examine the next witness. It quite makes my forehead ache!"

    show alice thinking at breathing
    camera:
        ease cam_transition xpos court_alice ypos 0 zpos -500 # alice
    voice "n1530"
    "Alice watched the White Rabbit as he fumbled over the list, feeling very curious to see what the next witness would be like."
    voice "alice367"
    alice "(They haven’t got much evidence yet)"
    voice "n1531"
    "Imagine her surprise, when the White Rabbit read out, at the top of his shrill little voice, the name:"

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit29"
    rabbit "Alice!"

label chapter12:
    $ persistent.started_story = True
    scene black
    call reset_camera
    voice "n1532"
    "{size=+40}Chapter XII: \n{/size}Alice's Evidence"

    call setup_court
    play music "audio/rinne lilly.mp3" if_changed
    camera:
        perspective True
        xpos 3905 xoffset -center_offset
        ease cam_transition xpos 1475 ypos 0 zpos 0 # alice
    
    show alice excited at breathing:
        zoom 1.0
    voice "alice368"
    alice "Here!"

    show alice normal at breathing:
        pause 1.0
        linear 2.0 xpos court_witness

    show jurybox at anchor:
        pause 1.5
        ease 1.0 zrotate 180

    show lory at anchor:
        pause 1.5
        ease 1.0 zrotate 90

    show bill at anchor:
        pause 1.5
        ease 1.0 zrotate 90


    #"Cried Alice, quite forgetting in the flurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldfish she had accidentally upset the week before."
    voice "n1533"
    "Alice forgot in the flurry of the moment how large she had grown in the last few minutes, and she jumped up in such a hurry that she tipped over the jury-box with the edge of her skirt, upsetting all the jurymen on to the heads of the crowd below, and there they lay sprawling about, reminding her very much of a globe of goldfish she had accidentally upset the week before."

    show alice surprised at breathing:
        ease 1.0 xpos 2030
    camera:
        ease cam_transition xpos court_jury # jury
    voice "alice369"
    alice "Oh, I beg your pardon!"
    show lory at breathing:
        ease 1.0 zrotate 0

    show bill at breathing:
        pause 0.5
        ease 1.0 zrotate 180
    voice "n1534"
    "She began picking them up again as quickly as she could, for the accident of the goldfish kept running in her head, and she had a vague sort of idea that they must be collected at once and put back into the jury-box, or they would die."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king34"
    king "The trial cannot proceed, until all the jurymen are back in their proper places." # tone of great dismay
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1200 # king zoom
    voice "king35"
    king "All!"
    voice "n1535"
    "He repeated the last word with great emphasis, looking hard at Alice as he said so."
    
    camera:
        ease cam_transition xpos court_bill zpos -1000 ypos 300 # jury bill
    voice "n1536"
    "Alice looked at the jury-box, and saw that, in her haste, she had put the Lizard in head downwards, and the poor little thing was waving its tail about in a melancholy way, being quite unable to move."
    show bill at breathing:
        ease 1.0 zrotate 0
    voice "n1537"
    "She soon got it out again, and put it right."
    voice "alice370"
    alice "(not that it signifies much)" 
    voice "alice371"
    alice "(I should think it would be quite as much use in the trial one way up as the other)"

    show alice thinking at breathing:
        ease 1.0 xpos court_witness zpos -350
    voice "n1538"
    "As soon as the jury had a little recovered from the shock of being upset, and their slates and pencils had been found and handed back to them, they set to work very diligently to write out a history of the accident, all except the Lizard, who seemed too much overcome to do anything but sit with its mouth open, gazing up into the roof of the court."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king36"
    king "What do you know about this business?"

    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice witness
    voice "alice372"
    alice "Nothing."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king37"
    king "Nothing whatever?" # persisted the King.

    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice
    show alice pout at breathing:
        xpos court_witness zpos -350 
    voice "alice373"
    alice "Nothing whatever."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king38"
    king "That’s very important."

    camera:
        ease cam_transition xpos court_jury ypos 0 zpos -900 # jury
    voice "n1539"
    "The king turned to the jury."
    voice "n1540"
    "They were just beginning to write this down on their slates, when the White Rabbit interrupted:"

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit44"
    rabbit "Unimportant, your Majesty means, of course."
    voice "n1541"
    "He said in a very respectful tone, but frowning and making faces at him as he spoke."
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king39"
    king "Unimportant, of course, I meant."
    voice "n1542"
    "The King  went on to himself in an undertone:"
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1200 # king zoom
    voice "king40"
    king "(important—unimportant—unimportant—important—)"
    voice "n1543"
    "As if he were trying which word sounded best."
    voice "n1544"
    "Some of the jury wrote it down “important,” and some “unimportant.”"
    
    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice 
    show alice thinking at breathing
    voice "n1545"
    "Alice could see this, as she was near enough to look over their slates."
    voice "alice374"
    alice "(But it doesn’t matter a bit...)"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "n1546"
    "At this moment the King, who had been for some time busily writing in his note-book, cackled out:"
    voice "king41"
    king "Silence!"
    voice "n1547"
    "And he read out from his book:"
    voice "king42"
    king "Rule Forty-two. All persons more than a mile high have to leave the court."
    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice 
    voice "n1548"
    "Everybody looked at Alice."

    show alice pout at breathing
    voice "alice375"
    alice "I’m not a mile high."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king43"
    king "You are."
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    show queen happy at breathing
    voice "queen33"
    queen "Nearly two miles high."

    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice 
    show queen normal at breathing
    show alice joking at breathing
    voice "alice376"
    alice "Well, I shan’t go, at any rate, besides, that’s not a regular rule: you invented it just now."
    
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king44"
    king "It’s the oldest rule in the book."

    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice 
    show alice pout at breathing
    voice "alice377"
    alice "Then it ought to be Number One."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    show king scared  at breathing
    voice "n1549"
    "The King turned pale, and shut his note-book hastily."
    voice "king45"
    king "Consider your verdict."
    voice "n1550"
    "He said to the jury, in a low, trembling voice."

    # hide alice because of clipping
    hide alice
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit30"
    rabbit "There’s more evidence to come yet, please your Majesty."
    voice "n1551"
    "The White Rabbit was jumping up in a great hurry."
    voice "rabbit31"
    rabbit "This paper has just been picked up."

    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    voice "queen34"
    queen "What’s in it?"

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit32"
    rabbit "I haven’t opened it yet, but it seems to be a letter, written by the prisoner to—to somebody."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    show king at breathing
    voice "king46"
    king "It must have been that, unless it was written to nobody, which isn’t usual, you know."

    camera:
        ease cam_transition xpos court_bill zpos -1000 ypos 300 # jury bill
    voice "bill2"
    bill "Who is it directed to?" # said one of the jurymen.

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit33"
    rabbit "It isn’t directed at all, in fact, there’s nothing written on the outside."
    voice "n1552"
    "He unfolded the paper as he spoke."
    voice "rabbit34"
    rabbit "It isn’t a letter, after all: it’s a set of verses."

    camera:
        ease cam_transition xpos court_lory zpos -1000 ypos 300 # jury lory
    voice "lory7"
    lory "Are they in the prisoner’s handwriting?" # asked another of the jurymen.

    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit35"
    rabbit "No, they’re not, and that’s the queerest thing about it."

    camera:
        ease cam_transition xpos court_jury zpos -900 ypos 0 # jury
    voice "n1553"
    "(The jury all looked puzzled)"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king47"
    king "He must have imitated somebody else’s hand."
    voice "n1554"
    "(The jury all brightened up again)"

    
    camera:
        ease cam_transition xpos court_knave ypos 0 zpos -500 # knave
    voice "knave1"
    knave "Please your Majesty, I didn’t write it, and they can’t prove I did: there’s no name signed at the end."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king48"
    king "If you didn’t sign it, that only makes the matter worse. You must have meant some mischief, or else you’d have signed your name like an honest man."
    voice "n1555"
    "There was a general clapping of hands at this: it was the first really clever thing the King had said that day."
    
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    voice "queen35"
    queen "That proves his guilt."

    show alice pout at breathing:
        ypos 1.0 xpos court_witness zpos -350
    camera:
        ease cam_transition xpos court_witness ypos -315 zpos -500 # alice 
    voice "alice378"
    alice "It proves nothing of the sort!"
    show alice disturbed at breathing
    voice "alice379"
    alice "Why, you don’t even know what they’re about!"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king49"
    king "Read them."

    hide alice # because of clipping
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "n1556"
    "The White Rabbit put on his spectacles."
    voice "rabbit36"
    rabbit "Where shall I begin, please your Majesty?"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king50"
    king "Begin at the beginning, and go on till you come to the end: then stop."
    #"These were the verses the White Rabbit read:—"
    
    camera:
        ease cam_transition xpos court_rabbit ypos 500 zpos -1000 # rabbit
    voice "rabbit37"
    rabbit "They told me you had been to her,\n{space=30}And mentioned me to him:\nShe gave me a good character,\n{space=30}But said I could not swim."
    voice "rabbit38"
    rabbit "He sent them word I had not gone\n{space=30}(We know it to be true):\nIf she should push the matter on,\n{space=30}What would become of you?"
    voice "rabbit39"
    rabbit "I gave her one, they gave him two,\n{space=30}You gave us three or more;\nThey all returned from him to you,\n{space=30}Though they were mine before."
    voice "rabbit40"
    rabbit "If I or she should chance to be\n{space=30}Involved in this affair,\nHe trusts to you to set them free,\n{space=30}Exactly as we were."
    voice "rabbit41"
    rabbit "My notion was that you had been\n{space=30}(Before she had this fit)\nAn obstacle that came between\n{space=30}Him, and ourselves, and it."
    voice "rabbit42"
    rabbit "Don’t let him know she liked them best,\n{space=30}For this must ever be\nA secret, kept from all the rest,\n{space=30}Between yourself and me."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king51"
    king "That’s the most important piece of evidence we’ve heard yet." #,” said the King, rubbing his hands; 
    voice "king52"
    king "So now let the jury—"

    show alice pout at breathing:
        ypos 1.0 xpos court_witness zpos -350 zoom 1.3
    camera:
        ease cam_transition xpos court_witness ypos -800 zpos -500 # alice 
    voice "alice380"
    alice "If any one of them can explain it I’ll give him sixpence. I don’t believe there’s an atom of meaning in it."
    voice "n1557"
    "(she had grown so large in the last few minutes that she wasn’t a bit afraid of interrupting him)"

    camera:
        ease cam_transition xpos court_jury zpos -900 ypos 0 # jury
    voice "n1558"
    "The jury all wrote down on their slates: “She doesn’t believe there’s an atom of meaning in it”, but none of them attempted to explain the paper."
    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king53"
    king "If there’s no meaning in it, that saves a world of trouble, you know, as we needn’t try to find any."
    voice "king54"
    king "And yet I don’t know..."
    voice "n1559"
    "He went on, spreading out the verses on his knee, and looking at them with one eye."
    voice "king55"
    king "I seem to see some meaning in them, after all. “—said I could not swim—” you can’t swim, can you?"

    hide alice
    camera:
        ease cam_transition xpos court_knave ypos 0 zpos -500 # knave
    voice "n1560"
    "He turned to the Knave."
    voice "n1561"
    "The Knave shook his head sadly."
    voice "knave2"
    knave "Do I look like it?"
    voice "n1562"
    "(He certainly did not, being made entirely of cardboard)"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king56"
    king "All right, so far."
    voice "n1563"
    "The King went on muttering over the verses to himself:"
    voice "king57"
    king "‘We know it to be true—’ that’s the jury, of course—‘I gave her one, they gave him two—’ why, that must be what he did with the tarts, you know—” "

    show alice disturbed at breathing:
        ypos 1.0 xpos court_witness zpos -350 zoom 1.3
    camera:
        ease cam_transition xpos court_witness ypos -800 zpos -500 # alice 
    voice "alice381"
    alice "But, it goes on ‘they all returned from him to you’"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king58"
    king "Why, there they are!"

    camera:
        ease cam_transition xpos 2560 ypos 300 zpos 0 # tarts
    voice "n1564"
    "The King triumphantly pointed to the tarts on the table."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king59"
    king "Nothing can be clearer than that. Then again—‘before she had this fit—’ you never had fits, my dear, I think?"
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    show queen angry at breathing
    voice "queen36"
    queen "Never!"

    camera:
        ease cam_transition xpos court_bill zpos -1000 ypos 300 # jury bill
    voice "n1565"
    "Said the Queen furiously, throwing an inkstand at the Lizard as she spoke."
    voice "n1566"
    "(The unfortunate little Bill had left off writing on his slate with one finger, as he found it made no mark; but he now hastily began again, using the ink, that was trickling down his face, as long as it lasted)"

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    show queen normal at breathing
    voice "king60"
    king "Then the words don’t fit you."
    voice "n1570"
    "The King was looking round the court with a smile."
    "..."
    voice "n1571"
    "There was a dead silence."

    camera:
        ease cam_transition xpos court_king ypos 0 zpos -1000 # king
    voice "king61"
    king "*offended* It’s a pun!" 
    voice "n1572"
    "Everybody laughed."
    voice "king62"
    king "Let the jury consider their verdict."
    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    voice "queen37"
    queen "No, no! Sentence first—verdict afterwards."
    
    camera:
        ease cam_transition xpos court_witness ypos -800 zpos -500 # alice
    show alice pout at breathing 
    voice "alice382"
    alice "Stuff and nonsense!"
    show alice disturbed at breathing
    voice "alice383"
    alice "The idea of having the sentence first!"

    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    show queen angry at breathing
    voice "queen38"
    queen "Hold your tongue!"
    voice "n1573"
    "The queen turned purple."

    camera:
        ease cam_transition xpos court_witness ypos -800 zpos -500 # alice
    show alice pout 
    voice "alice384"
    alice "I won’t!"

    camera:
        ease cam_transition xpos court_queen ypos 0 zpos -1000 # queen
    voice "queen39"
    queen "Off with her head!"
    voice "n1574"
    "The Queen shouted at the top of her voice."
    voice "n1575"
    "Nobody moved."

    camera:
        ease cam_transition xpos court_witness ypos -900 zpos -500 # alice 
    show alice joking at breathing:
        zoom 1.5
    voice "alice385"
    alice "Who cares for you?"
    voice "n1576"
    "(Alice had grown to her full size by this time)"
    voice "alice386"
    alice "You’re nothing but a pack of cards!"

    camera:
        ease 0.5 zrotate -0.1
        ease 0.5 zrotate 0.1
        repeat
    show alice surprised at breathing
    voice "n1577"
    "At this the whole pack rose up into the air, and came flying down upon her: she gave a little scream, half of fright and half of anger, and tried to beat them off, and found herself lying on the bank, with her head in the lap of her sister, who was gently brushing away some dead leaves that had fluttered down from the trees upon her face."

    scene black
    call reset_camera
    stop music fadeout 1.0

    voice "sister1"
    sister "Wake up, Alice dear!"

    scene sister_cg with dissolve
    play music "audio/rinne sad.mp3"
    camera:
        ease 3.0 zrotate -0.1
        ease 3.0 zrotate 0.1
        repeat
    voice "sister2"
    sister "Why, what a long sleep you’ve had!"
    voice "alice387"
    alice "Oh, I’ve had such a curious dream!" 
    voice "n1578"
    "She told her sister, as well as she could remember them, all these strange Adventures of hers that you have just been reading about; and when she had finished, her sister kissed her."
    voice "sister3"
    sister "It was a curious dream, dear, certainly: but now run in to your tea; it’s getting late."
    voice "n1579"
    "So Alice got up and ran off, thinking while she ran, as well she might, what a wonderful dream it had been."
    voice "n1580"
    "But her sister sat still just as she left her, leaning her head on her hand, watching the setting sun, and thinking of little Alice and all her wonderful Adventures, till she too began dreaming after a fashion, and this was her dream:—"

    voice "na01"
    "First, she dreamed of little Alice herself, and once again the tiny hands were clasped upon her knee, and the bright eager eyes were looking up into hers."
    voice "na02"
    "She could hear the very tones of her voice, and see that queer little toss of her head to keep back the wandering hair that would always get into her eyes."
    voice "na03"
    "And still as she listened, or seemed to listen, the whole place around her became alive with the strange creatures of her little sister’s dream."
    voice "na04"
    "The long grass rustled at her feet as the White Rabbit hurried by."
    voice "na05"
    "The frightened Mouse splashed his way through the neighbouring pool."
    voice "na06"
    "She could hear the rattle of the teacups as the March Hare and his friends shared their never-ending meal, and the shrill voice of the Queen ordering off her unfortunate guests to execution."
    voice "na07"
    "Once more the pig-baby was sneezing on the Duchess’s knee, while plates and dishes crashed around it."
    voice "na08"
    "Once more the shriek of the Gryphon, the squeaking of the Lizard’s slate-pencil, and the choking of the suppressed guinea-pigs, filled the air, mixed up with the distant sobs of the miserable Mock Turtle."
    voice "na09"
    "So she sat on, with closed eyes, and half believed herself in Wonderland, though she knew she had but to open them again, and all would change to dull reality."
    voice "na10"
    "The grass would be only rustling in the wind, and the pool rippling to the waving of the reeds."
    voice "na11"
    "The rattling teacups would change to tinkling sheep-bells, and the Queen’s shrill cries to the voice of the shepherd boy."
    voice "na12"
    "And the sneeze of the baby, the shriek of the Gryphon, and all the other queer noises, would change (she knew) to the confused clamour of the busy farm-yard."
    voice "na13"
    "While the lowing of the cattle in the distance would take the place of the Mock Turtle’s heavy sobs."
    voice "na14"
    "Lastly, she pictured to herself how this same little sister of hers would, in the after-time, be herself a grown woman; and how she would keep, through all her riper years, the simple and loving heart of her childhood:"
    voice "na15"
    "And how she would gather about her other little children, and make their eyes bright and eager with many a strange tale, perhaps even with the dream of Wonderland of long ago: and how she would feel with all their simple sorrows, and find a pleasure in all their simple joys, remembering her own child-life, and the happy summer days."

    scene black
    call reset_camera
    voice "na16"
    "The End."
    $ persistent.started_story = False # reset story
    call screen credits
    return

label autoload:
    if persistent.started_story and renpy.can_load("auto-1"):
        $ renpy.load("auto-1")
    else:
        $ persistent.started_story = True
        jump start
    return
