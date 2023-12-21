# VK_comics_pusher
 
This project was made to pracise my skills in working with API.

## Installation

### Installing dependecies

Python3 should already be installed.
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

### Enviroment

Create `.env` file with this variable:

- `VK_IMPLICIT_FLOW_TOKEN=your access token`. You can get it [there](https://dev.vk.com/ru/api/access-token/implicit-flow-user).
- `VK_GROUP_ID=your group id`. You can get it [there](https://regvk.com/id/)

## Run

### Running scripts with console

To run program you must head to files' direcory and type:

```
python main.py
```

## Notes

You can `delete` line `155` so image won't delete automatically.

Working with `VK` API, program will `raise HTTPError` exception if errors were found in response
