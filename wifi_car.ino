#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Wi-Fi credentials
const char* ssid = "sanjayp_fbrgj";
const char* password = "Barsanjay1";

// Motor driver pins
#define ENA D0
#define IN1 D1
#define IN2 D2
#define IN3 D3
#define IN4 D4
#define ENB D5

// Web server on port 80
ESP8266WebServer server(80);

// HTML Web Page
String htmlPage = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>Wi-Fi Controlled Car</title>
  <style>
    body { font-family: Arial; text-align: center; padding: 20px; }
    button { margin: 10px; padding: 15px 30px; font-size: 16px; }
  </style>
</head>
<body>
  <h1>Wi-Fi Controlled Car</h1>
  <button onclick="sendCommand('forward')">⬆ Forward</button><br>
  <button onclick="sendCommand('left')">⬅ Left</button>
  <button onclick="sendCommand('stop')">⏹ Stop</button>
  <button onclick="sendCommand('right')">➡ Right</button><br>
  <button onclick="sendCommand('backward')">⬇ Backward</button>

  <script>
    function sendCommand(command) {
      fetch('/control?command=' + command)
        .then(response => console.log(response.statusText))
        .catch(error => console.error('Error:', error));
    }
  </script>
</body>
</html>
)rawliteral";

void setup() {
  // Initialize Serial Monitor
  Serial.begin(115200);

  // Initialize motor pins
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Stop motors initially
  stopMotors();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.println(WiFi.localIP());

  // Configure web server routes
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html", htmlPage);
  });

  // Web control route
  server.on("/control", HTTP_GET, handleWebControl);

  // REST API route for commands
  server.on("/action", HTTP_POST, handleAction);
  server.begin();
  Serial.println("Web server started");
}

void loop() {
  // Handle incoming client requests
  server.handleClient();
}

void handleWebControl() {
  if (server.hasArg("command")) {
    String command = server.arg("command");
    executeCommand(command);
  }
  server.send(200, "text/plain", "Command received");
}

void handleAction() {
  if (server.hasArg("plain")) {
    String command = server.arg("plain");
    executeCommand(command);
  }
  server.send(200, "text/plain", "Action executed");
}

void executeCommand(String command) {
  if (command == "forward") {
    moveForward();
  } else if (command == "backward") {
    moveBackward();
  } else if (command == "left") {
    turnLeft();
  } else if (command == "right") {
    turnRight();
  } else if (command == "stop") {
    stopMotors();
  }
}

void moveForward() {
  analogWrite(ENA, 1023);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 1023);
  Serial.println("Moving Forward");
  delay(2000); // Stop after 2 seconds
  stopMotors();
}

void moveBackward() {
  analogWrite(ENA, 1023);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, 1023);
  Serial.println("Moving Backward");
  delay(2000); // Stop after 2 seconds
  stopMotors();
}

void turnLeft() {
  analogWrite(ENA, 512);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
  Serial.println("Turning Left");
  delay(2000); // Stop after 2 seconds
  stopMotors();
}

void turnRight() {
  analogWrite(ENA, 512);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 1023);
  Serial.println("Turning Right");
  delay(2000); // Stop after 2 seconds
  stopMotors();
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  Serial.println("Motors Stopped");
}
