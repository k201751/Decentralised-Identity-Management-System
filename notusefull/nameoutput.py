from subprocess import run, PIPE

command = f"multichain-cli test liststreamitems identity_stream"
result = run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
if result['CNIC'] == '42201-4828550-7':
    print(result['name'])