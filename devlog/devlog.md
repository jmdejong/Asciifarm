# Rooms/Asciifarm Developer log

~rbiv recently asked me for a developer log for this project

Currently I don't feel like setting up a whole blog, and they are short messages anyways, so for now I'll just write in one file

## 22/10

Today I managed to make what I think is a minimal playable game:

Players can kill goblins.
Goblins drop seeds as loot.
Seeds can be planted and farmed for food.
Food will heal the player when eaten.
The player will need a lot of health to kill the final boss: the troll.
The troll drops stones which can be used to build walls in the world.

I think I should make the buildable walls destructible, but that comes later.

I'm afraid when I make them destructible I have to give them an alignment, and that causes the AI to possibly target them, so the game will slow down when there are some AI enemies and a lot of built walls in the room.
I should probably make Target a separate component instead of part of Alignment.

Another thing: I managed to get configurable keybindings working.
Players can specify another json file to load keybindings from using the command line argument -k or --keybindings.

Talking about keybindings, I'm not sure yet what the best default keybindings would be.
I read that 'g' is default for picking up things, but I prefer 'e'.

Another thing that is now configurable is the sprite mapping.
With the -c or --characters command line argument, players can choose a file describing different characters for some sprite name.
If you don't like some choice I made you can change it now.
Other untested uses would include using fullwidth characters for a better width-height ratio, or if you speak chinese (~m455) you can use the chinese character for that object.

Aaand, inet sockets are supported to with the -s flag.
You can select 'unix', 'abstract' and 'inet'.
'abstract' sockets are actually just unix sockets but with a null byte in front of them, placing them in an abstract namspace.

## 23/10

I managed to make walls destructible, by making target a different component.

I've been browsing reddit.com/r/roguelikedev.
I don't think the core of rooms is really a roguelike: no permadeath, most of the rooms are predesigned instead of randomly generated, steps are in real time instead of turn based.
I still feel that I like the community of roguelikes more (at least compared to /r/gamedev).
Roguelikes are more games made for programmers and computer enthousiasts.
Roguelikes are also much more commonly made from scratch, using libraries instead of frameworks or engines.

One of the reasons to include procedurally generated dungeons in the game is to be more roguelike, and appeal more to the roguelike community.
It's probably not a very good reason.
There are other reasons too:
It brings an unlimited source of special items in the game (though this could be done with regular dungeons too...).
Also, since the game currently doesn't see as much community involvement as I had hoped (at least not with coding and testing), a nice way to involve others is to let them write their own dungeon generator.

Alright, maybe these are not very short messages

## 24/5

Yesterday ~m455 gave me permission to name my project AsciiFarm.
This is a much better name that Rooms, but originally that idea was his, and he already started some work under that name.

## 27/5

Last days I've been making a lot of changes to the client, since the server is pretty much a minimal working game now.
The client now uses different curses pads to show the game information.
When the room is larger than the fiels area of the display, the display will only show part of it centered on the player.

Colours work too now.
It was a bit of a hassle to make them look nice on 16 colour palettes and also work on 8 colour palettes (and still work without), but I managed to.
Basically if an 8 colour palette is used, all coloura are done % 8.

With the addition of colours I also made a healthbar.
This quickly made me realize that health lowered way to fast, so I doubled the attack delay for all creatures.

There is only one main change I want to make to the client now: add a message log.
Ok, maybe 2: select items in the inventory for using.



