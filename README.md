# hflav-python-library

## Documentation

If you want to check the full documentation of this project, go to the docs folder.

The module overview can be checked in this picture:

![Class diagram](docs/Module%20Overview.png)

And the class structure is as it can be seen in this image:

![Class diagram](docs/Class%20Diagram.png)

## Configuring environment variables

All the environment variables available can be seen in the `EnvironmentVariables` enum inside the [config](hflav_zenodo/config.py) file

If you want to use it in your code you should add these lines before anything:

```python
from dotenv import load_dotenv

load_dotenv()
```