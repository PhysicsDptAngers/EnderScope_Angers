#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN       7
#define NUMPIXELS  16

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin();
  pixels.setBrightness(255); // Réglez la luminosité à 255 (maximum)
}

void loop() {
  // Allumer toutes les LEDs en rouge
  for(int i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(255, 255,0)); // Rouge
    pixels.show();

    delay(5000);

    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
    pixels.show();
  }
  // Afficher les changements

  delay(8000); // Attendez 5 minutes (300 000 millisecondes)

  // Éteindre toutes les LEDs
  for(int i = 0; i <1; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0)); // Éteindre
  }
  pixels.show(); // Afficher les changements
}
