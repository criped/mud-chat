# Django Channels MUD
MUD game based on Django Channels

===============

Django Channels MUD brings a MUD game based on WebSocket connections. In this game, players can register, login, 
chat with others, move to other rooms, as well as some other features. New features can be added by implementing your
own commands as stated below.


## Dependencies


Django MUD Server currently supports Python 3.7+ and Django 3.0+, as it is deployed on ASGI, 
the emerging Python standard for asynchronous web servers and applications.


## Contributing


To learn more about contributing, please read our contribution guide on `CONTRIBUTING.md`.

## Get Started 

In order to run the game server, the easiest way is by using Docker Compose. Simply: 

```
# Start MUD server on docker compose 
docker-compose up
```

Once we have the server up and running, you can enter the game by running a client as follows:

```
docker-compose exec mud-server init-client.sh
```

Alternatively, you can run a test server within your own Python environment as follows:

```
# Install dependencies 
pip install -r requirements/base.txt

# Run Server, make sure you run a Python 3.7+ interpreter 
python src/manage.py runserver 9878

# Run client
python client.py
```

From the MUD client just started, you can see the available commands by typing `help`. 
Create your user account via the `register` command and start chatting with online users across available rooms! 

## Code Walk-through

### Server

The server handles asynchronous websocket connections by implementing a 
[Django Channels Consumer](https://channels.readthedocs.io/en/stable/topics/consumers.html).
It is placed on `src/main/consumers/mud.py`

### Users 
`src/contrib/mud_auth` contains Django models to store and handle user-related features.

### World 
`src/world` contains Django models to store and handle world-related features like rooms and their exits. New rooms
can be added directly from database by inserting a new room and its exits.

### Commands
Commands are implemented in `src/server/commands` in an extensible way. These are the steps if you want to implement 
your own command in your project:

1. Make sure you have installed this app into your django apps. 
2. Create your own command, inheriting from `src.server.commands.base.CommandBase`. You will have to implement 
all the abstract methods like the constructor, `run()` and `is_available()`. The last one is relevant so that the `help` 
command can show info about it.
3. Create your command parser, inheriting from `src.server.commands.parsers.base.CommandParserBase`. Your previously 
created command class will receive it in order to manage the input arguments.
4. Register it on your django settings file by extending the `COMMAND_CONFIG` dict. For example:
```
# your settings.py
MUD_COMMANDS = {
    'path.to.your.commands.module.CommandClass': 'path.to.your.command.parsers.module.CommandParserClass'   
}
```
