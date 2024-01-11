﻿init python:
    renpy.register_shader("game.breathing", variables="""
        uniform float u_time;
        uniform vec2 res0;
    """, fragment_300="""
        float rng = dot(texture2D(tex0, vec2(0.5), 10.0).xyz, vec3(0.33)); // random offset for each texture
        float scale = 0.5 + 0.5 * sin(u_time + rng * 2.0 * 3.141);
        vec2 texC = v_tex_coord.xy;
        texC.y = 1.0 - (1.0 - texC.y) * (1.0 + 0.01 * scale);
        if(texC.y < 0.0 || texC.y > 1.0) discard;

        gl_FragColor = texture2D(tex0, texC, -0.55);
    """)
    #renpy.register_shader("game.cat", variables="""
    #    uniform float u_time;
    #    uniform sampler2D tex1;
    #    uniform float u_dissolve;
    #""", fragment_400="""
    #    vec2 d = texture(tex1, v_tex_coord, -0.5).xy;
    #    float alpha = 1.0 - clamp((u_dissolve - d.x) / max(d.y - d.x, 0.001), 0.#0, 1.0);
    #    gl_FragColor = texture2D(tex0, v_tex_coord, -0.5);
    #    gl_FragColor.a *= alpha;
    #""")

define alice = Character("Alice", color="#ADD8E6")
define rabbit = Character("Rabbit", color="#ffffff")
define mouse = Character("Mouse", color="#adadad")
define lory = Character("Lory", color="#8c00ff")
define duck = Character("Duck", color="#ff8c00")
define dodo = Character("Dodo", color="#008cff")
define eaglet = Character("Eaglet", color="#be8200")
define everyone = Character("Everyone", color="#ffffff")
define old_crab = Character("Old Crab", color="#ff8c00")
define young_crab = Character("Young Crab", color="#ff8c00")
define magpie = Character("Magpie", color="#ffffff")
define canary = Character("Canary", color="#ffe600")
define pat = Character("Pat", color="#00ff00")
define anon = Character("???", color="#ffffff")
define bill = Character("Bill", color="#0400ff")
define caterpillar = Character("Caterpillar", color="#5cffc9")
define pigeon = Character("Pigeon", color="#adadad")
define fishfoot = Character("Fish-Footmen", color="#9694ff")
define frogfoot = Character("Frog-Footmen", color="#b5ff9e")
define duchess = Character("Duchess", color="#ff8c00")
define cat = Character("Cheshire Cat", color="#fa6400")

image riverbank = "riverbank.png"

default alice_scale = 0.5
default alice_scale_large = 0.7
default alice_scale_muddy = 0.4
default rabbit_scale = 0.7
define mouse_scale = 0.5
define mouse_muddy_scale = 0.3
define lory_scale = 0.3
define duck_scale = 0.4
define dodo_scale = 0.7
define eaglet_scale = 0.45
define old_crab_scale = 0.3
define young_crab_scale = 0.2
define magpie_scale = 0.35
define canary_scale = 0.2

define cam_transition = 0.5
define center_offset = 540 # half of 1080

define repeat_rate = 1.0 / 30.0

transform falling:
    xpos -0.5 ypos 0.0
    linear 1.0 xoffset -20 yoffset -20 rotate 5
    linear 1.0 xoffset 20 yoffset 20 rotate -5
    linear 1.0 xoffset -20 yoffset 20 rotate 5
    linear 1.0 xoffset 20 yoffset -20 rotate -5
    repeat

transform falling2:
    xpos -0.2 ypos 0.1
    linear 1.0 xoffset -10 yoffset -10 rotate 2
    linear 1.0 xoffset 10 yoffset 10 rotate -2
    linear 1.0 xoffset -10 yoffset 10 rotate 2
    linear 1.0 xoffset 10 yoffset -10 rotate -2
    repeat

transform pan_background:
    xalign 0.0
    linear 30.0 xalign 1.0
    linear 30.0 xalign 0.0
    repeat

transform breathing_calm(xposition, scale = 1.0):
    pos (xposition, 0.7)
    anchor (0.5, 1.0)
    zoom scale
    # todo slower speed
    shader "game.breathing"
    pause repeat_rate
    repeat

transform breathing(xposition, scale = 1.0, yposition = 0.7):
    pos (xposition, yposition)
    anchor (0.5, 1.0)
    zoom scale
    shader "game.breathing"
    pause repeat_rate
    repeat

transform breathing_crying(xposition, scale = 1.0):
    pos (xposition, 0.7)
    anchor (0.5, 1.0)
    zoom scale
    # todo custom breathing?
    shader "game.breathing"
    pause repeat_rate
    repeat

transform swimming(xposition, scale = 1.0):
    pos (xposition, 0.5)
    anchor (0.5, 0.0)
    zoom scale
    ease 2.0 yoffset -10
    ease 2.0 yoffset 10
    repeat

transform mouse_swims_away:
    pos (0.7, 0.5)
    anchor (0.5, 0.0)
    zoom mouse_scale
    linear 10.0 xoffset 1000

transform mouse_swims_back:
    pos (1.2, 0.5)
    anchor (0.5, 0.0)
    zoom mouse_scale
    linear 10.0 xoffset -500
    

transform wave_animation():
    pos (0.5, 1.0)
    anchor (0.5, 1.0)
    linear 1.0 yoffset 20
    linear 1.0 yoffset 10
    repeat

transform alice_growing_large:
    pos (0.5, 0.7)
    anchor (0.5, 1.0)
    zoom 0.5
    easeout 60.0 zoom 10.0

transform alice_shrinking:
    pos (0.5, 0.7)
    anchor (0.5, 1.0)
    zoom alice_scale_large
    easein 20.0 zoom alice_scale

transform pan_background_to_center:
    xalign 0.0
    linear 15.0 xalign 0.5



label start:
    #jump chapter1_after_fall
label chapter1:

    scene black
    # start of new chapter
    "{size=+40}Chapter I: \n{/size}Down the Rabbit-Hole"

    scene riverbank at left
    play music "audio/rinne wanderer.mp3"
    show alice sleepy at breathing_calm(0.7, alice_scale)
    "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it."


    # voice "voice/alice001.mp3"
    alice "And what is the use of a book without pictures or conversations?" 

    "So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself:"

    scene riverbank at center
    #show alice normal at left as grayscale
    hide alice
    show rabbit normal at breathing(0.5)

    rabbit "Oh dear! Oh dear! I shall be too late!"

    "(when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural)"
    "But when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge."

    scene riverbank at left
    show alice happy at breathing(0.7, alice_scale)
    "In another moment down went Alice after it, never once considering how in the world she was to get out again."

    scene black

    "The rabbit-hole went straight on like a tunnel for some way,"
    
    scene well at center 
    play music "audio/rinne aurelia.mp3" fadeout 1.0 fadein 1.0 

    show alice falling at falling

    "and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well."

    "Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next."

    "First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs."

    show orange marmalade at Position(ypos = 0.7)

    "She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it."

    hide orange marmalade

    # voice "voice/alice002.mp3"
    alice "Well! After such a fall as this, I shall think nothing of tumbling down stairs! "  
    
    # voice "voice/alice003.mp3"
    alice "How brave they'll all think me at home!" 
    
    # voice "voice/alice004.mp3"
    alice "Why, I wouldn’t say anything about it, even if I fell off the top of the house!"  
    "(Which was very likely true.)"


    "Down, down, down. Would the fall never come to an end?"
    # voice "voice/alice005.mp3"
    alice "I wonder how many miles I've fallen by this time?"
    # voice "voice/alice006.mp3"
    alice "I must be getting somewhere near the centre of the earth."
    # voice "voice/alice007.mp3"
    alice "Let me see: that would be four thousand miles down, I think—"

    "(for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over)"

    # voice "voice/alice008.mp3"
    alice "—yes, that’s about the right distance—but then I wonder what Latitude or Longitude I’ve got to?"

    "(Alice had no idea what Latitude was, or Longitude either, but thought they were nice grand words to say.)"

    "Presently she began again."

    # voice "voice/alice009.mp3"
    alice "I wonder if I shall fall right through the earth! How funny it’ll seem to come out among the people that walk with their heads downward! The Antipathies, I think—"

    "(she was rather glad there was no one listening, this time, as it didn’t sound at all the right word) "

    #show alice curtsy air2 at falling2
    alice "—but I shall have to ask them what the name of the country is, you know. Please, Ma’am, is this New Zealand or Australia?"

    "(and she tried to curtsey as she spoke—fancy curtseying as you’re falling through the air! Do you think you could manage it?)"

    alice "And what an ignorant little girl she’ll think me for asking! No, it’ll never do to ask: perhaps I shall see it written up somewhere."
    show alice falling at falling
    "Down, down, down."

    "There was nothing else to do, so Alice soon began talking again."

    alice "Dinah’ll miss me very much to-night, I should think!"

    "(Dinah was the cat.)"

    alice "I hope they’ll remember her saucer of milk at tea-time. Dinah my dear! I wish you were down here with me!"
    alice "There are no mice in the air, I’m afraid, but you might catch a bat, and that’s very like a mouse, you know." 
    alice "But do cats eat bats, I wonder?"

    "And here Alice began to get rather sleepy, and went on saying to herself, in a dreamy sort of way"
    alice "Do cats eat bats? Do cats eat bats?"
    "and sometimes"
    alice "Do bats eat cats?" 
    "You see, as she couldn’t answer either question, it didn’t much matter which way she put it."
    "She felt that she was dozing off, and had just begun to dream that she was walking hand in hand with Dinah, and saying to her very earnestly:"
    alice "Now, Dinah, tell me the truth: did you ever eat a bat?"

    stop music fadeout 1.0
    scene black

    play sound "sfx/thump2.mp3"
    "when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over."


    
    "Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead;"

    scene hall at pan_background_to_center
    play music "audio/rinne memories of clockwise tower.mp3" fadein 1.0

    "before her was another long passage, and the White Rabbit was still in sight, hurrying down it."

    "There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner"

    hide alice
    show rabbit normal at breathing(0.5)
    rabbit "Oh my ears and whiskers, how late it's getting!"
    hide rabbit

    show alice happy at breathing(0.5, alice_scale)

    "She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof."

    show alice pout at breathing(0.5, alice_scale)
    "There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again."

    hide alice
    show three_legged_table_key at Position(ypos = 0.6)
    "Suddenly she came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them."
    hide three_legged_table_key

    scene small_door at center
    "However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about fifteen inches high: she tried the little golden key in the lock, and to her great delight it fitted!"

    play sound "sfx/unlock.mp3"
    "Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw."

    "How she longed to get out of that dark hall, and wander about among those beds of bright flowers and those cool fountains, but she could not even get her head through the doorway;"

    show alice pout at breathing(0.5, alice_scale)
    alice "and even if my head would go through, it would be of very little use without my shoulders."
    alice "Oh, how I wish I could shut up like a telescope! I think I could, if I only knew how to begin."

    "For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible."

    scene hall at center
    hide alice
    show three_legged_table_bottle at Position(ypos = 0.6)
    "There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it."
    alice "This certainly was not here before"
    "Around the neck of the bottle was a paper label, with the words 'DRINK ME' beautifully printed on it in large letters."

    "It was all very well to say 'Drink me', but the wise little Alice was not going to do that in a hurry."
    alice "No, I’ll look first and see whether it’s marked 'poison' or not."
    
    "she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they would not remember the simple rules their friends had taught them: "
    "such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger very deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked 'poison', it is almost certain to disagree with you, sooner or later."
    hide three_legged_table_bottle
    play sound "sfx/cork.mp3"

    "However, this bottle was not marked 'poison,' so Alice ventured to taste it, and finding it very nice, (it had, in fact, a sort of mixed flavour of cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off."
    
    show alice happy at breathing(0.5, alice_scale)
    alice "What a curious feeling! I must be shutting up like a telescope."

    "And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden."

    "First, however, she waited for a few minutes to see if she was going to shrink any further: she felt a little nervous about this."
    show alice surprised at breathing(0.5, alice_scale)
    alice "It might end, you know, in my going out altogether, like a candle. I wonder what I should be like then?"
    "And she tried to fancy what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing."

    "After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice, when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: "
    show alice crying at breathing_crying(0.5, alice_scale)
    "she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried."

    alice "Come, there’s no use in crying like that!"
    show alice pout at breathing(0.5, alice_scale)
    alice "I advise you to leave off this minute!"
    "She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people."
    alice "But it’s no use now, to pretend to be two people! Why, there’s hardly enough of me left to make one respectable person!"

    hide alice
    show box_cake at Position(ypos = 0.65)
    "Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words 'EAT ME' were beautifully marked in currants."

    hide box_cake
    show alice normal at breathing(0.5, alice_scale)
    alice "Well, I’ll eat it, and if it makes me grow larger, I can reach the key; and if it makes me grow smaller, I can creep under the door: so either way I’ll get into the garden, and I don’t care which happens!"

    "She ate a little bit, and said anxiously to herself: "
    show alice excited at breathing(0.5, alice_scale)
    alice "Which way? Which way?"
    "She was holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to find that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way."
    "So she set to work, and very soon finished off the cake."

label chapter2:
    scene black
    "{size=+40}Chapter II: \n{/size}The Pool of Tears"

    scene hall at center
    play music "audio/rinne memories of clockwise tower.mp3"

    show alice excited at alice_growing_large
    alice "Curiouser and curiouser!"
    "(she was so much surprised, that for the moment she quite forgot how to speak good English)"
    alice "Now I’m opening out like the largest telescope that ever was!"
    alice "Good-bye, feet!"
    "(For when she looked down at her feet, they seemed to be almost out of sight, they were getting so far off)"
    alice "Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able! "
    alice "I shall be a great deal too far off to trouble myself about you: you must manage the best way you can; —but I must be kind to them, or perhaps they won’t walk the way I want to go!" 
    alice "Let me see: I’ll give them a new pair of boots every Christmas."
    "And she went on planning to herself how she would manage it."
    alice "They must go by the carrier, and how funny it’ll seem, sending presents to one’s own feet! And how odd the directions will look!"
    "Alice’s Right Foot, Esq. \nHearthrug, \nNear the Fender, \n(with Alice’s love)."
    alice "Oh dear, what nonsense I’m talking!"
    play sound "sfx/bump.mp3"
    "Just then, her head struck against the roof of the hall: in fact she was now rather more than nine feet high, and she at once took up the little golden key and hurried off to the garden door."
    "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again."
    show alice crying at breathing_crying(0.5, alice_scale_large)

    alice "You ought to be ashamed of yourself, a great girl like you, to go on crying in this way! Stop this moment, I tell you!"
    "But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall."

    show alice pout at breathing(0.5, alice_scale_large)
    "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming."
    "It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other:"
    "he came trotting along in a great hurry, muttering to himself as he came,"
    hide alice
    show rabbit normal at breathing(0.5)
    rabbit "Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!"
    "Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice,"
    hide rabbit
    show alice pout at breathing(0.5, alice_scale_large)
    alice "If you please, sir—"
    hide alice

    show fan gloves at Position(ypos = 0.65)
    "The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go."

    "Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking:"
    hide fan gloves

    show alice pout at breathing(0.5, alice_scale_large)
    alice "Dear, dear! How queer everything is to-day! And yesterday things went on just as usual."
    alice "I wonder if I’ve been changed in the night? Let me think:"
    alice "was I the same when I got up this morning? I almost think I can remember feeling a little different."
    alice "But if I’m not the same, the next question is, Who in the world am I? Ah, that’s the great puzzle!"
    "And she began thinking over all the children she knew that were of the same age as herself, to see if she could have been changed for any of them."

    alice "I’m sure I’m not Ada, for her hair goes in such long ringlets, and mine doesn’t go in ringlets at all; and I’m sure I can’t be Mabel, for I know all sorts of things, and she, oh! she knows such a very little! Besides, she’s she, and I’m I, and—oh dear, how puzzling it all is!"
    alice "I’ll try if I know all the things I used to know. Let me see: four times five is twelve, and four times six is thirteen, and four times seven is—oh dear! I shall never get to twenty at that rate!"
    alice "However, the Multiplication Table doesn’t signify: let’s try Geography. London is the capital of Paris, and Paris is the capital of Rome, and Rome—no, that’s all wrong, I’m certain!"
    alice "I must have been changed for Mabel! I’ll try and say 'How doth the little—'"
    "and she crossed her hands on her lap as if she were saying lessons, and began to repeat it, but her voice sounded hoarse and strange, and the words did not come the same as they used to do:"

    alice "How doth the little crocodile \n    Improve his shining tail, \nAnd pour the waters of the Nile \n    On every golden scale!"

    alice "How cheerfully he seems to grin, \n    How neatly spread his claws, \nAnd welcome little fishes in \n    With gently smiling jaws!"

    show alice crying at breathing_crying(0.5, alice_scale_large)
    alice "I’m sure those are not the right words"
    alice "I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh!"
    alice "Ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here!" 
    alice "It’ll be no use their putting their heads down and saying 'Come up again, dear!' I shall only look up and say 'Who am I then?'" 
    alice "'Tell me that first, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else' —but, oh dear!"
    alice "I do wish they would put their heads down! I am so very tired of being all alone here!"

    show alice thinking at alice_shrinking
    "As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking."
    alice "How can I have done that?"
    alice "I must be growing small again."
    "She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly:"
    "she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether."

    show alice happy at breathing(0.5, alice_scale)
    alice "That was a narrow escape!"
    "She was a good deal frightened at the sudden change, but very glad to find herself still in existence."
    alice "And now for the garden!"
    "And she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before,"
    show alice pout at breathing(0.5, alice_scale)
    alice  "And things are worse than ever, for I never was so small as this before, never! And I declare it’s too bad, that it is!"

    stop music fadeout 1.0
    play sound "sfx/splash.mp3"
    "As she said these words her foot slipped, and in another moment, splash!"

    show waves zorder 0 at wave_animation
    show wavestop zorder 99 at wave_animation
    show alice pout zorder 1 at swimming(0.5, alice_scale)
    play music "audio/rinne beyond the sea.mp3"
    "she was up to her chin in salt water."

    show alice thinking zorder 1 at swimming(0.5, alice_scale)
    "Her first idea was that she had somehow fallen into the sea, "

    alice "and in that case I can go back by railway"
    "(Alice had been to the seaside once in her life, and had come to the general conclusion, that wherever you go to on the English coast you find a number of bathing machines in the sea, some children digging in the sand with wooden spades, then a row of lodging houses, and behind them a railway station)"
    "However, she soon made out that she was in the pool of tears which she had wept when she was nine feet high."

    show alice pout zorder 1 at swimming(0.5, alice_scale)
    alice "I wish I hadn’t cried so much!"
    "She swam about, trying to find her way out."
    alice "I shall be punished for it now, I suppose, by being drowned in my own tears! That will be a queer thing, to be sure! However, everything is queer to-day."

    show alice thinking zorder 1 at swimming(0.5, alice_scale)
    play sound "sfx/splash.mp3"
    "Just then she heard something splashing about in the pool a little way off, and she swam nearer to make out what it was:"
    show alice thinking zorder 1 at swimming(0.3, alice_scale)
    show mouse zorder 1 at swimming(0.7, mouse_scale)
    "at first she thought it must be a walrus or hippopotamus, but then she remembered how small she was now, and she soon made out that it was only a mouse that had slipped in like herself."

    alice "Would it be of any use, now, to speak to this mouse?"
    alice "Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying."
    "So she began:"
    show alice normal zorder 1 at swimming(0.3, alice_scale)
    alice "O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!"
    "(Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, 'A mouse—of a mouse—to a mouse—a mouse—O mouse!')"
    "The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing."

    show alice thinking zorder 1 at swimming(0.3, alice_scale)
    alice "Perhaps it doesn’t understand English, I daresay it’s a French mouse, come over with William the Conqueror."
    "(For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened)"
    "So she began again:"
    show alice normal zorder 1 at swimming(0.3, alice_scale)
    alice "Où est ma chatte?"
    "which was the first sentence in her French lesson-book."
    "The mouse gave a sudden leap out of the water, and seemed to quiver all over with fright."
    show alice thinking zorder 1 at swimming(0.3, alice_scale)
    alice "Oh, I beg your pardon!"
    "She was afraid that she had hurt the poor animal’s feelings."
    alice "I quite forgot you didn’t like cats."

    mouse "Not like cats!"
    mouse "Would you like cats if you were me?"

    alice "Well, perhaps not, don’t be angry about it."
    show alice happy zorder 1 at swimming(0.3, alice_scale)
    alice "And yet I wish I could show you our cat Dinah: I think you’d take a fancy to cats if you could only see her."
    alice "She is such a dear quiet thing,"
    "Alice went on, half to herself, as she swam lazily about in the pool,"
    alice "and she sits purring so nicely by the fire, licking her paws and washing her face—and she is such a nice soft thing to nurse—and she’s such a capital one for catching mice—oh, I beg your pardon!"
    "This time the Mouse was bristling all over, and she felt certain it must be really offended."
    show alice thinking zorder 1 at swimming(0.3, alice_scale)
    alice "We won’t talk about her any more if you’d rather not."

    mouse "We indeed!"
    "The mouse was trembling down to the end of its tail."
    mouse "As if I would talk on such a subject! Our family always hated cats: nasty, low, vulgar things! Don’t let me hear the name again!"

    show alice normal zorder 1 at swimming(0.3, alice_scale)
    alice "I won’t indeed!"
    "alice was in a great hurry to change the subject of conversation."
    alice "Are you—are you fond—of—of dogs?"
    "The mouse did not answer, so Alice went on eagerly:"
    alice "There is such a nice little dog near our house I should like to show you!"
    alice "A little bright-eyed terrier, you know, with oh, such long curly brown hair!"
    alice "And it’ll fetch things when you throw them, and it’ll sit up and beg for its dinner, and all sorts of things—I can’t remember half of them—and it belongs to a farmer, you know, and he says it’s so useful, it’s worth a hundred pounds!"
    alice "He says it kills all the rats and—oh dear!"
    show alice crying zorder 1 at swimming(0.3, alice_scale)
    "Alice cried in a sorrowful tone"
    alice "I’m afraid I’ve offended it again!"
    show mouse zorder 1 at mouse_swims_away
    "For the Mouse was swimming away from her as hard as it could go, and making quite a commotion in the pool as it went."

    alice "Mouse dear! Do come back again, and we won’t talk about cats or dogs either, if you don’t like them!"
    show alice normal zorder 1 at swimming(0.3, alice_scale)
    hide mouse
    show mouse zorder 1 at mouse_swims_back
    "When the Mouse heard this, it turned round and swam slowly back to her: its face was quite pale (with passion, Alice thought), and it said in a low trembling voice,"
    mouse "Let us get to the shore, and then I’ll tell you my history, and you’ll understand why it is I hate cats and dogs."

    "It was high time to go, for the pool was getting quite crowded with the birds and animals that had fallen into it: there were a Duck and a Dodo, a Lory and an Eaglet, and several other curious creatures."
    stop music fadeout 1.0
    "Alice led the way, and the whole party swam to the shore."

label chapter3:
    scene black 
    "{size=+40}Chapter III: \n{/size}A Caucus-Race and a Long Tale"

    scene muddy:
        xpos 0
    # show all characters
    define muddy_eaglet_pos = 1104
    define muddy_lory_pos = 540
    define muddy_duck_pos = 822
    define muddy_dodo_pos = 1950
    define muddy_alice_pos = 1386
    define muddy_mouse_pos = 1668
    define muddy_old_crab_pos = 2232
    define muddy_young_crab_pos = 2514
    define muddy_magpie_pos = 2796
    define muddy_canary_pos = 3078
    show eaglet at breathing(muddy_eaglet_pos, eaglet_scale)
    show lory at breathing(muddy_lory_pos, lory_scale)
    show duck at breathing(muddy_duck_pos, duck_scale)
    show dodo at breathing(muddy_dodo_pos, dodo_scale)
    show alice normal at breathing(muddy_alice_pos, alice_scale_muddy)
    show mouse at breathing(muddy_mouse_pos, mouse_muddy_scale)
    show old_crab at breathing(muddy_old_crab_pos, old_crab_scale)
    show young_crab at breathing(muddy_young_crab_pos, young_crab_scale)
    show magpie at breathing(muddy_magpie_pos, magpie_scale)
    show canary at breathing(muddy_canary_pos, canary_scale)

    camera:
        perspective True
        xpos center_offset xoffset -center_offset
        linear 20.0 xpos 2280


    play music "audio/rinne oak general store.mp3"

    "They were indeed a queer-looking party that assembled on the bank—the birds with draggled feathers, the animals with their fur clinging close to them, and all dripping wet, cross, and uncomfortable."

    "The first question of course was, how to get dry again: they had a consultation about this, and after a few minutes it seemed quite natural to Alice to find herself talking familiarly with them, as if she had known them all her life."
    "Indeed, she had quite a long argument with the Lory, who at last turned sulky, and would only say"

    camera: 
        ease cam_transition xpos muddy_lory_pos
    lory "I am older than you, and must know better"
    "and this Alice would not allow without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said."

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    "At last the Mouse, who seemed to be a person of authority among them, called out:"
    
    mouse "Sit down, all of you, and listen to me! I’ll soon make you dry enough!"
    "They all sat down at once, in a large ring, with the Mouse in the middle."
    "Alice kept her eyes anxiously fixed on it, for she felt sure she would catch a bad cold if she did not get dry very soon."

    mouse "Ahem!"
    mouse "Are you all ready? This is the driest thing I know."
    mouse "Silence all round, if you please!"
    mouse "'William the Conqueror, whose cause was favoured by the pope, was soon submitted to by the English, who wanted leaders, and had been of late much accustomed to usurpation and conquest." 
    mouse "Edwin and Morcar, the earls of Mercia and Northumbria—'"

    camera: 
        ease cam_transition xpos muddy_lory_pos
    lory "Ugh!"

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    mouse "I beg your pardon!"
    mouse "Did you speak?"

    camera: 
        ease cam_transition xpos muddy_lory_pos
    lory "Not I!"

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    mouse "I thought you did, —I proceed."
    mouse "'Edwin and Morcar, the earls of Mercia and Northumbria, declared for him: and even Stigand, the patriotic archbishop of Canterbury, found it advisable—'"

    camera: 
        ease cam_transition xpos muddy_duck_pos
    duck "Found what?"

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    mouse "Found it, of course you know what 'it' means."

    camera: 
        ease cam_transition xpos muddy_duck_pos
    duck "I know what 'it' means well enough, when I find a thing, it’s generally a frog or a worm. The question is, what did the archbishop find?"

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    "The Mouse did not notice this question, but hurriedly went on,"

    mouse "'—found it advisable to go with Edgar Atheling to meet William and offer him the crown. William’s conduct at first was moderate. But the insolence of his Normans—'"
    "it continued, turning to Alice as it spoke."
    mouse "How are you getting on now, my dear?"

    camera: 
        ease cam_transition xpos muddy_alice_pos
    show alice pout at breathing(muddy_alice_pos, alice_scale_muddy)
    alice "As wet as ever, it doesn’t seem to dry me at all."

    camera: 
        ease cam_transition xpos muddy_dodo_pos
    dodo "In that case, I move that the meeting adjourn, for the immediate adoption of more energetic remedies—"

    camera: 
        ease cam_transition xpos muddy_eaglet_pos
    eaglet "Speak English! I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!"
    "And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly."

    camera: 
        ease cam_transition xpos muddy_dodo_pos
    dodo "What I was going to say, was that the best thing to get us dry would be a Caucus-race."

    "..."

    camera: 
        ease cam_transition xpos muddy_alice_pos
    show alice thinking at breathing(muddy_alice_pos, alice_scale_muddy)
    alice "What is a Caucus-race?"

    "not that she wanted much to know, but the Dodo had paused as if it thought that somebody ought to speak, and no one else seemed inclined to say anything."

    camera: 
        ease cam_transition xpos muddy_dodo_pos
    dodo "Why, the best way to explain it is to do it."

    "(And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it)"

    show racetrack at Position(ypos = 0.65, xpos = muddy_dodo_pos)
    "First it marked out a race-course, in a sort of circle."
    dodo "The exact shape doesn’t matter"
    hide racetrack

    # place party members randomly
    show alice normal:
        ease cam_transition xpos 2000
    show mouse:
        ease cam_transition xpos 1900
    show duck:
        ease cam_transition xpos 2200
    show old_crab:
        ease cam_transition xpos 2100
    show young_crab:
        ease cam_transition xpos 2150

    "And then all the party were placed along the course, here and there."

    show alice happy:
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


    "There was no 'One, two, three, and away', but they began running when they liked, and left off when they liked, so that it was not easy to know when the race was over."
    "..."
    "However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out:"

    scene black:
        xpos 0
    camera:
        xpos center_offset xoffset -center_offset
    dodo "The race is over!"

    scene muddy:
        xpos 0
    camera:
        perspective True
        xpos center_offset xoffset -center_offset
        linear 20.0 xpos 2280

    # restore original positions
    show eaglet at breathing(muddy_eaglet_pos, eaglet_scale)
    show lory at breathing(muddy_lory_pos, lory_scale)
    show duck at breathing(muddy_duck_pos, duck_scale)
    show dodo at breathing(muddy_dodo_pos, dodo_scale)
    show alice normal at breathing(muddy_alice_pos, alice_scale_muddy)
    show mouse at breathing(muddy_mouse_pos, mouse_muddy_scale)
    show old_crab at breathing(muddy_old_crab_pos, old_crab_scale)
    show young_crab at breathing(muddy_young_crab_pos, young_crab_scale)
    show magpie at breathing(muddy_magpie_pos, magpie_scale)
    show canary at breathing(muddy_canary_pos, canary_scale)

    "and they all crowded round it, panting, and asking, "
    everyone "But who has won?"

    "This question the Dodo could not answer without a great deal of thought, and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence."
    dodo "Everybody has won, and all must have prizes."

    everyone "But who is to give the prizes?"
    dodo "Why, she, of course," 
    camera:
        ease cam_transition xpos muddy_alice_pos
    "said the Dodo, pointing to Alice with one finger; and the whole party at once crowded round her, calling out in a confused way,"
    everyone "Prizes! Prizes!"

    show comfits at Position(ypos = 0.65, xpos = muddy_alice_pos)
    "Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes."
    "There was exactly one a-piece all round."
    hide comfits

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    mouse "But she must have a prize herself, you know."

    camera: 
        ease cam_transition xpos muddy_dodo_pos
    dodo "Of course. What else have you got in your pocket?"
    "The dodo truned to Alice"

    camera: 
        xpos muddy_alice_pos
    show alice normal at breathing(muddy_alice_pos, alice_scale_muddy)

    show thimble at Position(ypos = 0.65, xpos = muddy_alice_pos)
    alice "Only a thimble."
    hide thimble

    camera: 
        ease cam_transition xpos muddy_dodo_pos
    dodo "Hand it over here."

    "Then they all crowded round her once more, while the Dodo solemnly presented the thimble"
    camera: 
        xpos muddy_dodo_pos
    show thimble at Position(ypos = 0.65, xpos = muddy_dodo_pos)
    dodo "We beg your acceptance of this elegant thimble."
    "And, when it had finished this short speech, they all cheered."

    "Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could."
    hide thimble 

    camera: 
        ease cam_transition xpos muddy_alice_pos
    "The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back."

    camera: 
        ease cam_transition xpos muddy_mouse_pos
    "However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more."

    
    alice "You promised to tell me your history, you know,"
    alice "and why it is you hate—C and D"
    "alice added in a whisper, half afraid that it would be offended again."
 
    mouse "Mine is a long and a sad {b}tale{/b}!"

    alice "It is a long {b}tail{/b}, certainly, but why do you call it sad?"
    "She kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:—"

    mouse " {space=80} Fury said to a\n {space=60} mouse. That he\n {space=40} met in the\n {space=20} house.\n'Let us\n {space=20} both go to\n {space=40} law: I will\n {space=60} prosecute\n {space=80} YOU.—Come,\n {space=100} I’ll take no"
    mouse " {space=120} denial; We\n {space=100} must have a\n {space=80} trial: For\n {space=60} really this\n {space=40} morning I’ve\n {space=20} nothing\nto do.'\n {space=20} Said the\n {space=40} mouse to the\n {space=60} cur, 'Such"
    mouse " {space=80} a trial,\n {space=100} dear Sir,\n {space=120} With\n {space=100} no jury\n {space=80} or judge,\n {space=60} would be\n {space=40} wasting\n {space=20} our\n {space=40} breath.'\n {space=60} 'I’ll be"
    mouse " {space=80} judge, I’ll\n {space=100} be jury'\n {space=120} Said\n {space=100} cunning\n {space=120} old Fury:\n {space=140} 'I’ll\n {space=120} try the\n {space=140} whole\n {space=160} cause,\n {space=180} and"
    mouse " {space=160} condemn\n {space=140} you\n {space=120} to\n {space=140} death.'"

    mouse "You are not attending!"
    mouse "What are you thinking of?"

    alice "I beg your pardon, you had got to the fifth bend, I think?"

    mouse "I had not!" # cried the Mouse, sharply and very angrily.

    alice "A knot!" # said Alice, always ready to make herself useful, and looking anxiously about her. 
    alice "Oh, do let me help to undo it!"

    mouse "I shall do nothing of the sort."
    show mouse:
        ease 1.0 xoffset 200

    "the mouse gets up and walks away."
    mouse "You insult me by talking such nonsense!"

    alice "I didn’t mean it! But you’re so easily offended, you know!"
    show mouse:
        ease 1.0 xoffset 400
    "The mouse only growled in reply."

    alice "Please come back and finish your story!"
    "All the others joined in chorus"
    show mouse:
        ease 1.0 xoffset 600
    everyone "Yes, please do!"
    "but the Mouse only shook its head impatiently, and walked a little quicker."
    hide mouse

    camera: 
        ease cam_transition xpos muddy_lory_pos
    lory "What a pity it wouldn’t stay!"
    "sighed the Lory, as soon as it was quite out of sight; and an old Crab took the opportunity of saying to her daughter"

    camera: 
        ease cam_transition xpos muddy_old_crab_pos
    old_crab "Ah, my dear! Let this be a lesson to you never to lose your temper!"
    
    camera: 
        ease cam_transition xpos muddy_young_crab_pos
    young_crab "Hold your tongue, Ma! You’re enough to try the patience of an oyster!"

    camera: 
        ease cam_transition xpos muddy_alice_pos
    show alice normal at breathing(muddy_alice_pos, alice_scale_muddy)
    alice "I wish I had our Dinah here, I know I do!"
    alice "She’d soon fetch it back!"

    camera: 
        ease cam_transition xpos muddy_lory_pos
    lory "And who is Dinah, if I might venture to ask the question?"

    camera: 
        ease cam_transition xpos muddy_alice_pos
    alice "Dinah’s our cat. And she’s such a capital one for catching mice you can’t think! And oh, I wish you could see her after the birds! Why, she’ll eat a little bird as soon as look at it!"

    camera: 
        ease cam_transition xpos muddy_magpie_pos
    "This speech caused a remarkable sensation among the party. Some of the birds hurried off at once: one old Magpie began wrapping itself up very carefully"
    show magpie:
        xzoom -1.0
        linear 1.0 xpos 4000
    magpie "I really must be getting home; the night-air doesn’t suit my throat!"
    hide magpie

    "and a Canary called out in a trembling voice to its children"
    show canary:
        xzoom -1.0
        linear 1.0 xpos 4000
    canary "Come away, my dears! It’s high time you were all in bed!"
    hide canary
    
    show young_crab:
        linear 2.0 xpos 4000
    show old_crab:
        linear 2.0 xpos 4000
    hide dodo
    hide eaglet
    hide lory
    hide duck

    camera: 
        ease 2.0 xpos muddy_alice_pos
    "On various pretexts they all moved off, and Alice was soon left alone."

    show alice pout at breathing(muddy_alice_pos, alice_scale_muddy)
    alice "I wish I hadn’t mentioned Dinah!"
    alice "Nobody seems to like her, down here, and I’m sure she’s the best cat in the world!"
    alice "Oh, my dear Dinah! I wonder if I shall ever see you any more!"
    show alice crying at breathing_crying(muddy_alice_pos, alice_scale_muddy)
    "And here poor Alice began to cry again, for she felt very lonely and low-spirited."
    "In a little while, however, she again heard a little pattering of footsteps in the distance, and she looked up eagerly, half hoping that the Mouse had changed his mind, and was coming back to finish his story."

label chapter4:
    scene black
    camera: # revert camera
        perspective False
    "{size=+40}Chapter IV: \n{/size}The Rabbit Sends in a Little Bill"
    scene muddy
    play music "audio/rinne oak general store.mp3" if_changed
    #jump ch4_forest
    #jump ch4_grass

    show alice pout at breathing(0.7, alice_scale)

    show rabbit normal:
        anchor (0.5, 1.0)
        zoom rabbit_scale
        ypos 0.8
        xpos 1.2
        ease 20.0 xpos -1.0

    "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself"
    rabbit  "The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where can I have dropped them, I wonder?"
    "Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen—everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely."

    show rabbit normal:
        xzoom -1.0
        ease 5.0 xpos 0.2 ypos 0.7
    "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone"
    show alice surprised
    rabbit "Why, Mary Ann, what are you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!"
    show alice surprised:
        linear 1.0 xpos 2.0
    "And Alice was so much frightened that she ran off at once in the direction it pointed to, without trying to explain the mistake it had made."
    scene black
    alice "He took me for his housemaid. How surprised he’ll be when he finds out who I am! But I’d better take him his fan and gloves—that is, if I can find them."

    scene rabbit_house:
        xalign 0.0
        linear 10.0 xalign 1.0
    "As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name 'W. RABBIT' engraved upon it."
    "She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves."

    scene rabbit_room:
        xalign 0.0
        linear 10.0 xalign 1.0

    alice "How queer it seems, to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!"
    "And she began fancying the sort of thing that would happen:"
    alice "'Miss Alice! Come here directly, and get ready for your walk!' 'Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.'"
    alice "Only I don’t think, that they’d let Dinah stop in the house if it began ordering people about like that!"

    show fan gloves at Position(ypos = 0.65, xpos = 0.5)
    "By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves:"
    hide fan gloves
    show alice excited at breathing(0.5, alice_scale, 1.0)
    alice "she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass."
    play sound "sfx/cork.mp3"
    "There was no label this time with the words 'DRINK ME', but nevertheless she uncorked it and put it to her lips."
    alice "I know something interesting is sure to happen, whenever I eat or drink anything; so I’ll just see what this bottle does."
    alice "I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!"

    show alice excited:
        pos (0.5, 1.0)
        anchor (0.5, 1.0)
        zoom alice_scale
        easeout 60.0 zoom 10.0

    "It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken."
    "She hastily put down the bottle."
    alice "That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!"

    show alice belly:
        xalign 0.7
        yalign 1.0
        anchor (0.5, 1.0)
        zoom 1.0
        easeout 10.0 zoom 2.0

    "Alas! it was too late to wish that! She went on growing, and growing, and very soon had to kneel down on the floor:"
    "In another minute there was not even room for this, and she tried the effect of lying down with one elbow against the door, and the other arm curled round her head."
    "Still she went on growing, and, as a last resource, she put one arm out of the window, and one foot up the chimney"


    alice "Now I can do no more, whatever happens. What will become of me?"

    # stop growing, show at max w/ breathing
    show alice belly at breathing(0.7, 2.0, 1.0)
    "Luckily for Alice, the little magic bottle had now had its full effect, and she grew no larger:"

    "Still it was very uncomfortable, and, as there seemed to be no sort of chance of her ever getting out of the room again, no wonder she felt unhappy."

    alice "It was much pleasanter at home, when one wasn’t always growing larger and smaller, and being ordered about by mice and rabbits."
    alice "I almost wish I hadn’t gone down that rabbit-hole—and yet—and yet—it’s rather curious, you know, this sort of life!"
    alice "I do wonder what can have happened to me! When I used to read fairy-tales, I fancied that kind of thing never happened, and now here I am in the middle of one!"
    alice "There ought to be a book written about me, that there ought! And when I grow up, I’ll write one—but I’m grown up now, at least there’s no room to grow up any more here."

    alice "But then, shall I never get any older than I am now? That’ll be a comfort, one way—never to be an old woman—but then—always to have lessons to learn! Oh, I shouldn’t like that!"

    alice "Oh, you foolish Alice!"
    alice "How can you learn lessons in here?"
    alice "Why, there’s hardly room for you, and no room at all for any lesson-books!"

    "And so she went on, taking first one side and then the other, and making quite a conversation of it altogether; but after a few minutes she heard a voice outside, and stopped to listen."

    rabbit "Mary Ann! Mary Ann!"
    rabbit "Fetch me my gloves this moment!"

    play sound "sfx/upstairs.mp3"
    "Then came a little pattering of feet on the stairs."
    "Alice knew it was the Rabbit coming to look for her, and she trembled till she shook the house, quite forgetting that she was now about a thousand times as large as the Rabbit, and had no reason to be afraid of it."

    play sound "sfx/door_closed.mp3"
    "Presently the Rabbit came up to the door, and tried to open it; but, as the door opened inwards, and Alice’s elbow was pressed hard against it, that attempt proved a failure."
    rabbit "Then I’ll go round and get in at the window."

    alice "That you won’t!"
    "thought Alice, and, after waiting till she fancied she heard the Rabbit just under the window,"
    play sound "sfx/snatch.mp3"
    "she suddenly spread out her hand, and made a snatch in the air."
    play sound "sfx/shatter.mp3"
    "She did not get hold of anything, but she heard a little shriek and a fall, and a crash of broken glass, from which she concluded that it was just possible it had fallen into a cucumber-frame, or something of the sort."

    "Next came an angry voice—"
    rabbit "Pat! Pat! Where are you?"
    "And then a voice she had never heard before, "
    pat "Sure then I’m here! Digging for apples, yer honour!"
    rabbit "Digging for apples, indeed!"
    rabbit "Here! Come and help me out of this!"
    "..."
    play sound "sfx/shatter.mp3"
    "(Sounds of more broken glass)"
    rabbit "Now tell me, Pat, what’s that in the window?"
    pat "Sure, it’s an arrumm, yer honour!"
    rabbit "An arm, you goose! Who ever saw one that size? Why, it fills the whole window!"
    pat "Sure, it does, yer honour: but it’s an arm for all that."
    rabbit "Well, it’s got no business there, at any rate: go and take it away!"

    "There was a long silence after this, and Alice could only hear whispers now and then; such as,"
    pat "Sure, I don’t like it, yer honour, at all, at all!"
    rabbit "Do as I tell you, you coward!"
    play sound "sfx/snatch.mp3"
    "and at last she spread out her hand again, and made another snatch in the air."

    play sound "sfx/shatter.mp3"
    "This time there were two little shrieks, and more sounds of broken glass."
    alice "What a number of cucumber-frames there must be!"
    alice "I wonder what they’ll do next! As for pulling me out of the window, I only wish they could! I’m sure I don’t want to stay in here any longer!"

    "She waited for some time without hearing anything more: at last came a rumbling of little cartwheels, and the sound of a good many voices all talking together:"

    anon "Where’s the other ladder?"
    anon "Why, I hadn’t to bring but one; Bill’s got the other"
    anon "Bill! fetch it here, lad!"
    anon "Here, put 'em up at this corner"
    anon "No, tie 'em together first—they don’t reach half high enough yet—Oh! they’ll do well enough; don’t be particular"
    anon "Here, Bill! catch hold of this rope"
    anon "Will the roof bear?"
    anon "Mind that loose slate"
    anon "Oh, it’s coming down! Heads below!"

    play sound "sfx/shatter.mp3"
    anon "Now, who did that?"
    anon "It was Bill, I fancy"
    anon "Who’s to go down the chimney?"
    anon "Nay, I shan’t! You do it!"
    anon "That I won’t, then!"
    anon "Bill’s to go down"
    anon "Here, Bill! the master says you’re to go down the chimney!"

    alice "Oh! So Bill’s got to come down the chimney, has he?"
    alice "Shy, they seem to put everything upon Bill! I wouldn’t be in Bill’s place for a good deal: this fireplace is narrow, to be sure; but I think I can kick a little!"

    "She drew her foot as far down the chimney as she could, and waited till she heard a little animal (she couldn’t guess of what sort it was) scratching and scrambling about in the chimney close above her:"
    alice "This is Bill!"
    play sound "sfx/snatch.mp3"
    "She gave one sharp kick, and waited to see what would happen next."

    "The first thing she heard was a general chorus of"
    everyone "There goes Bill!"
    "Then the Rabbit’s voice along—"
    rabbit "Catch him, you by the hedge!"
    play sound "sfx/shatter.mp3"
    "..."
    "Then silence, and then another confusion of voices—"
    anon "Hold up his head"
    anon "Brandy now"
    anon "Don’t choke him"
    anon "How was it, old fellow? What happened to you? Tell us all about it!"

    "Last came a little feeble, squeaking voice"
    bill "Well, I hardly know—No more, thank ye; I’m better now—but I’m a deal too flustered to tell you—all I know is, something comes at me like a Jack-in-the-box, and up I goes like a sky-rocket!"
    anon "So you did, old fellow!"

    rabbit "We must burn the house down!"
    "Alice called out as loud as she could:"
    alice "If you do, I’ll set Dinah at you!"

    "..."
    "There was a dead silence instantly, and Alice thought to herself:"
    alice "I wonder what they will do next! If they had any sense, they’d take the roof off."
    "After a minute or two, they began moving about again"
    rabbit "A barrowful will do, to begin with."

    alice "A barrowful of what?"
    "She had not long to doubt, for the next moment a shower of little pebbles came rattling in at the window, and some of them hit her in the face."
    alice "I’ll put a stop to this."
    "she said to herself, and shouted out, "
    alice "You’d better not do that again!"
    "which produced another dead silence."

    show pebble_cake at Position(ypos = 0.65, xpos = 0.5)
    "Alice noticed with some surprise that the pebbles were all turning into little cakes as they lay on the floor, and a bright idea came into her head."
    alice "If I eat one of these cakes, it’s sure to make some change in my size; and as it can’t possibly make me larger, it must make me smaller, I suppose."
    hide pebble_cake

    show alice:
        easein 10.0 zoom 1.0
    "So she swallowed one of the cakes, and was delighted to find that she began shrinking directly."

    scene rabbit_house:
        xalign 0.2 zoom 1.3 yalign 1.0

    show bill guinea at breathing(0.25, 0.8, 0.92)
    show alice surprised at breathing(0.85, alice_scale, 0.79)
    "As soon as she was small enough to get through the door, she ran out of the house, and found quite a crowd of little animals and birds waiting outside."
    "The poor little Lizard, Bill, was in the middle, being held up by two guinea-pigs, who were giving it something out of a bottle."

    show alice:
        linear 1.0 xpos 2.0
    "They all made a rush at Alice the moment she appeared; but she ran off as hard as she could, and soon found herself safe in a thick wood."

label ch4_forest:
    scene forest
    camera:
        perspective True
        xpos -215 ypos 490 zpos -500

    show alice thinking at breathing(0.3, 0.14, 0.85)
    show thistle:
        pos (0.10, 0.85)
        anchor (0.5, 1.0)
        zoom 0.3
        zpos 60
    show puppy:
        pos (0.89, 0.85)
        anchor (0.5, 1.0)
        zoom 1.0

    alice "The first thing I’ve got to do, is to grow to my right size again; and the second thing is, to find my way into that lovely garden."
    alice "I think that will be the best plan."

    "It sounded an excellent plan, no doubt, and very neatly and simply arranged; the only difficulty was, that she had not the smallest idea how to set about it; and while she was peering about anxiously among the trees, a little sharp bark just over her head made her look up in a great hurry."

    camera:
        linear 2.0 xpos 0 ypos 425 zpos -335
    #scene huge_dog # todo replace with normal sized dog
    play sound "sfx/bark.mp3"
    "An enormous puppy was looking down at her with large round eyes, and feebly stretching out one paw, trying to touch her."
    alice "Poor little thing!"
    "She tried hard to whistle to it; but she was terribly frightened all the time at the thought that it might be hungry, in which case it would be very likely to eat her up in spite of all her coaxing."

    play sound "sfx/bark.mp3"
    show puppy:
        easein 1.0 yoffset -200
        easeout 1.0 yoffset 0

    "Hardly knowing what she did, she picked up a little bit of stick, and held it out to the puppy; whereupon the puppy jumped into the air off all its feet at once, with a yelp of delight, and rushed at the stick, and made believe to worry it;"
    camera:
        linear 2.0 xpos -275 ypos 425 zpos -335
    show alice:
        linear 0.5 xpos 0.05
    show puppy:
        linear 0.7 xpos 0.7
        linear 0.7 xpos 0.38 ypos 0.75 zrotate -40
        linear 0.7 xpos 0.0 ypos 0.75 zrotate -80
        linear 0.7 xpos -0.42 ypos 0.75 zrotate -120
        linear 0.7 xpos -0.71 ypos 0.75 zrotate -160
        linear 0.2 xpos -0.71 ypos 0.75 zrotate 0 xzoom -1.0

    "then Alice dodged behind a great thistle, to keep herself from being run over; and the moment she appeared on the other side, the puppy made another rush at the stick, and tumbled head over heels in its hurry to get hold of it;"
    show alice:
        linear 0.5 xpos 0.17
    "then Alice, thinking it was very like having a game of play with a cart-horse, and expecting every moment to be trampled under its feet, ran round the thistle again;"
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
    "then the puppy began a series of short charges at the stick, running a very little way forwards each time and a long way back, and barking hoarsely all the while, till at last it sat down a good way off, panting, with its tongue hanging out of its mouth, and its great eyes half shut."

    "This seemed to Alice a good opportunity for making her escape; so she set off at once, and ran till she was quite tired and out of breath, and till the puppy’s bark sounded quite faint in the distance."
label ch4_grass:

    # hacky way to save setup for next chapter
    call setup_caterpillar
    jump ch4_caterpillar

label setup_caterpillar:
    scene sky:
        xpos 0.0 zpos -1500 zzoom True


    show soil:
        anchor (0.0, 0.0)
        xrotate 90 yoffset -512 zpos -1100 ypos 1.0 

    show blades at Position(xpos = 800, ypos = 1.0):
        anchor (0.5, 1.0)
        zpos -1100
        zoom 0.5

    show alice normal at breathing(800, 0.2, 1.0):
        zpos -1000 

    show buttercup at Position(xpos = 650, ypos = 1.0):
        anchor (0.5, 1.0)
        zoom 0.3
        zpos -950

    show caterpillar at breathing(1090, 0.3, 0.85):
        zpos -900

    show mushroom at Position(xpos = 1090, ypos = 1.0):
        anchor (0.5, 1.0)
        zoom 0.38
        zpos -880
    show blades as blades2 at Position(xpos = 800, ypos = 1.14):
        anchor (0.5, 1.0)
        zpos -860
        zoom 0.5
    return
label ch4_caterpillar:

    camera:
        perspective True
        xpos 730 ypos 815 zpos -1460 xoffset -center_offset

    alice "And yet what a dear little puppy it was!"
    "She leant against a buttercup to rest herself, and fanned herself with one of the leaves:"

    alice "I should have liked teaching it tricks very much, if—if I’d only been the right size to do it!"
    alice "Oh dear! I’d nearly forgotten that I’ve got to grow up again!"
    alice "Let me see—how is it to be managed?"
    alice "I suppose I ought to eat or drink something or other; but the great question is, what?"

    "The great question certainly was, what?"

    camera:
        linear 4.0 xpos 1000 

    "Alice looked all round her at the flowers and the blades of grass, but she did not see anything that looked like the right thing to eat or drink under the circumstances."



    "There was a large mushroom growing near her, about the same height as herself; and when she had looked under it, and on both sides of it, and behind it, it occurred to her that she might as well look and see what was on the top of it."

    camera:
        linear 4.0 xpos 1000 ypos 635 zpos -1275

    "She stretched herself up on tiptoe, and peeped over the edge of the mushroom, and her eyes immediately met those of a large caterpillar, that was sitting on the top with its arms folded, quietly smoking a long hookah, and taking not the smallest notice of her or of anything else."

label chapter5:
    scene black
    camera: # revert camera
        perspective False
        zpos 0
    "{size=+40}Chapter V: \n{/size}Advice from a Caterpillar"

    play music "audio/rinne oak general store.mp3" if_changed

    #jump ch5_sky

    call setup_caterpillar

    camera:
        perspective True
        xpos 1000 ypos 635 zpos -1275 xoffset -center_offset

    "The Caterpillar and Alice looked at each other for some time in silence: at last the Caterpillar took the hookah out of its mouth, and addressed her in a languid, sleepy voice."

    caterpillar "Who are you?"

    "This was not an encouraging opening for a conversation."
    alice "I—I hardly know, sir, just at present—at least I know who I was when I got up this morning, but I think I must have been changed several times since then."

    caterpillar "What do you mean by that?"
    caterpillar "Explain yourself!"

    alice "I can’t explain myself, I’m afraid, sir, because I’m not myself, you see."

    caterpillar "I don’t see."

    alice "I’m afraid I can’t put it more clearly, for I can’t understand it myself to begin with; and being so many different sizes in a day is very confusing."

    caterpillar "It isn’t."

    alice "Well, perhaps you haven’t found it so yet, but when you have to turn into a chrysalis—you will some day, you know—and then after that into a butterfly, I should think you’ll feel it a little queer, won’t you?"

    caterpillar "Not a bit."

    alice "Well, perhaps your feelings may be different. All I know is, it would feel very queer to me."

    caterpillar "You!" # said the Caterpillar contemptuously.
    caterpillar "Who are you?"

    "Which brought them back again to the beginning of the conversation."
    "Alice felt a little irritated at the Caterpillar’s making such very short remarks, and she drew herself up and said, very gravely,"
    alice "I think, you ought to tell me who you are, first."

    caterpillar "Why?"

    "Here was another puzzling question; and as Alice could not think of any good reason, and as the Caterpillar seemed to be in a very unpleasant state of mind, she turned away."

    caterpillar "Come back!"
    caterpillar "I’ve something important to say!"

    "This sounded promising, certainly: Alice turned and came back again."

    caterpillar "Keep your temper."

    "..."

    alice "Is that all?"
    "Alice swallowed down her anger as well as she could."
    caterpillar "No"

    "Alice thought she might as well wait, as she had nothing else to do, and perhaps after all it might tell her something worth hearing."
    "..."
    "For some minutes it puffed away without speaking, but at last it unfolded its arms, took the hookah out of its mouth again."
    caterpillar "So you think you’re changed, do you?"

    alice "I’m afraid I am, sir."
    alice "I can’t remember things as I used—and I don’t keep the same size for ten minutes together!"

    caterpillar "Can’t remember what things?"

    alice "Well, I’ve tried to say 'How doth the little busy bee', but it all came different!"

    caterpillar "Repeat, 'You are old, Father William.'"

    "Alice folded her hands, and began:"

    alice "'You are old, Father William,' the young man said,\n   And your hair has become very white;\nAnd yet you incessantly stand on your head—\n   Do you think, at your age, it is right?'"

    alice "'In my youth,' Father William replied to his son,\n   'I feared it might injure the brain;\nBut, now that I’m perfectly sure I have none,\n   Why, I do it again and again.'"

    alice "'You are old,' said the youth, 'as I mentioned before,\n   And have grown most uncommonly fat;\nYet you turned a back-somersault in at the door—\n   Pray, what is the reason of that?'"

    alice "'In my youth,' said the sage, as he shook his grey locks,\n   'I kept all my limbs very supple\nBy the use of this ointment—one shilling the box—\n   Allow me to sell you a couple?'"

    alice "'You are old,' said the youth, 'and your jaws are too weak\n   For anything tougher than suet;\nYet you finished the goose, with the bones and the beak—\n   Pray how did you manage to do it?'"

    alice "'In my youth,' said his father, 'I took to the law,\n   And argued each case with my wife;\nAnd the muscular strength, which it gave to my jaw,\n   Has lasted the rest of my life.'"

    alice "'You are old,' said the youth, 'one would hardly suppose\n   That your eye was as steady as ever;\nYet you balanced an eel on the end of your nose—\n   What made you so awfully clever?'"

    alice "'I have answered three questions, and that is enough,'\n   Said his father; 'don’t give yourself airs!\nDo you think I can listen all day to such stuff?\n   Be off, or I’ll kick you down stairs!'"

    caterpillar "That is not said right."

    alice "Not quite right, I’m afraid." # said alice timidly;
    alice "Some of the words have got altered."

    caterpillar "It is wrong from beginning to end."
    "..."
    "And there was silence for some minutes."

    caterpillar "What size do you want to be?"

    alice "Oh, I’m not particular as to size, only one doesn’t like changing so often, you know."

    caterpillar "I don’t know."

    "Alice said nothing: she had never been so much contradicted in all her life before, and she felt that she was losing her temper."

    caterpillar "Are you content now?"

    alice "Well, I should like to be a little larger, sir, if you wouldn’t mind."
    alice "Three inches is such a wretched height to be."

    caterpillar "It is a very good height indeed!"
    "said the Caterpillar angrily, rearing itself upright as it spoke (it was exactly three inches high)."

    alice "But I’m not used to it!"
    "pleaded poor Alice in a piteous tone. And she thought of herself:"

    alice "I wish the creatures wouldn’t be so easily offended!"

    caterpillar "You’ll get used to it in time."
    "The caterpillar put the hookah into its mouth and began smoking again."

    "This time Alice waited patiently until it chose to speak again."
    "In a minute or two the Caterpillar took the hookah out of its mouth and yawned once or twice, and shook itself."

    show caterpillar at breathing(1090, 0.3, 0.85):
        zpos -900
        linear 2.0 ypos 1.0
        linear 20.0 zpos -1200
    "Then it got down off the mushroom, and crawled away in the grass."
    caterpillar "One side will make you grow taller, and the other side will make you grow shorter."

    alice "One side of what? The other side of what?"
    caterpillar "Of the mushroom."
    "In another moment it was out of sight."

    hide caterpillar

    "Alice remained looking thoughtfully at the mushroom for a minute, trying to make out which were the two sides of it; and as it was perfectly round, she found this a very difficult question."
    "However, at last she stretched her arms round it as far as they would go, and broke off a bit of the edge with each hand."

    camera:
        linear 0.5 xpos 800 ypos 815 zpos -1500
    alice "And now which is which?"
    "She nibbled a little of the right-hand bit to try the effect:"

    show alice normal at breathing(800, 0.2, 1.0):
        zpos -1000
        easein_expo 10.0 yzoom 0.1

    "The next moment she felt a violent blow underneath her chin: it had struck her foot!"



    "She was a good deal frightened by this very sudden change, but she felt that there was no time to be lost, as she was shrinking rapidly; so she set to work at once to eat some of the other bit."
    "Her chin was pressed so closely against her foot, that there was hardly room to open her mouth; but she did it at last, and managed to swallow a morsel of the lefthand bit."

    alice "Come, my head’s free at last!"
    show alice normal:
        zoom 0.2
        zpos -1000
        yzoom 0.1
        easeout_expo 10.0 yzoom 5.0
    "alice was delighted, which changed into alarm in another moment, when she found that her shoulders were nowhere to be found: all she could see, when she looked down, was an immense length of neck, which seemed to rise like a stalk out of a sea of green leaves that lay far below her."

    # switch scene to sky
label ch5_sky:

    scene sky:
        # center sky
        anchor (0.5, 0.5)
        xpos 0.5 ypos 0.5
        zoom 2.2
    camera:
        perspective True
        zpos 0
        easein 3.0 zrotate -5.0 xpos -30 ypos 30
        easeout 3.0 zrotate 0.0 xpos 0 ypos 0
        easein 3.0 zrotate 5.0 xpos 30 ypos 30
        easeout 3.0 zrotate 0.0 ypos 0 ypos 0
        repeat

    show cloud as cloud1:
        anchor (0.5, 0.5)
        xpos 0.0 ypos 0.2 zpos -1200

    show cloud as cloud2:
        anchor (0.5, 0.5)
        xpos 1.0 ypos 0.0 zpos -800

    show cloud as cloud3:
        anchor (0.5, 0.5)
        xpos 1.2 ypos 0.7 zpos -600

    alice "What can all that green stuff be?"
    alice "And where have my shoulders got to?"
    alice "And oh, my poor hands, how is it I can’t see you?"
    "She was moving them about as she spoke, but no result seemed to follow, except a little shaking among the distant green leaves."

    "As there seemed to be no chance of getting her hands up to her head, she tried to get her head down to them, and was delighted to find that her neck would bend about easily in any direction, like a serpent."

    show pigeon:
        zpos -1400 xpos 2.0
        easein 8.0 zpos 0.0 xpos 0.0
    "She had just succeeded in curving it down into a graceful zigzag, and was going to dive in among the leaves, which she found to be nothing but the tops of the trees under which she had been wandering, when a sharp hiss made her draw back in a hurry: a large pigeon had flown into her face, and was beating her violently with its wings."

    pigeon "Serpent!"

    alice "I’m not a serpent! Let me alone!"

    pigeon "Serpent, I say again!"
    pigeon "I’ve tried every way, and nothing seems to suit them!"

    alice "I haven’t the least idea what you’re talking about."

    pigeon "I’ve tried the roots of trees, and I’ve tried banks, and I’ve tried hedges, but those serpents! There’s no pleasing them!"

    "Alice was more and more puzzled, but she thought there was no use in saying anything more till the pigeon had finished."

    pigeon "As if it wasn’t trouble enough hatching the eggs, but I must be on the look-out for serpents night and day!"
    pigeon "Why, I haven’t had a wink of sleep these three weeks!"

    alice "I’m very sorry you’ve been annoyed."

    pigeon "And just as I’d taken the highest tree in the wood, and just as I was thinking I should be free of them at last, they must needs come wriggling down from the sky! Ugh, Serpent!" # ontinued the Pigeon, raising its voice to a shriek

    alice "But I’m not a serpent, I tell you!"
    alice "I’m a—I’m a—"

    pigeon "Well! What are you?"
    pigeon "I can see you’re trying to invent something!"

    alice "I—I’m a little girl..."
    "said Alice, rather doubtfully, as she remembered the number of changes she had gone through that day."

    pigeon "A likely story indeed!"
    pigeon "I’ve seen a good many little girls in my time, but never one with such a neck as that!"
    pigeon "No, no! You’re a serpent; and there’s no use denying it."
    pigeon "I suppose you’ll be telling me next that you never tasted an egg!"

    alice "I have tasted eggs, certainly, but little girls eat eggs quite as much as serpents do, you know."

    pigeon "I don’t believe it, but if they do, why then they’re a kind of serpent, that’s all I can say."

    "This was such a new idea to Alice, that she was quite silent for a minute or two."
    "..."

    pigeon "You’re looking for eggs, I know that well enough; and what does it matter to me whether you’re a little girl or a serpent?"

    alice "It matters a good deal to me, but I’m not looking for eggs, as it happens; and if I was, I shouldn’t want yours: I don’t like them raw."

    pigeon "Well, be off, then!"
    "Alice crouched down among the trees as well as she could, for her neck kept getting entangled among the branches, and every now and then she had to stop and untwist it."
    "After a while she remembered that she still held the pieces of mushroom in her hands, and she set to work very carefully, nibbling first at one and then at the other, and growing sometimes taller and sometimes shorter, until she had succeeded in bringing herself down to her usual height."

    scene forest
    camera:
        perspective False
        xpos 0 ypos 0 zpos 0 zrotate 0

    "It was so long since she had been anything near the right size, that it felt quite strange at first; but she got used to it in a few minutes, and began talking to herself, as usual."

    show alice happy at breathing(0.5, 0.6, 0.9)
    alice "Come, there’s half my plan done now!"
    alice "How puzzling all these changes are!" 
    alice "I’m never sure what I’m going to be, from one minute to another!"
    alice "However, I’ve got back to my right size: the next thing is, to get into that beautiful garden—how is that to be done, I wonder?"
    
    scene forest_house
    show alice happy at breathing(0.8, 0.7, 0.9)
    "She came suddenly upon an open place, with a little house in it about four feet high."
    alice "Whoever lives there, it’ll never do to come upon them this size: why, I should frighten them out of their wits!"
    show alice:
        linear 5.0 zoom 0.1
    "So she began nibbling at the righthand bit again, and did not venture to go near the house till she had brought herself down to nine inches high."

label chapter6:
    scene black
    "{size=+40}Chapter VI: \n{/size}Pig and Pepper"

    scene forest_house
    show footmen_fish at breathing(-0.5, 0.5, 0.9):
        linear 4.0 xpos 0.3

    "For a minute or two she stood looking at the house, and wondering what to do next, when suddenly a footman in livery came running out of the wood—(she considered him to be a footman because he was in livery: otherwise, judging by his face only, she would have called him a fish)—and rapped loudly at the door with his knuckles."

    play sound "sfx/knockknockknock.mp3"
    show footmen_frog at breathing(0.7, 0.5, 0.9)

    "It was opened by another footman in livery, with a round face, and large eyes like a frog; and both footmen, Alice noticed, had powdered hair that curled all over their heads."
    "She felt very curious to know what it was all about, and crept a little way out of the wood to listen."

    "The Fish-Footman began by producing from under his arm a great letter, nearly as large as himself, and this he handed over to the other, saying, in a solemn tone:"
    fishfoot "For the Duchess. An invitation from the Queen to play croquet."
    "The Frog-Footman repeated, in the same solemn tone, only changing the order of the words a little"
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

    "Then they both bowed low, and their curls got entangled together."



    "Alice laughed so much at this, that she had to run back into the wood for fear of their hearing her; "
    
    hide footmen_fish
    hide footmen_frog
    show footmen_frog at breathing(0.7, 0.5, 0.9)
    "and when she next peeped out the Fish-Footman was gone, and the other was sitting on the ground near the door, staring stupidly up into the sky."

    show alice normal at breathing(0.3, 0.5, 0.9)
    play sound "sfx/knockknockknock.mp3"
    "Alice went timidly up to the door, and knocked."

    fishfoot "There’s no sort of use in knocking, and that for two reasons. First, because I’m on the same side of the door as you are; secondly, because they’re making such a noise inside, no one could possibly hear you."

    #play sound "sfx/shatter.mp3"
    "And certainly there was a most extraordinary noise going on within—a constant howling and sneezing, and every now and then a great crash, as if a dish or kettle had been broken to pieces."

    alice "Please, then, how am I to get in?"

    fishfoot "There might be some sense in your knocking, if we had the door between us. For instance, if you were inside, you might knock, and I could let you out, you know."

    "He was looking up into the sky all the time he was speaking, and this Alice thought decidedly uncivil."

    alice "But perhaps he can’t help it, his eyes are so very nearly at the top of his head. But at any rate he might answer questions."

    alice "How am I to get in?"

    fishfoot "I shall sit here, till tomorrow—"

    play sound "<silence 2.0>"
    queue sound "sfx/shatter.mp3"
    show plate: # at center
        anchor(0.5, 0.5)
        xpos 1.5 ypos 0.4 zoom 0.5
        linear 2.0 xpos -0.5

    "At this moment the door of the house opened, and a large plate came skimming out, straight at the Footman’s head: it just grazed his nose, and broke to pieces against one of the trees behind him."


    fishfoot "—or next day, maybe,"

    #"The Footman continued in the same tone, exactly as if nothing had happened."

    alice "How am I to get in?" # asked Alice again, in a louder tone.

    fishfoot "Are you to get in at all? That’s the first question, you know."

    "It was, no doubt: only Alice did not like to be told so."

    alice "It’s really dreadful, the way all the creatures argue. It’s enough to drive one crazy!"

    "The Footman seemed to think this a good opportunity for repeating his remark, with variations."

    fishfoot "I shall sit here, on and off, for days and days."

    alice "But what am I to do?"

    fishfoot "Anything you like" # said the Footman, and began whistling.

    alice "Oh, there’s no use in talking to him, he’s perfectly idiotic!"

    play sound "sfx/door_open.mp3"
    "And she opened the door and went in."

label ch6_kitchen:
    scene kitchen
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
    show alice normal at breathing(alice_kitchen_pos, 0.5, 0.9)
    show cook at breathing(cook_kitchen_pos, 0.6, 0.9)
    show cat:
        align (0.5, 1.0)
        xpos cat_kitchen_pos ypos 0.59 zoom 0.63
    show duchess at breathing(duchess_kitchen_pos, 0.6, 0.9)
    show baby normal:
        anchor (0.5, 1.0)
        xpos duchess_kitchen_pos ypos 0.75 zoom 0.7 zpos 30
        linear 1.0 xoffset -10 yoffset -10 rotate 2
        linear 1.0 xoffset 10 yoffset 10 rotate -2
        linear 1.0 xoffset -10 yoffset 10 rotate 2
        linear 1.0 xoffset 10 yoffset -10 rotate -2
        repeat
    
    "The door led right into a large kitchen, which was full of smoke from one end to the other: the Duchess was sitting on a three-legged stool in the middle, nursing a baby; the cook was leaning over the fire, stirring a large cauldron which seemed to be full of soup."

    alice "(There’s certainly too much pepper in that soup!)" # Alice said to herself, as well as she could for sneezing.

    "There was certainly too much of it in the air. Even the Duchess sneezed occasionally; and as for the baby, it was sneezing and howling alternately without a moment’s pause."

    "The only things in the kitchen that did not sneeze, were the cook, and a large cat which was sitting on the hearth and grinning from ear to ear."

    camera:
        ease cam_transition xpos cat_kitchen_pos zpos cat_cam_z_zom
    alice "Please would you tell me, why your cat grins like that?" # said Alice, a little timidly, for she was not quite sure whether it was good manners for her to speak first

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    duchess "It’s a Cheshire cat, and that’s why. Pig!"

    camera:
        ease cam_transition xpos alice_duchess_kitchen_pos zpos 0
    show alice:
        ease 0.3 yoffset -100
        ease 0.3 yoffset 0
    "She said the last word with such sudden violence that Alice quite jumped; but she saw in another moment that it was addressed to the baby, and not to her, so she took courage, and went on again:"

    show alice surprised
    alice "I didn’t know that Cheshire cats always grinned; in fact, I didn’t know that cats could grin."

    duchess "They all can, and most of ’em do."

    alice "I don’t know of any that do."

    show alice normal
    "Alice said very politely, feeling quite pleased to have got into a conversation."

    duchess "You don’t know much, and that’s a fact."

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

    "While she was trying to fix on one, the cook took the cauldron of soup off the fire, and at once set to work throwing everything within her reach at the Duchess and the baby—the fire-irons came first; then followed a shower of saucepans, plates, and dishes."

    hide plate1
    hide plate2
    hide plate3
    "The Duchess took no notice of them even when they hit her; and the baby was howling so much already, that it was quite impossible to say whether the blows hurt it or not."
    
    show alice pout
    alice "Oh, please mind what you’re doing!"
    "cried Alice, jumping up and down in an agony of terror."#
    alice "Oh, there goes his precious nose"

    show saucepan:
        anchor(0.5, 0.5)
        xpos cook_kitchen_pos ypos 0.7 zoom 1.0
        linear 4.0 xpos -600
    "An unusually large saucepan flew close by it, and very nearly carried it off."

    duchess "If everybody minded their own business, the world would go round a deal faster than it does." # the Duchess said in a hoarse growl, "
    hide saucepan

    show alice normal
    alice "Which would not be an advantage. Just think what work it would make with the day and night! You see the earth takes twenty-four hours to turn round on its axis—"

    duchess "Talking of axes, chop off her head!"

    show alice pout

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0
    "Alice glanced rather anxiously at the cook, to see if she meant to take the hint; but the cook was busily stirring the soup, and seemed not to be listening, so she went on again:"

    show alice normal
    camera:
        ease cam_transition xpos alice_kitchen_pos zpos 0

    alice "Twenty-four hours, I think; or is it twelve? I—"

    duchess "Oh, don’t bother me, I never could abide figures!" 
    "And with that she began nursing her child again, singing a sort of lullaby to it as she did so, and giving it a violent shake at the end of every line:"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    duchess "Speak roughly to your little boy,\n{space=30}And beat him when he sneezes:\nHe only does it to annoy,\n{space=30}Because he knows it teases."

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0

    #"CHORUS.\n(In which the cook and the baby joined):"

    everyone "Wow! wow! wow!"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    "While the Duchess sang the second verse of the song, she kept tossing the baby violently up and down, and the poor little thing howled so, that Alice could hardly hear the words:"

    duchess "I speak severely to my boy,\n{space=30}I beat him when he sneezes;\nFor he can thoroughly enjoy\n{space=30}The pepper when he pleases!"

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0    
    everyone "Wow! wow! wow!"

    camera:
        ease cam_transition xpos duchess_kitchen_pos zpos 0
    duchess "Here! you may nurse it a bit, if you like!" 
    
    show baby normal:
        ease 1.0 xpos alice_kitchen_pos ypos 0.8
    "The Duchess said to Alice, flinging the baby at her as she spoke."
    duchess "I must go and get ready to play croquet with the Queen."
    "The duchess hurried out of the room."
    show duchess:
        linear 3.0 xpos 3000

    camera:
        ease cam_transition xpos cook_kitchen_pos zpos 0
    "The cook threw a frying-pan after her as she went out, but it just missed her."

    camera:
        ease cam_transition xpos alice_kitchen_pos zpos 0
    
    "Alice caught the baby with some difficulty, as it was a queer-shaped little creature, and held out its arms and legs in all directions."
    show alice surprised
    alice "Just like a star-fish."
    "The poor little thing was snorting like a steam-engine when she caught it, and kept doubling itself up and straightening itself out again, so that altogether, for the first minute or two, it was as much as she could do to hold it."

    scene black
    camera:
        perspective False
        xpos 0 zpos 0 xoffset 0
    "As soon as she had made out the proper way of nursing it, (which was to twist it up into a sort of knot, and then keep tight hold of its right ear and left foot, so as to prevent its undoing itself,) she carried it out into the open air."


    scene forest

    show alice pout at breathing(0.5, 0.5, 0.9)
    show baby normal:
        anchor (0.5, 1.0)
        xpos 0.5 ypos 0.8 zoom 0.7
        linear 1.0 xoffset -10 yoffset -10 rotate 2
        linear 1.0 xoffset 10 yoffset 10 rotate -2
        linear 1.0 xoffset -10 yoffset 10 rotate 2
        linear 1.0 xoffset 10 yoffset -10 rotate -2
        repeat

    alice "(If I don’t take this child away with me, they’re sure to kill it in a day or two:)"
    alice "wouldn’t it be murder to leave it behind?"
    "The little thing grunted in reply (it had left off sneezing by this time)."
    alice "Don’t grunt, that’s not at all a proper way of expressing yourself."

    "The baby grunted again, and Alice looked very anxiously into its face to see what was the matter with it."
    show baby half
    "There could be no doubt that it had a very turn-up nose, much more like a snout than a real nose; also not like the look of the thing at all."
    alice "But perhaps it was only sobbing"
    "She looked into its eyes again, to see if there were any tears."

    "No, there were no tears"
    alice "If you’re going to turn into a pig, my dear, I’ll have nothing more to do with you. Mind now!"
    "The poor little thing sobbed again (or grunted, it was impossible to say which), and they went on for some while in silence."

    alice "Now, what am I to do with this creature when I get it home?"
    "Then it grunted again, so violently, that she looked down into its face in some alarm."

    show baby pig
    "This time there could be no mistake about it: it was neither more nor less than a pig, and she felt that it would be quite absurd for her to carry it further."

    hide baby
    "So she set the little creature down, and felt quite relieved to see it trot away quietly into the wood."

    alice "If it had grown up, it would have made a dreadfully ugly child: but it makes rather a handsome pig, I think."

    "And she began thinking over other children she knew, who might do very well as pigs."

    alice "If one only knew the right way to change them—"

    "She got a little startled by seeing the Cheshire Cat sitting on a bough of a tree a few yards off."

    show cat:
        anchor (0.5, 1.0)
        xpos 0.79 ypos 0.25 zoom 0.5

    "The Cat only grinned when it saw Alice."
    "It looked good-natured, she thought: still it had very long claws and a great many teeth, so she felt that it ought to be treated with respect."

    alice "Cheshire Puss," 
    "she began, rather timidly, as she did not at all know whether it would like the name: however, it only grinned a little wider."
    alice "Come, it’s pleased so far."
    alice "Would you tell me, please, which way I ought to go from here?"

    cat "That depends a good deal on where you want to get to."
    
    alice "I don’t much care where—"

    cat "Then it doesn’t matter which way you go."

    alice "—so long as I get somewhere."

    cat "Oh, you’re sure to do that, if you only walk long enough."

    "Alice felt that this could not be denied, so she tried another question."

    alice "What sort of people live about here?"

    cat "In that direction, lives a Hatter: and in that direction, lives a March Hare. Visit either you like: they’re both mad."

    alice "But I don’t want to go among mad people."

    cat "Oh, you can’t help that. We’re all mad here. I’m mad. You’re mad."

    alice "How do you know I’m mad?"

    cat "You must be, or you wouldn’t have come here."

    "Alice didn’t think that proved it at all; however, she went on:"

    alice "And how do you know that you’re mad?"

    cat "To begin with, a dog’s not mad. You grant that?"

    alice "I suppose so,"

    cat "Well, then, you see, a dog growls when it’s angry, and wags its tail when it’s pleased. Now I growl when I’m pleased, and wag my tail when I’m angry. Therefore I’m mad."

    alice "I call it purring, not growling,"

    cat "Call it what you like."
    cat "Do you play croquet with the Queen today?"

    alice "I should like it very much, but I haven’t been invited yet."

    cat "You’ll see me there."

    hide cat
    "The Cat vanished."

    "Alice was not much surprised at this, she was getting so used to queer things happening."

    "While she was looking at the place where it had been, it suddenly appeared  again." # the cat appeared again

    show cat:
        anchor (0.5, 1.0)
        xpos 0.79 ypos 0.25 zoom 0.5
    cat "By the by, what became of the baby?"
    cat "I’d nearly forgotten to ask."

    alice "It turned into a pig."

    cat "I thought it would." # said the cat and VANISHED again

    hide cat
    "The Cat vanished again."

    "Alice waited a little, half expecting to see it again, but it did not appear, and after a minute or two she walked on in the direction in which the March Hare was said to live."

    alice "I’ve seen hatters before, the  March Hare will be much the most interesting, and perhaps as this is May it won’t be raving mad—at least not so mad as it was in March."

label ch6_cat:
    show cat:
        anchor (0.5, 1.0)
        xpos 0.79 ypos 0.25 zoom 0.5
        
    "As she said this, she looked up, and there was the Cat again, sitting on a branch of a tree."

    cat "Did you say pig, or fig?"

    alice "I said pig, and I wish you wouldn’t keep appearing and vanishing so suddenly: you make one quite giddy."

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
        xpos 0.79 ypos 0.25 zoom 0.5

    "This time it vanished quite slowly, beginning with the end of the tail, and ending with the grin, which remained some time after the rest of it had gone."

    alice "Well! I’ve often seen a cat without a grin, but a grin without a cat! It’s the most curious thing I ever saw in my life!"

    scene hare_house
    "She had not gone much farther before she came in sight of the house of the March Hare: she thought it must be the right house, because the chimneys were shaped like ears and the roof was thatched with fur."

    "It was so large a house, that she did not like to go nearer till she had nibbled some more of the lefthand bit of mushroom, and raised herself to about two feet high: even then she walked up towards it rather timidly"    

    alice "Suppose it should be raving mad after all! I almost wish I’d gone to see the Hatter instead!"

label chapter7:
    scene black
    "{size=+40}Chapter VII: \n{/size}A Mad Tea-Party"

    scene hare_house


label chapter8:
    scene black
    "{size=+40}Chapter VIII: \n{/size}The Queen's Croquet-Ground"

label chapter9:
    scene black
    "{size=+40}Chapter IX: \n{/size}The Mock Turtle's Story"

label chapter10:
    scene black
    "{size=+40}Chapter X: \n{/size}The Lobster Quadrille"

label chapter11:
    scene black
    "{size=+40}Chapter XI: \n{/size}Who Stole the Tarts?"

label chapter12:
    scene black
    "{size=+40}Chapter XII: \n{/size}Alice's Evidence"

    
