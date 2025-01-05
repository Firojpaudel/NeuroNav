import json
import paho.mqtt.client as mqtt
from live_advance import LiveAdvance
import threading

# Configuration details
your_app_client_id = 'XtMIEP4zNp0XNhvjHsKWkS5JVPjShy8KlGcMNhgu'  # Replace with your Cortex client ID
your_app_client_secret = 'cv9gq02WQieE9KLSrc5ZcE5MUkqPWkvk75Np7A4jehDgv1tJyRdJOXuc57KiqPYYfSaKBAnWE2AvqDAws3ta5ivZmt4X7WNlGrYW7S81C1UKxAbtI7tMJm2obI8yWsS2'  # Replace with your Cortex client secret
trained_profile_name = 'Firoj'  # Replace with your trained profile name

# MQTT Configuration
mqtt_broker = "test.mosquitto.org"  # Replace with your MQTT broker address
mqtt_port = 1883  # Default MQTT port
mqtt_topic = "esp8266/commands"  # Updated topic for ESP8266

# Global Variables
mqtt_client = None

def load_config():
    """Load control configuration from config.json"""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def save_config(settings):
    """Save control configuration to config.json"""
    with open("config.json", "w") as config_file:
        json.dump(settings, config_file, indent=4)

def on_mqtt_connect(client, userdata, flags, rc):
    """Callback when MQTT client connects to the broker"""
    if rc == 0:
        print("Connected to MQTT broker successfully.")
    else:
        print(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_mqtt_publish(client, userdata, mid):
    """Callback when a message is published"""
    print("MQTT message published.")

def setup_mqtt():
    """Initialize and connect the MQTT client"""
    global mqtt_client
    mqtt_client = mqtt.Client(client_id="Python_Client", protocol=mqtt.MQTTv311)
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_publish = on_mqtt_publish
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.loop_start()

def send_to_mqtt(action):
    """Send a command to the ESP8266 via MQTT"""
    if not mqtt_client:
        print("MQTT client is not connected. Please establish a connection first.")
        return

    try:
        print(f"Publishing message: {action}")  # Print action before publishing
        result = mqtt_client.publish(mqtt_topic, action)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Sent action to MQTT: {action}")
        else:
            print(f"Failed to send message. Error code: {result.rc}")
    except Exception as e:
        print(f"Error sending to MQTT: {e}")

def on_new_com_data_override(*args, **kwargs):
    """Handle new mental command data from LiveAdvance"""
    data = kwargs.get('data')
    if not data:
        return

    action = data.get('action')
    power = data.get('power')

    print(f"Received data: {data}")  # Add this line to see the raw data
    if action and power is not None:
        print(f"Received action: {action}, Power: {power}")
        if power >= 0.1:  # Send command to ESP8266 only for significant actions
            send_to_mqtt(action)

def start_live_advance():
    """Start the LiveAdvance process"""
    print("Starting Neuro-Nav Controller...")
    live_advance_instance.start(trained_profile_name)

def update_config(action, index):
    """Update the configuration mapping"""
    config = load_config()
    config[action] = index
    save_config(config)
    print(f"Updated {action} mapping to index {index}.")

def send_custom_message():
    """Send a custom message to the ESP8266 via MQTT"""
    message = input("Enter the message to send: ").strip()
    if message:
        send_to_mqtt(message)
    else:
        print("Message cannot be empty.")

def display_menu():
    """Display the menu options"""
    print("\nOptions:")
    print("  1. Connect to MQTT broker")
    print("  2. Start mapping")
    print("  3. Update configuration")
    print("  4. Send custom message")
    print("  5. Exit")

def main():
    """Main program function"""
    global live_advance_instance
    live_advance_instance = LiveAdvance(your_app_client_id, your_app_client_secret)
    live_advance_instance.on_new_com_data = on_new_com_data_override

    config = load_config()
    print("Current Configuration:")
    for action, index in config.items():
        print(f"  {action.capitalize()}: {index}")

    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == '1':
            setup_mqtt()

        elif choice == '2':
            threading.Thread(target=start_live_advance).start()
            print("Mapping started. Use Ctrl+C to stop.")

        elif choice == '3':
            print("Update Configuration:")
            print("  Options: push, pull, left, right")
            action = input("Enter action to update: ").strip().lower()
            if action in config:
                try:
                    index = int(input(f"Enter new index for {action}: ").strip())
                    update_config(action, index)
                except ValueError:
                    print("Invalid index. Please enter a number.")
            else:
                print("Invalid action. Choose from: push, pull, left, right.")

        elif choice == '4':
            send_custom_message()

        elif choice == '5':
            print("Exiting Neuro-Nav Controller.")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
