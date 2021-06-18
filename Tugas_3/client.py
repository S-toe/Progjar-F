import rpyc


if __name__ == "__main__":
  client = rpyc.connect("localhost", 1060)      # connect client

  while True:
    command = input('> ').strip()                 # input 

    if command.startswith('rawquery(\'') and command.endswith('\')'):         # rawquery
      query = command[command.find('\'') + 1:-2]
      print(client.root.rawquery(query))
    elif command.startswith('tabquery(\'') and command.endswith('\')'):       #tabquery
      query = command[command.find('\'') + 1:-2]
      print(client.root.tabquery(query))
    elif command == 'quit':
      client.root.quit()
    else:
      print('Error! please insert a valid command')