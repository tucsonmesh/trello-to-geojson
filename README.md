# Convert Trello cards to GeoJSON

This is a Python package that creates Trello Cards reflecting Tucson Mesh installs into a GeoJSON map of the nodes.

The generated GeoJSON is rendered by [tucsonmesh/map-js](https://github.com/tucsonmesh/map-js) and the Trello cards are populated by a [Google Form](https://tinyurl.com/JoinTucsonMesh) which is processed by the [tucsonmesh/form-to-trello](https://github.com/tucsonmesh/form-to-trello) AppScript.

## Assumptions

- Python 3.8+.
- Trello API key and token. See the [Authorization](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/) page in the Trello REST API documentation for information about how to create an API key and token.

## Installation

```
pip install git+https://github.com/tucsonmesh/trello-to-geojson.git
```

## Usage

```
trello-to-geojson > out.geojson
```

## Configuration

Configuration is through environment variables.

### `TRELLO_API_KEY`

API key to access Trello's REST API. See the [Authorization](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/) page in the Trello REST API documentation for information about how to create an API key and token.

### `TRELLO_TOKEN`

Authorization token for Trello's REST API. Typically this is generated through an OAuth flow, but because this is an application designed to run on a server, you should generate the token manually. See the [Authorization](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/) page in the Trello REST API documentation for information about how to create an API key and token.

## Get set up for local development

Clone this repository.

```
git clone https://github.com/tucsonmesh/trello-to-geojson.git
```

Change to the project directory.

```
cd trello-to-geojson
```

Create a virtual environment and activate it.

This will create an isolated environment so this app and its dependencies won't collide with your system Python.

```
python3 -m venv venv
source venv/bin/activate
```

Use pip to install this package in editable mode.

```
pip install -e .
```

Make sure the configuration environment variables are available. You could put these in an .env file, or preferably, [use a password manager](https://blog.gruntwork.io/how-to-securely-store-secrets-in-bitwarden-cli-and-load-them-into-your-zsh-shell-when-needed-f12d4d040df).

If using a .env file and bash, you can add the variables to your environment like this:

```
set -a
source .env
set +a
```

