import json
from subprocess import run, PIPE
def extract():
    # Assume the 'result' variable contains the provided JSON text
    command = "multichain-cli test liststreamitems identity_stream"
    result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        try:
            # Parse the JSON from the command output
            json_result = json.loads(result.stdout)

            # Extract information for each entry in the 'json_result' variable
            for entry in json_result:
                data_json = entry.get("data", {}).get("json", {})

                cnic = data_json.get("CNIC", "")
                if cnic == "42201-4828550-9":
                    name = data_json.get("name", "")
                    father_name = data_json.get("father's name", "")
                    dob = data_json.get("DOB", "")
                    picture_hash = data_json.get("person's picture hash", "")
                    picture_location = data_json.get("picture location", "")
                    print(f"Name: {name}")
                    print(f"Father's Name: {father_name}")
                    print(f"Date of Birth: {dob}")
                    print(f"CNIC: {cnic}")
                    print(f"Picture Hash: {picture_hash}")
                    print(f"Picture Location: {picture_location}")
                    print("-----")
                    break

            print("Not found!")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Error running command: {result.stderr}")
