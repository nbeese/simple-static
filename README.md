# simple-static

A simple static site generator based on the [boot.dev](https://boot.dev) guided project.
Uses Python and some bash/shell scripting.
Tested and developed on Linux (CachyOS) using the system-wide Python 3 install, no uv, pipenv or similar tooling was used for this project.
The generated page can be found [here](https://nbeese.github.io/simple-static).

## Documentation

This simple static site generator mostly follows the instructions of the "Build a Static Site Generator" guided project on boot.dev. 
There are a few changes here and there, 
i.e. some functions and structures will vary and some refactoring has been done as well, to keep everything nice and tidy.


Use main.sh to run a small python http server locally for testing purposes in your local setup.
Use test.sh to run the unittests found in test.py.
Use build.sh to build it for deployment on GitHub Pages.

### Last but not least

Yes, you could probably take this thing and just submit it as your own for the [boot.dev](https://boot.dev) guided project.
But where is the fun in that?! 
Also you would need to change a few things along the way to make that work, anyway.
