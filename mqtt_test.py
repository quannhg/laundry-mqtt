import paho.mqtt.client as mqtt
import json
import threading
import uuid

# Define MQTT broker settings
BROKER = 'localhost'  # Assuming you are running the broker locally
PORT = 1883
USERNAME = 'python_test'  # Replace with your actual username
PASSWORD = 'secretpassword'  # Replace with your actual password
MQTT_TO_SERVER_TOPIC = "laundry/system/server"  # Single topic for all message types
MQTT_TO_HARDWARE_TOPIC = "laundry/system/hardware"  # Single topic for all message types

machine_id = "99f41bf1-f47b-4ab3-9c23-c1764be25570"

# Define messages to be published on connection
messages = {
    0: {
        "type": 0,  # Assuming 0 is the type for adding a machine
        "payload": {
            "id": machine_id
        }
    },
    1: {
        "type": 1,  # Assuming 0 is the type for remove a machine
        "payload": {
            "id": machine_id
        }
    },
    2: {
        "type": 2,  # Assuming 0 is the type for update washing status a machine
        "payload": {
            "id": machine_id,
            "status": "WASHING"
        }
    },

}

# Event to ensure the on_connect function completes before publishing
connect_event = threading.Event()

# Define the callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", str(rc))
    # Subscribe to the topic
    client.subscribe(MQTT_TO_HARDWARE_TOPIC)
    # Signal that the connection is established and the subscription is done
    connect_event.set()

# Define the callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    # Decode the message payload and parse it as JSON
    message = json.loads(msg.payload.decode())
    print(f"Received message from topic {msg.topic}: {message}")

def main():
    # Create a new MQTT client instance
    client = mqtt.Client()

    # Attach the defined callback functions to the client
    client.on_connect = on_connect
    client.on_message = on_message

    # Set username and password
    client.username_pw_set(USERNAME, PASSWORD)

    # Connect to the broker
    client.connect(BROKER, PORT, 60)

    # Start the network loop
    client.loop_start()

    # Wait until connection and subscription are complete
    connect_event.wait()

    try:
        while True:
                # Read message key from keyboard
                msg_key = int(input(f"Enter message key to send {list(messages.keys())}: "))
                if msg_key in messages:
                    message_payload = json.dumps(messages[msg_key])
                    print(f"Publishing message to topic {MQTT_TO_SERVER_TOPIC}: {message_payload}")
                    client.publish(MQTT_TO_SERVER_TOPIC, message_payload)
                else:
                    print(f"Invalid message key. Please enter {list(messages.keys())}.")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()