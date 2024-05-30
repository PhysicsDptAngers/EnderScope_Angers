// Call the adafruit library
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        7

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 16 

// Define what's a pixels
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 10000 // Time (in milliseconds) to pause between pixels

void setup() {
  Serial.begin(9600); // That's the baudrate value
  pixels.begin(); // Setup all pixels
}

void loop() {
   
      pixels.setBrightness(255); // set the brightness of the pixel (0 to 255)
      // That's three loop for each value (R,G and B) which take 0 or 255, it depends of the value of the factor 
  for(int r=0; r<=1; r++) { 
    for(int g=0; g<=1;g++) { 
      for(int b=0; b<=1;b++) {
       
         for(int i=0; i<NUMPIXELS; i++) { // For each pixel...
                pixels.setPixelColor(i, pixels.Color(255*r, 255*g, 255*b)); // Set the pixel color
              }
              pixels.show(); // Give the order to the pixel
              delay(DELAYVAL); // Create a Delay
            }
          }
        }
      
      pixels.clear(); // Turn off each pixels
    }
