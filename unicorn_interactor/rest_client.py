import requests

def send_json_payload(payload):
    """
    Sends a JSON payload to the specified URL and returns the response.

    Args:
    payload (dict): The JSON payload to send.

    Returns:
    dict: The JSON response from the server.
    """
    url = "https://rest.unicorn.meme/cosmos/tx/v1beta1/txs"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send POST request with JSON payload
        response = requests.post(url, json=payload, headers=headers)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Return the JSON response
        return response.json()

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
