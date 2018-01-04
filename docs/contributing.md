
# Contributing to AsciiFarm

AsciiFarm was always intended to be a town project.

Since the whole codebase might be a bit hard to get into, here useful other ways to help.

For any reporting of things please use github issues, or talk to me (~troido) in tilde.town.
Github issues are not just for bugs, but also suggestions and other types of feedback.

## Testing/Feedback

There's probably a some bugs that I didn't catch.
Maybe there's some bugs that only happen on some systems.
If you play the game it can help in finding these bugs.

What alco can happen is that something is not very intuitive, or hard to understand.
Please also report this since the aim is to make the game as intuitive as possible.

## Suggestions

I don't always know what direction to take asciifarm to.

Suggestions regarding gameplay are very useful.

Unless it's a very simple suggestion it might take a while before I get to work on it though.

## Screenshots

Make screenshots to get people enthousiastic about asciifarm.

Ascii videos would also be appreciated.
[Asciinema](https://asciinema.org/) is a good way to make ascii videos.

## Charmaps and Keybindings

Character maps and keybindings can be customized.

Make your own and share it so others can use them too.

If you have custom charmaps or keybindings, make a pull request to share them

## Level creation

AsciiFarm uses premade rooms.

It would be great if someone create more rooms and fill them with interesting stuff

Also it would be great if the [Tiled mapeditor](http://www.mapeditor.org/) could be used for level creation.
It would be very much appreciated if someone would write at tool to convert the maps as exported by Tiled into maps that can be used by asciifarm.

## Entity creation

For this you'll have to interact with the codebase, but only a small part of it.

Create an entity by adding a factory function to the 'entity' dict in gameobjects.py

Usually you can just copy an excisting entity (eg 'goblin' if you want to make a moster, or 'sword' if you want to make a weapon) and tweak some parameters.

When you have the entity, add a character for it in the charmaps.

## Code Reviews

Give constructive criticism on the source code: report code smells, antipatterns and anything that could be improved

## Documentation

Report everything that you think needs documentation, and if you can, write documentation for it.
Also improve excisting documentation (or report flaws in the current documentation).

## Core development

There's a lot of work to do (see todo list in README), and probably a lot more that I didn't think of.
All help is welcome.

## Other stuff

This page probably doesn't have all ways, so if you can think of another way to help, please do so!
