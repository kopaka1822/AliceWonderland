background_width = 3360
screen_half = 540
screen_full = 1080
actors = [
    ("lory", 0.0),
    ("duck", 0.1),
    ("dodo", 0.5),
    ("alice", 0.3),
    ("mouse", 0.4),
    ("eaglet", 0.2),
    ("old_crab", 0.6),
    ("young_crab", 0.7),
    ("magpie", 0.8),
    ("canary", 0.9)
]

for actor, x in actors:
    pixelpos = round(540 + x * (background_width - screen_half), 0)
    #display pixelpos without comma
    pixelpos = str(pixelpos).replace(".0", "")
    print(f"show {actor} at breathing({pixelpos}, {actor}_scale)")

# for actor, x in actors:
#     print(f"label setup_muddy_{actor}(pose = \"normal\"):")
#     print(f"    scene muddy at Position(xalign = {x})")
#     # linear interpolate between screen_half and (background_width - screen_half) for pixel center
#     pixel_center = (1-x) * screen_half + x * (background_width - screen_half)

#     for oa, ox in actors:
#         if oa == actor:
#             continue

#         o_pixel_center = (1-ox) * screen_half + ox * (background_width - screen_half)
#         # compute pixel pos
#         pixel_pos = o_pixel_center - pixel_center
#         align_pos = round(0.5 + pixel_pos / screen_half, 2)
#         if align_pos < -0.7 or align_pos > 1.7:
#             continue

#         #print(f"# absolute: {pixel_pos}")
#         addition = ""
#         if oa == "alice":
#             addition = " pose"

#         print(f"    show {oa}{addition} at breathing({align_pos}, {oa}_scale)")
#     print(f"    show {actor} at breathing(0.5, {actor}_scale)")
#     print(f"    return")
#     print()