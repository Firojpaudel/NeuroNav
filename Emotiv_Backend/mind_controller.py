import json
import requests
from live_advance import LiveAdvance
import threading

# Configuration details
your_app_client_id = 'XtMIEP4zNp0XNhvjHsKWkS5JVPjShy8KlGcMNhgu'  # Replace with your Cortex client ID
your_app_client_secret = 'cv9gq02WQieE9KLSrc5ZcE5MUkqPWkvk75Np7A4jehDgv1tJyRdJOXuc57KiqPYYfSaKBAnWE2AvqDAws3ta5ivZmt4X7WNlGrYW7S81C1UKxAbtI7tMJm2obI8yWsS2'  # Replace with your Cortex client secret
trained_profile_name = 'Firoj'  # Replace with your trained profile name

# ESP8266 Configuration
esp8266_base_url = "http://192.168.1.92"  # Replace with the base URL of your ESP8266

def load_config():
    """Load control configuration from config.json"""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def save_config(settings):
    """Save control configuration to config.json"""
    with open("config.json", "w") as config_file:
        json.dump(settings, config_file, indent=4)

def send_to_esp8266(command):
    """Send a command to the ESP8266 via HTTP GET"""
    commands = {
        'push':'forward',
        'pull':'backward'
    }
    try:
        url = f"{esp8266_base_url}/control?command={commands[command]}"
        print(f"Sending GET request to: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command '{command}' sent successfully!")
        else:
            print(f"Failed to send command. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending command to ESP8266: {e}")

def on_new_com_data_override(*args, **kwargs):
    """Handle new mental command data from LiveAdvance"""
    data = kwargs.get('data')
    if not data:
        return

    action = data.get('action')
    power = data.get('power')

    print(f"Received data: {data}")
    if action and power is not None:
        print(f"Received action: {action}, Power: {power}")
        if power >= 0.1:  # Send command to ESP8266 only for significant actions
            send_to_esp8266(action)

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
    """Send a custom command to the ESP8266"""
    message = input("Enter the command to send: ").strip()
    if message:
        send_to_esp8266(message)
    else:
        print("Command cannot be empty.")

def display_menu():
    """Display the menu options"""
    print("\nOptions:")
    print("  1. Start mapping")
    print("  2. Update configuration")
    print("  3. Send custom command")
    print("  4. Exit")

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
            threading.Thread(target=start_live_advance).start()
            print("Mapping started. Use Ctrl+C to stop.")

        elif choice == '2':
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

        elif choice == '3':
            send_custom_message()

        elif choice == '4':
            print("Exiting Neuro-Nav Controller.")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
