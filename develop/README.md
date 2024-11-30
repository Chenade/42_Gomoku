```
 _____               _       
|   __|___ _____ ___| |_ _ _ 
|  |  | . |     | . | '_| | |
|_____|___|_|_|_|___|_,_|___|
```

## Game Mode
---
- [X] Play with Another player locally
- [ ] Play with Computer(AI)
- [ ] Play with Another player locally with suggestion (AI)

## View
 - [X] Select Game mode 
 - [X] Place the Stone on mouse click
 - [X] Display captured stone
 - [X] Timer for each move
 - [ ] Timer for computer (down to 0.000s)
 - [X] Button back to menu to retart the game
 - [-] Adjusted for different resolution


## Rule

### Endgame
- WIN
    - [X] Line up to five stones
    - [X] Capture more than 10 stones
    - [ ] If the opponent can break it by capturing a pair
        >Idea 1: Try to place stone around the winning line and see if there is capture

- Draw
    - [X] Not enough space
    - [ ] Not possibility even if there's space

### Check capture
- [ ] After a stone is placed, check all the direction to see if there is a pattern 
    > Pattern: different, different, same
- [ ] Direction: Up, Down, Left, Right
- [ ] Diretion: Four Diagonal
- [ ] Override the Frobidden Double three rule

### Forbidden Move
- Double-three
    - Check Free-three