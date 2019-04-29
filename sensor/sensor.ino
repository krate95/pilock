/*
 * HTTP Client POST Request
 * Copyright (c) 2018, circuits4you.com
 * All rights reserved.
 * https://circuits4you.com 
 * Connects to WiFi HotSpot. */

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

#define echoPin 13
#define trigPin 12
/* Set these to your desired credentials. */
const char *ssid = "Krate"; //ENTER YOUR WIFI SETTINGS
const char *password = "HoliCaracoli";

long duration, distance;
//=======================================================================
//                    Power on setup
//=======================================================================

void setup()
{

    delay(1000);
    Serial.begin(115200);
    WiFi.mode(WIFI_OFF); //Prevents reconnection issue (taking too long to connect)
    delay(1000);
    WiFi.mode(WIFI_STA); //This line hides the viewing of ESP as wifi hotspot

    WiFi.begin(ssid, password); //Connect to your WiFi router
    Serial.println("");

    Serial.print("Connecting");
    // Wait for connection
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    //If connection successful show IP address in serial monitor
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP()); //IP address assigned to your ESP

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
}

//=======================================================================
//                    Main Program Loop
//=======================================================================
void loop()
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    //Calculate the distance (in cm) based on the speed of sound.
    distance = duration / 58.2;
    Serial.println(distance);
    //Delay 50ms before next reading.

    HTTPClient http; //Declare object of class HTTPClient
    if (distance > 5)
    {
        http.begin("http://192.168.43.37:5000/sensor");
        int httpGetCode = http.GET();
        String payload = http.getString();

        Serial.println(httpGetCode); //Print HTTP return code
        Serial.println(payload);     //Print request response payload

        http.end(); //Close connection

        delay(30000); //Post Data at every 5 seconds
    } else {
        delay(3000);
    }
}
//=======================================================================
