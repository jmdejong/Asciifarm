
# Style

Development is done in python3 and hy.

This guide mostly covers python, but when a rule makes sence in hy it should be used there as well

## Syntax

- Indentation with 4 spaces
- camelCase for variable and fuctions (even though it's not pythonic)
- PascalCase for class names


### Code

- no global variables
- treat all class member variables as private (use getters and setters when needed) (this rule is under reconsideration)
- Keep it simple
- don't overuse inheritance
- avoid circular references when possible
- don't use `from somemodule import *`


### Structure

- nothing within World should reference something outside it
- nothing in a room should reference something outside of a room (except maybe eventlisteners)
