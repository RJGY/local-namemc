# local-namemc

A simple command-line tool in python to manage a local list of Minecraft players, tracking their usernames, UUIDs, and reasons for being on the list. The tool interacts with Mojang's APIs to fetch and update player information, and stores the data in a local file.

## Features

- Add a player to the list by username (with optional reason)
- Remove a player from the list
- Change or add a reason for a player (by username or UUID)
- Bulk add players from a file
- List all players, updating their names if changed
- Persistent storage in `player_list.txt`
- Fetches UUIDs and current names from Mojang APIs

## Usage

Run the script with one of the following commands:

- `add <username> <reason>`  
  Adds a user to the list. Reason is optional.

- `remove <username>`  
  Removes a user from the list.

- `reason <username/uuid> <reason>`  
  Adds or changes a reason for a user on the list (user must already be on the list). Either UUID or username can be passed.

- `bulk <file_path>`  
  Adds multiple users to the list from a file. See `example.txt` for the format.

- `list`  
  Lists all users on the list and updates their names if they have changed.

If run with no arguments, the script prints a help message.

## Example

```sh
python namemc.py add Notch "OG Minecraft creator"
python namemc.py remove Notch
python namemc.py reason Notch "Legend"
python namemc.py bulk add.txt
python namemc.py list
```

## File Format

- `player_list.txt`  
  Stores player data in the format:  
  `<uuid>|<name1,name2,...>|<reason>`

- `add.txt` (for bulk add)  
  Each line:  
  `<name1,name2,...>|<reason>`

## TODO

- Try to use a decorator for the save file command
- Add a db later if ur bothered

---

Feel free to contribute or suggest improvements!