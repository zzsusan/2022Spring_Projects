# 597 Final Project - Animal Chess
**Team Members**: Suzanne Wang, Keyu Han
**Project type**: Type1, Devise an original variation of existing puzzle type
**Title**: An Animal Chess Game
References:

1. https://www.ymimports.com/pages/how-to-play-jungle
2. https://github.com/weiyinfu/MammalChess  in Chinese
3. https://www.ifanr.com/minapp/1067085 in Chinese

## Game Background
Animal Chess (Dou Shou Qi) is a two-player traditional board game from China. It is also known as Jungle Chess and is a very popular game among children. The game bears resemblance to the western game Strategy, which is probably derived from Dou Shou Qi.
The board is composed of four columns and nine rows of squares. The pictures of the animals indicate the starting arrangement of each animal.
Each player has eight pieces representing different animals, each with a different degree of animal ranking(also known as animal levels). 
There are two versions of Animal Chess basically: 

1. Traditional Version

![image-20220429201053137](https://github.com/zzsusan/2022Spring_Projects/blob/main/image-20220429201053137.png)

2. Simplified Version

This version has a  4*4 puzzle, as shown in the screenshot below.

At the beginning of the game, all the pieces are flipped and we can’t see what animals they are. For each step, the player can choose a piece to flip or move one of his/her existing pieces to eat the opponent’s piece, until a winner appears. The game steps and moving rules will be described in the following paragraphs.

We are going to implement the simplified version.

## Game Rules
Firstly, our game will generate the 4*4 puzzle with the closed animal chess in every position ( However, every chess type and its owner player has generated randomly ). Then, the player will make moves based on the basic game rules.  The game will firstly be visualized in the command line.

### Basic Game rules

1. Each player should take an action in order.
(1) The **action** can be one of the below:
	① **Flip** a new animal piece.
		In this step, the player should select a piece and flip it. What’s more, the opened chess may belong to himself or his opponent because the puzzle was generated randomly in the beginning.
	② **Move** an existing opened animal piece to an empty position or eat the opponent’s animal based on the level of the animal(eat strategy).
2. Decide the winner:  If one player has lost all the chess, and the other has not, the player who first loses all the animal chess will lose. However, if there are 2 players on the board who may let the game get stuck into an endless loop, we will define the largest loop number to stop the game.

### The level of animal(eat strategy)

1. Elephant > Lion > Tiger > Leopard > Dog > Woof > Cat > Rat > Elephant 
(1) The higher level animals can eat his next level animals.
For example, Elephant can eat Lion, Lion can eat Tiger.
(2) The Rat can eat the Elephant as a food circle.

![image-20220429201147880](https://github.com/zzsusan/2022Spring_Projects/blob/main/image-20220429201053137.png)

2. For those same animals, they will disappear together if one player chose to eat his opponent.
(1) A moving example: In the following case, the red Tiger will eat the blue Tiger, and they will disappear together. And finally, the red player will win because he is the last chess owner.

![image-20220429201201567](https://github.com/zzsusan/2022Spring_Projects/blob/main/image-20220429201201567.png)

# Player Type

### Human Vs. Human

In this mode, two player will select the next step in Python Console in order.

```
player_input()
flip_the_piece()
input_move_from()
input_move_to()
move()
```

### Human Vs. Computer

In this mode, computer will use its strategy to play with human player

```
computer_turn
computer_generate_flip
computer_generate_move_info
move
```



### AI strategy

After successfully running out the game, we will optimize an AI game strategy if the time is enough. For example, we will add these rules to improve the computer performance:

1. Biggest First: Our game will choose to move the higher-level animals first.
2. Rat First: Our game will flip the piece near the Elephant and the Rat at last.

### Control the Game

```
play_the_game
determine_end
decide_the_winner
```

# Main Class 

![image-20220429201547123](https://github.com/zzsusan/2022Spring_Projects/blob/main/image-20220429201547123.png)

![image-20220429201558018](https://github.com/zzsusan/2022Spring_Projects/blob/main/image-20220429201558018.png)

# Main Functions & Big(O) Analysis

## Basic Function



## Validation Functions



## Strategy Functions



## Flip



## Move





