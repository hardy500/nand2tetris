// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//@KBD
//M=M

(START)
  @counter
  M=1

  @8192
  M=A

(LOOP)
  @KBD
  D=M
  @BLACK
  D;JNE

  @WHITE
  0;JMP

(WHITE)
  @SCREEN
  M=0

  @counter
  D=M

  @SCREEN
  A=A+D
  M=0

  @counter
  M=M+1

  @8192
  M=M-1
  D=M
  @START
  D;JEQ

  @LOOP
  0;JMP

(BLACK)
  @SCREEN
  M=-1

  @counter
  D=M

  @SCREEN
  A=A+D
  M=-1

  @counter
  M=M+1

  @8192
  M=M-1
  D=M
  @START
  D;JEQ

  @LOOP
  0;JMP







  


  



