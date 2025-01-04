#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "The NEXT";
const char* password = "NMSKFPBP";

// MQTT Broker settings
const char* mqtt_broker = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_topic = "esp32/commands";

WiFiClient espClient;
PubSubClient client(espClient);

// Callback function to handle incoming messages
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void setup() {
  // Start serial communication at 115200 baud rate
  Serial.begin(115200);  

  // Connect to WiFi
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis();
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    if (millis() - startAttemptTime >= 30000) {  // Timeout after 30 seconds
      Serial.println("Failed to connect to WiFi after 30 seconds.");
      return;
    }
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);  // Setting the callback function

  Serial.print("Connecting to MQTT broker...");
  while (!client.connected()) {
    if (client.connect("ESP32_Client")) {
      Serial.println("connected");
    } else {
      Serial.print(".");
      delay(1000);
    }
  }

  // Subscribe to topic
  if (client.subscribe(mqtt_topic)) {
    Serial.println("Successfully subscribed to topic.");
  } else {
    Serial.println("Failed to subscribe to topic.");
  }
}

void loop() {
  client.loop();  // Keep the MQTT connection alive
}
