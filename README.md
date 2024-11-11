# walkingpad-fitbit
Send walkingpad data to fitbit.

_This is a personal hobby app and is not associated with WalkingPad in any way._

This program:
* Connects to your WalkingPad treadmill over bluetooth.
* Receives walking data from the treadmill, every second (the interval is configurable).
* Prints the walking data to the console in a variety of formats (plain text, rich text, json).
* Sends a treadmill workout to FitBit when the walk stops.
* Provides a REST server with routes to control the treadmill.


## Configuration
This program requires a Fitbit developer application.
Create an application in the [Fitbit developer dashboard](https://dev.fitbit.com/apps/).

Note the client id and client secret.

Store them in one of two ways:

### Option 1: `.env` file
Copy the `.env.template` file to `.env`.
Enter your Fitbit application's client id and client secret.

### Option 2: Environment variables
Set the following environment variables:
* `FITBIT_OAUTH_CLIENT_ID`
* `FITBIT_OAUTH_CLIENT_SECRET`

## Usage

### Get your device's name

Use the `ph4_walkingpad` tool to find the name of your treadmill:
`python -m ph4_walkingpad.main --scan`

This outputs a line similar to the following:
```
Device: [ 0], XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX, KS-ST-A1P, ['0000fe00-0000-1000-8000-00805f9b34fb']
```

In this case, the device name is **KS-ST-A1P**.

Use this name when using the `walkingpadfitbit` command.

### Command options
```
% python -m walkingpadfitbit.main --help
usage: main.py [-h] [-d MONITOR_DURATION_S] [-p POLL_INTERVAL_S] [-m {plaintext,richtext,json}] device_name

positional arguments:
  device_name           Name of the walkingpad device (ex: KS-ST-A1P).

options:
  -h, --help            show this help message and exit
  -d MONITOR_DURATION_S, --monitor-duration MONITOR_DURATION_S
                        Monitoring duration in seconds. By default the program monitors forever.
  -p POLL_INTERVAL_S, --poll-interval POLL_INTERVAL_S
                        Poll interval in seconds (default 1.0).
  -m {plaintext,richtext,json}, --display-mode {plaintext,richtext,json}
                        Display mode
  --server-host SERVER_HOST
                        Host on which the http server will run.
  --server-port SERVER_PORT
                        Port on which the http server will run.
```

### Example command
This commmand will collect data every second from the treadmill:

`python -m walkingpadfitbit.main KS-ST-A1P`

### Treadmill controller server
The program starts an http server, by default on 127.0.0.1:11198. The host and port are configurable as described in the comand options above.

The server exposes two routes:

* `POST /treadmill/start`: to start the treadmill.
  Curl example:
  ```
  curl -X POST http://127.0.0.1:11198/treadmill/start
  ```
* `POST /treadmill/stop`: to stop the treadmill.
  Curl example:
  ```
  curl -X POST http://127.0.0.1:11198/treadmill/stop
  ```
* `POST /treadmill/toggle-start-stop`: to start the treadmill if it's running, otherwise stop it.
  Curl example:
  ```
  curl -X POST http://127.0.0.1:11198/treadmill/toggle-start-stop
  ```

A Swagger UI is available at the root route: http://127.0.0.1:11198/

Static api documentation is available in the [GitHub pages](https://caarmen.github.io/walkingpad-fitbit/restapi.html) for this project.

## Authentication
The first time you run the app, you will be prompted to log in to Fitbit, to grant authorization
(to the Fitbit app you created). After granting authorization, Fitbit will attempt to redirect to the
application. Since this is a command-line tool, there is no server to which Fitbit can redirect. It redirects
to a Github page which exists only to avoid an error due to the lack of a server. Copy the url of the page,
and paste it in the command line tool to complete the login.

How does it work? The application uses the OAuth flow: [Code Grant Flow with PKCE](https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/#Authorization-Code-Grant-Flow-with-PKCE) for a "Server" application type. In particular, under the hood, it uses a code verifier, which is not communicated in the browser, and is required for the authentication to complete.