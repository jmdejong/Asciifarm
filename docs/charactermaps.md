
# Character maps

The graphics of the game are configurable

By passing the command line argument `-c CHARACTERS` you can choose another configuration.
When this command is given the configuration can be either the name (without extension) of one of the files in the `charmaps` directory in the game, or the filename of another configuration file.
For example:

    asciifarm -c fullwidth

    asciifarm -c /home/troido/asciifarm/charmaps/fullwidth.json

## mapping

The mapping property of a character configuration holds the mapping of sprites to characters.

The sprite key is the spritename that is sent from the server to the client.

The value is either a character (or possibly multiple characters if charwidth > 1) or a list of first the character(s), then the foreground colour and then the background colour. The colours can be ommitted in the list.

The colours are numbers, indicating numbers from the terminal palette.
These colours can differ per terminal, but in most terminals they look like this:

0. black
1. red
2. green
3. yellow
4. blue
5. magenta
6. cyan
7. white

On terminals that have more than 8 colours, the next 8 colours will be the lighter version of the same colour.
On terminals that only have 8 colours, the nex 8 colours will be the same as the first 8 (colour = coulor % 8).

run the script test/colourpairs.py to see how the colour combinations look in your terminal.

## default

This is the character to be drawn when a spritename is encountered that is not in the mapping.

## charwidth

This is the width of the characters in the field. Set this to 2 if you're using fullwidth characters, or 2 characters per sprite.

## healthfull

The character to display in the part of the healthbar where you have health.
Semantics work mostly the same as the values in mapping, but charwidth has no effect on this; it has to be a single halfwidth character.

## healthempty

Similar to healthfull. Shown in the empty part of the healthbar.

