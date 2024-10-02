<p align="center">
    <h1 align="center"><b>Dash Tabler Icons</b></h1>
	<p align="center">
		Beautiful icons for your Dash apps.
    <br />
    <br />
    <br />
    <img width="100" height="100" src="https://avatars.githubusercontent.com/u/60114551?s=200&v=4" alt="Ploomber Logo">
    <br />
    <b>  Made by <a href="https://ploomber.io/?utm_source=dash-tabler-icons&utm_medium=github">Ploomber</a> with ❤️</b>
    <br />
    <br />
    <i>Deploy your Dash application on <a href="https://platform.ploomber.io/register/?utm_source=dash-tabler-icons&utm_medium=github">Ploomber.io</a> for free.</i>
    <br />
  </p>
</p>
<br/>



https://github.com/user-attachments/assets/d69dcfeb-1b59-4d4d-a395-e93ffe293079



Live demo: [dash-tabler-icons.ploomberapp.io](https://dash-tabler-icons.ploomberapp.io/)

## Installation

```sh
pip install dash-tabler-icons
```

## Usage

```python
import dash_tabler_icons as dti
from dash import html

icon = dti.DashTablerIcons(
    icon=dti.IconName.IconStar,
    size=48,
    color="#4B5563",
    stroke=1,
)

# Sample usage in a button
button = html.Button(
    icon,
    id="button-with-icon",
)
```

## Run demo locally

```sh
cd demo
pip install -r requirements.txt
python app.py
```

Open: http://localhost:8050


## Documentation


## Setup

```sh
npm install
pip install -r requirements.txt
pip install -r tests/requirements.txt
```

## Development

```sh
npm run build
python demo.py
```

The icon enum is auto-generated:

```sh
python generate-constants.py
```


## Release

```sh
# generate
npm run build
python setup.py sdist bdist_wheel
ls dist

# test artifact
pip install dash dist/dash_tabler_icons-0.0.1.tar.gz
python demo/app.py

# upload
pip install twine
twine upload dist/*

# clean up
rm -rf dist
```
