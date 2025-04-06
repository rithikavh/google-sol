import requests
import json

# Example data for mining a contract (adjust as needed for your application logic)
contract_data = {
    "transactions": [
        {
            "contract_name": "MyCounter",
            "contract_code": "function increment(state) { state.count = (state.count || 0) + 1; return state.count; }",
            "contract_state": {},
            "contract_transactions": []
        }
        # Add more transactions if needed
    ]
}

url = "http://127.0.0.1:5001/mine_contract"
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, json=contract_data)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    print("Contract mining initiated:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error sending request to mine contract: {e}")
except json.JSONDecodeError:
    print("Invalid JSON response from server during contract mining")

# Example of uploading a contract using the /upload_contract endpoint
upload_url = "http://127.0.0.1:5001/upload_contract"
upload_headers = {"Content-Type": "application/json"}
new_contract = {
    "contractName": "SampleLicense",
    "contractCode": "This is the code for a sample license agreement."
}

try:
    upload_response = requests.post(upload_url, headers=upload_headers, json=new_contract)
    upload_response.raise_for_status()
    print("\nContract upload initiated:")
    print(upload_response.json())
except requests.exceptions.RequestException as e:
    print(f"Error sending request to upload contract: {e}")
except json.JSONDecodeError:
    print("Invalid JSON response from server during contract upload")

# Example of fetching the list of contracts
get_contracts_url = "http://127.0.0.1:5001/api/contracts"
try:
    get_response = requests.get(get_contracts_url)
    get_response.raise_for_status()
    print("\nList of uploaded contracts:")
    print(get_response.json())
except requests.exceptions.RequestException as e:
    print(f"Error fetching contracts: {e}")
except json.JSONDecodeError:
    print("Invalid JSON response from server when fetching contracts")