## How to contribute to the jnotebook-reader project
First of all, thank you so much for taking your time to contribute! The jnotebook-reader is not very different from any other open
source projects you are aware of. It will be amazing if you could help us by doing any of the following:

- Ask a question tagged with `jnotebook-reader` at [StackOverflow](https://stackoverflow.com/questions/tagged/jnotebook-reader).
- File an issue in [the issue tracker](https://github.com/line/jnotebook-reader/issues) to report bugs or suggest an idea.
- Contribute your work by sending [a pull request](https://github.com/line/jnotebook-reader/pulls).

### Build and runtime requirements

- [Python3](https://www.python.org/download/releases/3.0/)

### Setting up jnotebook-reader for development

You can install jnotebook-reader for a development environment as follows.

\# Install
```
conda create -n py3 python=3
conda activate py3
```

\# Config
./lib/config.py

\# Start up
```
pip install
python app.py
```
By default jnotebook-reader listens on port `9088`.

> Note: jnotebook-reader strives to be a standard Flask application. Make sure to apply standard Flask development patterns.

### Contributor license agreement

When you are sending a pull request and it's a non-trivial change beyond fixing typos, please sign 
[the ICLA (individual contributor license agreement)](https://cla-assistant.io/line/jnotebook-reader). Please
[contact us](mailto:dl_oss_dev@linecorp.com) if you need the CCLA (corporate contributor license agreement).

### Code of conduct

We expect contributors to follow [our code of conduct](https://github.com/line/jnotebook-reader/blob/master/CODE_OF_CONDUCT.md).
