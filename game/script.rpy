define alice = Character("Alice", color="#c8ffc8")
define rabbit = Character("Rabbit", color="#c8ffc8")

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

transform pan_background_to_center:
    xalign 0.0
    linear 15.0 xalign 0.5

label start:
    #jump chapter1_after_fall
label chapter1:

    scene riverbank at left
    play music "audio/rinne wanderer.mp3"
    show alice sleepy
    "Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it."


    # voice "voice/alice001.mp3"
    alice "And what is the use of a book without pictures or conversations?" 

    "So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself:"

    scene riverbank at center
    #show alice normal at left as grayscale
    hide alice
    show rabbit normal

    rabbit "Oh dear! Oh dear! I shall be too late!"

    "(when she thought it over afterwards, it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural)"
    "But when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and fortunately was just in time to see it pop down a large rabbit-hole under the hedge."

    hide rabbit
    show alice happy
    "In another moment down went Alice after it, never once considering how in the world she was to get out again."

    scene well at center 
    play music "audio/rinne aurelia.mp3" fadeout 1.0 fadein 1.0 

    show alice falling at falling

    "The rabbit-hole went straight on like a tunnel for some way,"
    "and then dipped suddenly down, so suddenly that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well."

    "Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next."

    "First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs."

    "She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody underneath, so managed to put it into one of the cupboards as she fell past it."

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
    "when suddenly, thump! thump! down she came upon a heap of sticks and dry leaves, and the fall was over."

label chapter1_after_fall:

    stop music fadeout 1.0
    scene black
    
    "Alice was not a bit hurt, and she jumped up on to her feet in a moment: she looked up, but it was all dark overhead;"

    scene hall at pan_background_to_center
    play music "audio/rinne memories of clockwise tower.mp3" fadein 1.0

    "before her was another long passage, and the White Rabbit was still in sight, hurrying down it."

    "There was not a moment to be lost: away went Alice like the wind, and was just in time to hear it say, as it turned a corner"

    hide alice
    show rabbit normal
    rabbit "Oh my ears and whiskers, how late it's getting!"
    hide rabbit

    show alice happy

    "She was close behind it when she turned the corner, but the Rabbit was no longer to be seen: she found herself in a long, low hall, which was lit up by a row of lamps hanging from the roof."

    show alice pout
    "There were doors all round the hall, but they were all locked; and when Alice had been all the way down one side and up the other, trying every door, she walked sadly down the middle, wondering how she was ever to get out again."

    "Suddenly she came upon a little three-legged table, all made of solid glass; there was nothing on it except a tiny golden key, and Alice’s first thought was that it might belong to one of the doors of the hall; but, alas! either the locks were too large, or the key was too small, but at any rate it would not open any of them."

    scene small_door at center
    "However, on the second time round, she came upon a low curtain she had not noticed before, and behind it was a little door about fifteen inches high: she tried the little golden key in the lock, and to her great delight it fitted!"

    "Alice opened the door and found that it led into a small passage, not much larger than a rat-hole: she knelt down and looked along the passage into the loveliest garden you ever saw."

    "How she longed to get out of that dark hall, and wander about among those beds of bright flowers and those cool fountains, but she could not even get her head through the doorway;"

    show alice pout
    alice "and even if my head would go through, it would be of very little use without my shoulders."
    alice "Oh, how I wish I could shut up like a telescope! I think I could, if I only knew how to begin."

    "For, you see, so many out-of-the-way things had happened lately, that Alice had begun to think that very few things indeed were really impossible."

    scene hall at center
    show alice normal
    "There seemed to be no use in waiting by the little door, so she went back to the table, half hoping she might find another key on it, or at any rate a book of rules for shutting people up like telescopes: this time she found a little bottle on it."
    alice "This certainly was not here before"
    "Around the neck of the bottle was a paper label, with the words 'DRINK ME' beautifully printed on it in large letters."

    "It was all very well to say 'Drink me', but the wise little Alice was not going to do that in a hurry."
    alice "No, I’ll look first and see whether it’s marked 'poison' or not."
    
    "she had read several nice little histories about children who had got burnt, and eaten up by wild beasts and other unpleasant things, all because they would not remember the simple rules their friends had taught them: "
    "such as, that a red-hot poker will burn you if you hold it too long; and that if you cut your finger very deeply with a knife, it usually bleeds; and she had never forgotten that, if you drink much from a bottle marked 'poison', it is almost certain to disagree with you, sooner or later."

    "However, this bottle was not marked 'poison,' so Alice ventured to taste it, and finding it very nice, (it had, in fact, a sort of mixed flavour of cherry-tart, custard, pine-apple, roast turkey, toffee, and hot buttered toast,) she very soon finished it off."
    
    show alice happy
    alice "What a curious feeling! I must be shutting up like a telescope."

    "And so it was indeed: she was now only ten inches high, and her face brightened up at the thought that she was now the right size for going through the little door into that lovely garden."

    "First, however, she waited for a few minutes to see if she was going to shrink any further: she felt a little nervous about this."
    show alice surprised
    alice "It might end, you know, in my going out altogether, like a candle. I wonder what I should be like then?"
    "And she tried to fancy what the flame of a candle is like after the candle is blown out, for she could not remember ever having seen such a thing."

    "After a while, finding that nothing more happened, she decided on going into the garden at once; but, alas for poor Alice, when she got to the door, she found she had forgotten the little golden key, and when she went back to the table for it, she found she could not possibly reach it: "
    show alice crying
    "she could see it quite plainly through the glass, and she tried her best to climb up one of the legs of the table, but it was too slippery; and when she had tired herself out with trying, the poor little thing sat down and cried."

    alice "Come, there’s no use in crying like that!"
    show alice pout
    alice "I advise you to leave off this minute!"
    "She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people."
    alice "But it’s no use now, to pretend to be two people! Why, there’s hardly enough of me left to make one respectable person!"

    show alice normal
    "Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in it a very small cake, on which the words 'EAT ME' were beautifully marked in currants."
    alice "Well, I’ll eat it, and if it makes me grow larger, I can reach the key; and if it makes me grow smaller, I can creep under the door: so either way I’ll get into the garden, and I don’t care which happens!"

    "She ate a little bit, and said anxiously to herself: "
    show alice excited
    alice "Which way? Which way?"
    "She was holding her hand on the top of her head to feel which way it was growing, and she was quite surprised to find that she remained the same size: to be sure, this generally happens when one eats cake, but Alice had got so much into the way of expecting nothing but out-of-the-way things to happen, that it seemed quite dull and stupid for life to go on in the common way."
    "So she set to work, and very soon finished off the cake."

label chapter2:
    show alice excited
    alice "Curiouser and curiouser!"
    "(she was so much surprised, that for the moment she quite forgot how to speak good English)"
    alice "Now I’m opening out like the largest telescope that ever was!"
    alice "Good-bye, feet!"
    
