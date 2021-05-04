
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT  64

// NeoPixel brightness, 0 (min) to 255 (max)
#define BRIGHTNESS 15 // Set BRIGHTNESS to about 1/5 (max = 255)



int buzz = 7;
int light1 = 3;
int light2 = 2;
int light3 = 4;

int button1 = 5;
int button3 = 0;
int button2 = 1;


// 8X8 RGB MATRIX PIN 
#define LED_PIN  6


String val;

#include "notes.h"
#include "discord.h"

int check;




// Declare our NeoPixel strip object
Adafruit_NeoPixel pixels(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  pinMode(OUTPUT, buzz);
//  pinMode(OUTPUT, light1);
//  pinMode(INPUT, button1);

  pinMode(buzz, OUTPUT);
  pinMode(light1, OUTPUT);
  pinMode(light2, OUTPUT);
  pinMode(light3, OUTPUT);
  pinMode(button1, OUTPUT);

  // Light 1 
  pixels.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.setBrightness(BRIGHTNESS);

  //Connect to wifi
  connect_to_wifi();

  //Send msg
  discord_send("Connection Successful");



}


void loop() {
   pixels.clear();
  //Default Dog Animations 
  pinMode(buzz, LOW);
  noTone(buzz);
  showDog();
  delay(150);
  showDog2();
  delay(110);
  showDog();
  delay(150);
  showDog2();
  delay(160);
  showDog();

  
  //SERIAL READER FOR ROBOT
  while(Serial.available()>0){}
  val = Serial.readString();
  Serial.println(val);

  //Check for Light Inputs
  if (val == "light1On") {
   digitalWrite(light1,HIGH);
  }
   if (val == "light2On") {
   digitalWrite(light2,HIGH);
  }
   if (val == "light3On") {
   digitalWrite(light3,HIGH);
  }


//---------------------------------------------------------------------
//PLAY FUNCTIONS
  //Serial Checkers for commands
  if (val == "play") {

    //play rgb matrix animations
    showPlay();
    delay(150);
    showPlay2();
    delay(150);
    showPlay();
    delay(150);
    showPlay2();
    delay(150);
    showPlay();
    delay(150);
    showPlay2();
    delay(150);


    // Turn off LED  
    digitalWrite(light2,LOW);

    
    //Play Tone
    playTone();
  }


  
// Button Press 
  if (digitalRead(button2) == HIGH) {
    discord_send("botplay");

    //play rgb matrix animations
    showPlay();
    delay(150);
    showPlay2();
    delay(150);
    showPlay();
    delay(150);
    showPlay2();
    delay(150);
    showPlay();
    delay(150);
    showPlay2();
    delay(150);


    // Turn off LED  
    digitalWrite(light2,LOW);

    
    //Play Tone
    playTone();
    
  }

//---------------------------------------------------------------------
  
//---------------------------------------------------------------------
//PET FUNCTIONS
//    Physical Button press

  if (digitalRead(button1) == HIGH) {

    discord_send("botpet");
    
    pixels.clear();
    //play rgb matrix animations
    showPetting();
    delay(200);
    showPetting2();
    delay(350);
    showPetting();
    delay(250);



    // Turn off LED  
    digitalWrite(light1,LOW);
    //Play Tone
    acceptTone();
  } 


//   discord message 
  if (val == "pet" ) {
    pixels.clear();
    //play rgb matrix animations
    showPetting();
    delay(200);
    showPetting2();
    delay(350);
    showPetting();
    delay(250);



    // Turn off LED  
    digitalWrite(light1,LOW);
    //Play Tone
    acceptTone();
  }
  
//---------------------------------------------------------------------




  

   if (val == "feed") {
    pixels.clear();
    //play rgb matrix animations
    showTreat();
    delay(450);
    showTreat2();

    // Turn off LED  
    digitalWrite(light3 ,LOW);

    //Play tone
    acceptTone();
  }


    if (digitalRead(button3) == HIGH) {

    discord_send("botfeed");
    pixels.clear();
    //play rgb matrix animations
    showTreat();
    delay(450);
    showTreat2();

    // Turn off LED  
    digitalWrite(light3 ,LOW);

    //Play tone
    acceptTone();
  }


// END OF LOOP 
}




//----------------------------------------------------------------------





void showPlay() {
  pixels.clear();
  //Green pixels, NOTE : STARTS ON 1 
    //number of pixels for green
  int sizePurple = 24;
  int purplePixel[sizePurple] = {11,12,13,14,18,20,21,23,26,28,29,31,34,36,37,39,42,44,45,47,51,52,53,54};

    //check for green pixel then set
    for (int i = sizePurple; i >= 0;i--) {
      //Set Pixel Color
      pixels.setPixelColor(purplePixel[i]-1, pixels.Color(255, 0, 255));
    }

  
  int sizeWhite = 8;
  int whitePixel[sizeWhite] = {19,22,27,30,35,38,43,46};

    //check for green pixel then set
    for (int j = sizeWhite; j >= 0;j--) {
      //Set Pixel Color
      Serial.println(whitePixel[j]-1);
      pixels.setPixelColor(whitePixel[j]-1, pixels.Color(255, 255, 255));
    }
  pixels.show();
}

void showPlay2() {
  pixels.clear();
  //Green pixels, NOTE : STARTS ON 1 
    //number of pixels for green
  int sizePurple = 24;
  int purplePixel[sizePurple] = {19,20,21,22,26,28,29,31,34,36,37,39,42,44,45,47,50,52,53,55,59,60,61,62};

    //check for green pixel then set
    for (int i = sizePurple; i >= 0;i--) {
      //Set Pixel Color
      pixels.setPixelColor(purplePixel[i]-1, pixels.Color(255, 0, 255));
    }


  int sizeWhite = 8;
  int whitePixel[sizeWhite] = {27,30,35,38,43,46,51,54};

    //check for green pixel then set
    for (int j = sizeWhite; j >= 0;j--) {
      //Set Pixel Color
      Serial.println(whitePixel[j]-1);
      pixels.setPixelColor(whitePixel[j]-1, pixels.Color(255, 255, 255));
    }

  //update to show pixels 
  pixels.show();
}







void showTreat() {
  pixels.clear();
  //Brown pixels, NOTE : STARTS ON 1 
    //number of pixels for brown
  int sizeGreen = 24;
  int greenPixel[sizeGreen] = {2,3,14,15,16,17,18,19,20,28,29,30,36,37,38,41,42,43,44,54,55,56,58,59};

  for(int i=0; i<LED_COUNT; i++) {
      pixels.setPixelColor(i, pixels.Color(0, 0, 0));
  
    //check for green pixel then set
    for (int j = 0; j < sizeGreen;j++ ) {
      //check for brown pixels
      if (i == greenPixel[j]-1) {
        //if pixel is reader is equal to one of the brown pixels in array, set pixel to brown 
        pixels.setPixelColor(i, pixels.Color(49, 255, 38));
      }
    }
  }
  
  //COLOR DOG BROWN
  pixels.show(); //Update After Setting pins to light color 
}


void showTreat2() {
  //Green pixels, NOTE : STARTS ON 1 
    //number of pixels for green
  int sizeGreen = 24;
  int greenPixel[sizeGreen] = {2,3,14,15,16,17,18,19,20,28,29,30,36,37,38,41,42,43,44,54,55,56,58,59};

    //check for green pixel then set
    for (int j = sizeGreen; j >= 0;j--) {
      //Set Pixel Color
      pixels.setPixelColor(greenPixel[j]-1, pixels.Color(0, 0, 0));
      delay(100);
      //Instantaneous update to board
      pixels.show();
    }
  
  pixels.clear();
  pixels.show();
  
}





void showPetting() {
  pixels.clear();
  //Green pixels, NOTE : STARTS ON 1 
    //number of pixels for green
  int sizeYellow = 22;
  int yellowPixel[sizeYellow] = {10,14,19,23,26,27,30,31,41,42,47,48,50,51,52,53,54,55,59,60,61,62};

    //check for green pixel then set
    for (int i = sizeYellow; i >= 0;i--) {
      //Set Pixel Color
      pixels.setPixelColor(yellowPixel[i]-1, pixels.Color(255, 251, 0));
      //Instantaneous update to board
      delay(50);
      pixels.show();
    }

  pixels.show();
  
}


//No Eyes
void showPetting2() {
  pixels.clear();
  pixels.show();
  //Green pixels, NOTE : STARTS ON 1 
    //number of pixels for green
  int sizeYellow = 14;
  int yellowPixel[sizeYellow] = {41,42,47,48,50,51,52,53,54,55,59,60,61,62};

    //check for green pixel then set
    for (int i = sizeYellow; i >= 0;i--) {
      //Set Pixel Color
      pixels.setPixelColor(yellowPixel[i]-1, pixels.Color(255, 251, 0));
    }
  pixels.show();
}




void showDog2() {
  pixels.clear();
  //Brown pixels, NOTE : STARTS ON 1 
    //number of pixels for brown
  int sizeBrown = 26;
  int brownPixel[sizeBrown] = {10,13,14,20,21,22,23,26,28,30,35,36,37,38,39,42,43,44,53,54,55,56,57,58,59,60,61,62,63,64};

  int sizeBlue = 2; 
  int bluePixel[sizeBlue] = {27,29};
  //set background blue
  for(int i=0; i<LED_COUNT; i++) {

      pixels.setPixelColor(i, pixels.Color(0, 0, 0));
//    pixels.show();
//    delay(DELAYVAL);

    //set One Pixel to pink (dogs nose)
     pixels.setPixelColor(31-1, pixels.Color(237, 113, 100));


    //check then set blue pixels 
    for (int j = 0; j < sizeBlue; j++)
      if (i == bluePixel[j]-1){
        pixels.setPixelColor(i, pixels.Color(3, 82, 252));
      }
    
  
    //check for brown pixels
    for (int j = 0; j < sizeBrown;j++ ) {
      //check for brown pixels
      if (i == brownPixel[j]-1) {
        //if pixel is reader is equal to one of the brown pixels in array, set pixel to brown 
        pixels.setPixelColor(i, pixels.Color(94, 60, 16));
      }
    }
  }
  //COLOR DOG BROWN
  pixels.show(); //Update After Setting pins to light color 
}


void showDog() {
  pixels.clear();
  //Brown pixels, NOTE : STARTS ON 1 
    //number of pixels for brown
  int sizeBrown = 22;
  int brownPixel[sizeBrown] = {19,20,23,26,27,28,29,35,37,39,42,43,44,45,46,53,54,55,57,58,59,60};

  int sizeBlue = 2; 
  int bluePixel[sizeBlue] = {36,38};
  //set background blue
  for(int i=0; i<LED_COUNT; i++) {

      pixels.setPixelColor(i, pixels.Color(0, 0, 0));
//    pixels.show();
//    delay(DELAYVAL);

    //set One Pixel to pink (dogs nose)
     pixels.setPixelColor(33, pixels.Color(237, 113, 100));


    //check then set blue pixels 
    for (int j = 0; j < sizeBlue; j++)
      if (i == bluePixel[j]-1){
        pixels.setPixelColor(i, pixels.Color(3, 82, 252));
      }
    
  
    //check for brown pixels
    for (int j = 0; j < sizeBrown;j++ ) {
      //check for brown pixels
      if (i == brownPixel[j]-1) {
        //if pixel is reader is equal to one of the brown pixels in array, set pixel to brown 
        pixels.setPixelColor(i, pixels.Color(94, 60, 16));
      }
    }
  }
  //COLOR DOG BROWN
  pixels.show(); //Update After Setting pins to light color 
}







 //MUSIC TONES

void acceptTone() {
  pinMode(buzz, HIGH);
  tone(buzz,NOTE_E4);
  delay(200);
  tone(buzz,NOTE_F4);
  delay(200);
  tone(buzz,NOTE_G4);
  delay(500);
  tone(buzz,NOTE_C5);
  delay(500);
  noTone(buzz);
}

void denyTone() {
  pinMode(buzz, HIGH);
  tone(buzz,NOTE_F4);
  delay(200);
  tone(buzz,NOTE_G4);
  delay(200);
  tone(buzz,NOTE_G3);
  delay(500);
  tone(buzz,NOTE_F3);
  delay(500);
  noTone(buzz);
}

void playTone() {
  pinMode(buzz, HIGH);
  tone(buzz,NOTE_C5);
  delay(200);
  noTone(buzz);
  delay(50);
  tone(buzz,NOTE_C5);
  delay(200);
  tone(buzz,NOTE_E5);
  delay(200);
  tone(buzz,NOTE_F5);
  delay(300);
  noTone(buzz);
}

void almostdeathTone() {
  pinMode(buzz, HIGH);
  tone(buzz,NOTE_D4);
  delay(400);
  tone(buzz,NOTE_B3);
  delay(200);
  tone(buzz,NOTE_G3);
  delay(200);
  tone(buzz,NOTE_F3);
  delay(200);
  noTone(buzz);
}
