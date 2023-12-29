﻿define alice = Character("Alice", color="#ADD8E6")
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

image riverbank = "riverbank.png"

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
    ease 3.0 yzoom 0.99
    ease 3.0 yzoom 1.0
    repeat

transform breathing(xposition, scale = 1.0):
    pos (xposition, 0.7)
    anchor (0.5, 1.0)
    zoom scale
    ease 2.0 yzoom 0.99
    ease 2.0 yzoom 1.0
    repeat

transform breathing_crying(xposition, scale = 1.0):
    pos (xposition, 0.7)
    anchor (0.5, 1.0)
    zoom scale
    ease 1.0 yzoom 0.995
    ease 1.0 yzoom 0.99
    ease 2.5 yzoom 1.0
    repeat

transform alice_growing_large:
    pos (0.5, 0.7)
    anchor (0.5, 1.0)
    zoom 0.5
    easeout 60.0 zoom 10.0

transform pan_background_to_center:
    xalign 0.0
    linear 15.0 xalign 0.5

default alice_scale = 0.5

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
    "Just then, her head struck against the roof of the hall: in fact she was now rather more than nine feet high, and she at once took up the little golden key and hurried off to the garden door."
    "Poor Alice! It was as much as she could do, lying down on one side, to look through into the garden with one eye; but to get through was more hopeless than ever: she sat down and began to cry again."
    show alice crying at breathing_crying(0.5, alice_scale)

    alice "You ought to be ashamed of yourself, a great girl like you, to go on crying in this way! Stop this moment, I tell you!"
    "But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall."

    show alice pout at breathing(0.5, alice_scale)
    "After a time she heard a little pattering of feet in the distance, and she hastily dried her eyes to see what was coming."
    "It was the White Rabbit returning, splendidly dressed, with a pair of white kid gloves in one hand and a large fan in the other:"
    "he came trotting along in a great hurry, muttering to himself as he came,"
    hide alice
    show rabbit normal at breathing(0.5)
    rabbit "Oh! the Duchess, the Duchess! Oh! won’t she be savage if I’ve kept her waiting!"
    "Alice felt so desperate that she was ready to ask help of any one; so, when the Rabbit came near her, she began, in a low, timid voice,"
    hide rabbit
    show alice pout at breathing(0.5, alice_scale)
    alice "If you please, sir—"
    "The Rabbit started violently, dropped the white kid gloves and the fan, and skurried away into the darkness as hard as he could go."

    "Alice took up the fan and gloves, and, as the hall was very hot, she kept fanning herself all the time she went on talking:"

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

    show alice crying at breathing_crying(0.5, alice_scale)
    alice "I’m sure those are not the right words"
    alice "I must be Mabel after all, and I shall have to go and live in that poky little house, and have next to no toys to play with, and oh!"
    alice "Ever so many lessons to learn! No, I’ve made up my mind about it; if I’m Mabel, I’ll stay down here!" 
    alice "It’ll be no use their putting their heads down and saying 'Come up again, dear!' I shall only look up and say 'Who am I then?" 
    alice "Tell me that first, and then, if I like being that person, I’ll come up: if not, I’ll stay down here till I’m somebody else' —but, oh dear!"
    alice "I do wish they would put their heads down! I am so very tired of being all alone here!"

    "As she said this she looked down at her hands, and was surprised to see that she had put on one of the Rabbit’s little white kid gloves while she was talking."
    alice "How can I have done that?"
    alice "I must be growing small again."
    "She got up and went to the table to measure herself by it, and found that, as nearly as she could guess, she was now about two feet high, and was going on shrinking rapidly:"
    "she soon found out that the cause of this was the fan she was holding, and she dropped it hastily, just in time to avoid shrinking away altogether."

    alice "That was a narrow escape!"
    "She was a good deal frightened at the sudden change, but very glad to find herself still in existence."
    alice "And now for the garden!"
    "And she ran with all speed back to the little door: but, alas! the little door was shut again, and the little golden key was lying on the glass table as before,"
    alice  "And things are worse than ever, for I never was so small as this before, never! And I declare it’s too bad, that it is!"

    play sound "sfx/splash.mp3"
    "As she said these words her foot slipped, and in another moment, splash!"
    "she was up to her chin in salt water."
    "Her first idea was that she had somehow fallen into the sea, "
    alice "and in that case I can go back by railway"
    "(Alice had been to the seaside once in her life, and had come to the general conclusion, that wherever you go to on the English coast you find a number of bathing machines in the sea, some children digging in the sand with wooden spades, then a row of lodging houses, and behind them a railway station)"
    "However, she soon made out that she was in the pool of tears which she had wept when she was nine feet high."

    alice "I wish I hadn’t cried so much!"
    "She swam about, trying to find her way out."
    alice "I shall be punished for it now, I suppose, by being drowned in my own tears! That will be a queer thing, to be sure! However, everything is queer to-day."

    "Just then she heard something splashing about in the pool a little way off, and she swam nearer to make out what it was:"
    "at first she thought it must be a walrus or hippopotamus, but then she remembered how small she was now, and she soon made out that it was only a mouse that had slipped in like herself."

    alice "Would it be of any use, now, to speak to this mouse?"
    alice "Everything is so out-of-the-way down here, that I should think very likely it can talk: at any rate, there’s no harm in trying."
    "So she began:"
    alice "O Mouse, do you know the way out of this pool? I am very tired of swimming about here, O Mouse!"
    "(Alice thought this must be the right way of speaking to a mouse: she had never done such a thing before, but she remembered having seen in her brother’s Latin Grammar, 'A mouse—of a mouse—to a mouse—a mouse—O mouse!')"
    "The Mouse looked at her rather inquisitively, and seemed to her to wink with one of its little eyes, but it said nothing."

    alice "Perhaps it doesn’t understand English, I daresay it’s a French mouse, come over with William the Conqueror."
    "(For, with all her knowledge of history, Alice had no very clear notion how long ago anything had happened)"
    "So she began again:"
    alice "Où est ma chatte?"
    "which was the first sentence in her French lesson-book."
    "The mouse gave a sudden leap out of the water, and seemed to quiver all over with fright."
    alice "Oh, I beg your pardon!"
    "She was afraid that she had hurt the poor animal’s feelings."
    alice "I quite forgot you didn’t like cats."

    mouse "Not like cats!"
    mouse "Would you like cats if you were me?"

    alice "Well, perhaps not, don’t be angry about it."
    alice "And yet I wish I could show you our cat Dinah: I think you’d take a fancy to cats if you could only see her."
    alice "She is such a dear quiet thing,"
    "Alice went on, half to herself, as she swam lazily about in the pool,"
    alice "and she sits purring so nicely by the fire, licking her paws and washing her face—and she is such a nice soft thing to nurse—and she’s such a capital one for catching mice—oh, I beg your pardon!"
    "This time the Mouse was bristling all over, and she felt certain it must be really offended."
    alice "We won’t talk about her any more if you’d rather not."

    mouse "We indeed!"
    "The mouse was trembling down to the end of its tail."
    mouse "As if I would talk on such a subject! Our family always hated cats: nasty, low, vulgar things! Don’t let me hear the name again!"

    alice "I won’t indeed!"
    "alice was in a great hurry to change the subject of conversation."
    alice "Are you—are you fond—of—of dogs?"
    "The mouse did not answer, so Alice went on eagerly:"
    alice "There is such a nice little dog near our house I should like to show you!"
    alice "A little bright-eyed terrier, you know, with oh, such long curly brown hair!"
    alice "And it’ll fetch things when you throw them, and it’ll sit up and beg for its dinner, and all sorts of things—I can’t remember half of them—and it belongs to a farmer, you know, and he says it’s so useful, it’s worth a hundred pounds!"
    alice "He says it kills all the rats and—oh dear!"
    "Alice cried in a sorrowful tone"
    alice "I’m afraid I’ve offended it again!"
    "For the Mouse was swimming away from her as hard as it could go, and making quite a commotion in the pool as it went."

    alice "Mouse dear! Do come back again, and we won’t talk about cats or dogs either, if you don’t like them!"
    "When the Mouse heard this, it turned round and swam slowly back to her: its face was quite pale (with passion, Alice thought), and it said in a low trembling voice,"
    mouse "Let us get to the shore, and then I’ll tell you my history, and you’ll understand why it is I hate cats and dogs."

    "It was high time to go, for the pool was getting quite crowded with the birds and animals that had fallen into it: there were a Duck and a Dodo, a Lory and an Eaglet, and several other curious creatures."
    "Alice led the way, and the whole party swam to the shore."



label chapter3:
    scene black 
    "{size=+40}Chapter III: \n{/size}A Caucus-Race and a Long Tale"

    # TODO new scene for shore?

    "They were indeed a queer-looking party that assembled on the bank—the birds with draggled feathers, the animals with their fur clinging close to them, and all dripping wet, cross, and uncomfortable."

    "The first question of course was, how to get dry again: they had a consultation about this, and after a few minutes it seemed quite natural to Alice to find herself talking familiarly with them, as if she had known them all her life."
    "Indeed, she had quite a long argument with the Lory, who at last turned sulky, and would only say"
    lory "I am older than you, and must know better"
    "and this Alice would not allow without knowing how old it was, and, as the Lory positively refused to tell its age, there was no more to be said."

    "At last the Mouse, who seemed to be a person of authority among them, called out:"
    mouse "Sit down, all of you, and listen to me! I’ll soon make you dry enough!"
    "They all sat down at once, in a large ring, with the Mouse in the middle."
    "Alice kept her eyes anxiously fixed on it, for she felt sure she would catch a bad cold if she did not get dry very soon."

    mouse "Ahem!"
    mouse "Are you all ready? This is the driest thing I know."
    mouse "Silence all round, if you please!"
    mouse "'William the Conqueror, whose cause was favoured by the pope, was soon submitted to by the English, who wanted leaders, and had been of late much accustomed to usurpation and conquest." 
    mouse "Edwin and Morcar, the earls of Mercia and Northumbria—'"

    lory "Ugh!"

    mouse "I beg your pardon!"
    mouse "Did you speak?"

    lory "Not I!"

    mouse "I thought you did, —I proceed."
    mouse "'Edwin and Morcar, the earls of Mercia and Northumbria, declared for him: and even Stigand, the patriotic archbishop of Canterbury, found it advisable—'"

    duck "Found what?"

    mouse "Found it, of course you know what 'it' means."

    duck "I know what 'it' means well enough, when I find a thing, it’s generally a frog or a worm. The question is, what did the archbishop find?"

    "The Mouse did not notice this question, but hurriedly went on,"

    mouse "'—found it advisable to go with Edgar Atheling to meet William and offer him the crown. William’s conduct at first was moderate. But the insolence of his Normans—'"
    "it continued, turning to Alice as it spoke."
    mouse "How are you getting on now, my dear?"

    alice "As wet as ever, it doesn’t seem to dry me at all."

    dodo "In that case, I move that the meeting adjourn, for the immediate adoption of more energetic remedies—"

    eaglet "Speak English! I don’t know the meaning of half those long words, and, what’s more, I don’t believe you do either!"
    "And the Eaglet bent down its head to hide a smile: some of the other birds tittered audibly."

    dodo "What I was going to say, was that the best thing to get us dry would be a Caucus-race."

    "..."

    alice "What is a Caucus-race?"

    "not that she wanted much to know, but the Dodo had paused as if it thought that somebody ought to speak, and no one else seemed inclined to say anything."

    dodo "Why, the best way to explain it is to do it."

    "(And, as you might like to try the thing yourself, some winter day, I will tell you how the Dodo managed it)"

    "First it marked out a race-course, in a sort of circle."
    dodo "The exact shape doesn’t matter"
    "And then all the party were placed along the course, here and there."
    "There was no 'One, two, three, and away', but they began running when they liked, and left off when they liked, so that it was not easy to know when the race was over."
    "However, when they had been running half an hour or so, and were quite dry again, the Dodo suddenly called out:"
    dodo "The race is over!"
    "and they all crowded round it, panting, and asking, "
    everyone "But who has won?"

    "This question the Dodo could not answer without a great deal of thought, and it sat for a long time with one finger pressed upon its forehead (the position in which you usually see Shakespeare, in the pictures of him), while the rest waited in silence."
    dodo "Everybody has won, and all must have prizes."

    everyone "But who is to give the prizes?"
    dodo "Why, she, of course," 
    "said the Dodo, pointing to Alice with one finger; and the whole party at once crowded round her, calling out in a confused way,"
    everyone "Prizes! Prizes!"

    "Alice had no idea what to do, and in despair she put her hand in her pocket, and pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes."
    "There was exactly one a-piece all round."

    mouse "But she must have a prize herself, you know."

    dodo "Of course. What else have you got in your pocket?"
    "The dodo truned to Alice"

    alice "Only a thimble."
    dodo "Hand it over here."

    "Then they all crowded round her once more, while the Dodo solemnly presented the thimble"
    dodo "We beg your acceptance of this elegant thimble."
    "And, when it had finished this short speech, they all cheered."

    "Alice thought the whole thing very absurd, but they all looked so grave that she did not dare to laugh; and, as she could not think of anything to say, she simply bowed, and took the thimble, looking as solemn as she could."

    "The next thing was to eat the comfits: this caused some noise and confusion, as the large birds complained that they could not taste theirs, and the small ones choked and had to be patted on the back."
    "However, it was over at last, and they sat down again in a ring, and begged the Mouse to tell them something more."

    alice "You promised to tell me your history, you know,"
    alice "and why it is you hate—C and D"
    "alice added in a whisper, half afraid that it would be offended again."

    mouse "Mine is a long and a sad tale!"

    alice "It is a long tail, certainly, but why do you call it sad?"
    "She kept on puzzling about it while the Mouse was speaking, so that her idea of the tale was something like this:—"

    "Fury said to a mouse, That he met in the house, 'Let us both go to law: I will prosecute you.—Come, I’ll take no denial; We must have a trial: For really this morning I’ve nothing to do.'"
    "Said the mouse to the cur, 'Such a trial, dear Sir, With no jury or judge, would be wasting our breath.'"
    "'I’ll be judge, I’ll be jury,' Said cunning old Fury: 'I’ll try the whole cause, and condemn you to death.'"

    mouse "You are not attending!"
    mouse "What are you thinking of?"

    alice "I beg your pardon, you had got to the fifth bend, I think?"

    mouse "I had not!" # cried the Mouse, sharply and very angrily.

    alice "A knot!" # said Alice, always ready to make herself useful, and looking anxiously about her. 
    alice "Oh, do let me help to undo it!"

    mouse "I shall do nothing of the sort."
    "the mouse gets up and walks away."
    mouse "You insult me by talking such nonsense!"

    alice "I didn’t mean it! But you’re so easily offended, you know!"

    "The mouse only growled in reply."

    alice "Please come back and finish your story!"
    "All the others joined in chorus"
    everyone "Yes, please do!"
    "but the Mouse only shook its head impatiently, and walked a little quicker."

    lory "What a pity it wouldn’t stay!"
    "sighed the Lory, as soon as it was quite out of sight; and an old Crab took the opportunity of saying to her daughter"
    old_crab "Ah, my dear! Let this be a lesson to you never to lose your temper!"
    young_crab "Hold your tongue, Ma! You’re enough to try the patience of an oyster!"

    alice "I wish I had our Dinah here, I know I do!"
    alice "She’d soon fetch it back!"

    lory "And who is Dinah, if I might venture to ask the question?"

    alice "Dinah’s our cat. And she’s such a capital one for catching mice you can’t think! And oh, I wish you could see her after the birds! Why, she’ll eat a little bird as soon as look at it!"

    "This speech caused a remarkable sensation among the party. Some of the birds hurried off at once: one old Magpie began wrapping itself up very carefully"
    magpie "I really must be getting home; the night-air doesn’t suit my throat!"
    "and a Canary called out in a trembling voice to its children"
    canary "Come away, my dears! It’s high time you were all in bed!"
    "On various pretexts they all moved off, and Alice was soon left alone."

    alice "I wish I hadn’t mentioned Dinah!"
    alice "Nobody seems to like her, down here, and I’m sure she’s the best cat in the world!"
    alice "Oh, my dear Dinah! I wonder if I shall ever see you any more!"
    show alice crying at breathing_crying(0.5, alice_scale)
    "And here poor Alice began to cry again, for she felt very lonely and low-spirited."
    "In a little while, however, she again heard a little pattering of footsteps in the distance, and she looked up eagerly, half hoping that the Mouse had changed his mind, and was coming back to finish his story."

label chapter4:
    scene black
    "{size=+40}Chapter IV: \n{/size}The Rabbit Sends in a Little Bill"

    "It was the White Rabbit, trotting slowly back again, and looking anxiously about as it went, as if it had lost something; and she heard it muttering to itself"
    rabbot  "The Duchess! The Duchess! Oh my dear paws! Oh my fur and whiskers! She’ll get me executed, as sure as ferrets are ferrets! Where can I have dropped them, I wonder?"
    "Alice guessed in a moment that it was looking for the fan and the pair of white kid gloves, and she very good-naturedly began hunting about for them, but they were nowhere to be seen—everything seemed to have changed since her swim in the pool, and the great hall, with the glass table and the little door, had vanished completely."

    "Very soon the Rabbit noticed Alice, as she went hunting about, and called out to her in an angry tone"
    rabbit "Why, Mary Ann, what are you doing out here? Run home this moment, and fetch me a pair of gloves and a fan! Quick, now!"
    "And Alice was so much frightened that she ran off at once in the direction it pointed to, without trying to explain the mistake it had made."

    alice "He took me for his housemaid. How surprised he’ll be when he finds out who I am! But I’d better take him his fan and gloves—that is, if I can find them."
    "As she said this, she came upon a neat little house, on the door of which was a bright brass plate with the name 'W. RABBIT' engraved upon it."
    "She went in without knocking, and hurried upstairs, in great fear lest she should meet the real Mary Ann, and be turned out of the house before she had found the fan and gloves."

    alice "How queer it seems, to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!"
    "And she began fancying the sort of thing that would happen:"
    alice "'Miss Alice! Come here directly, and get ready for your walk!' 'Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.'"
    alice "Only I don’t think, that they’d let Dinah stop in the house if it began ordering people about like that!"

    "By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves:"
    alice "she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass."
    play sound "sfx/cork.mp3"
    "There was no label this time with the words 'DRINK ME', but nevertheless she uncorked it and put it to her lips."
    alice "I know something interesting is sure to happen, whenever I eat or drink anything; so I’ll just see what this bottle does."
    alice "I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!"

    "It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken."
    "She hastily put down the bottle."
    alice "That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!"

    "Alas! it was too late to wish that! She went on growing, and growing, and very soon had to kneel down on the floor:"
    "In another minute there was not even room for this, and she tried the effect of lying down with one elbow against the door, and the other arm curled round her head."
    "Still she went on growing, and, as a last resource, she put one arm out of the window, and one foot up the chimney"
    alice "Now I can do no more, whatever happens. What will become of me?"

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
    "Then came a little pattering of feet on the stairs."
    "Alice knew it was the Rabbit coming to look for her, and she trembled till she shook the house, quite forgetting that she was now about a thousand times as large as the Rabbit, and had no reason to be afraid of it."

    "Presently the Rabbit came up to the door, and tried to open it; but, as the door opened inwards, and Alice’s elbow was pressed hard against it, that attempt proved a failure."
    rabbit "Then I’ll go round and get in at the window."

    alice "That you won’t!"
    "thought Alice, and, after waiting till she fancied she heard the Rabbit just under the window, she suddenly spread out her hand, and made a snatch in the air."
    "She did not get hold of anything, but she heard a little shriek and a fall, and a crash of broken glass, from which she concluded that it was just possible it had fallen into a cucumber-frame, or something of the sort."

    "Next came an angry voice—"
    rabbit "Pat! Pat! Where are you?"
    "And then a voice she had never heard before, "
    pat "Sure then I’m here! Digging for apples, yer honour!"

    

label chapter5:
    scene black
    "{size=+40}Chapter V: \n{/size}Advice from a Caterpillar"

label chapter6:
    scene black
    "{size=+40}Chapter VI: \n{/size}Pig and Pepper"

label chapter7:
    scene black
    "{size=+40}Chapter VII: \n{/size}A Mad Tea-Party"

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

    
