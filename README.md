[![Build Status](https://travis-ci.org/MolSSI-BSE/BSE_website.svg?branch=master)](https://travis-ci.org/MolSSI-BSE/BSE_website)
[![codecov](https://codecov.io/gh/MolSSI-BSE/BSE_website/branch/master/graph/badge.svg)](https://codecov.io/gh/MolSSI-BSE/BSE_website)
# BSE website
Website of the Bases set exchange ver 2.0.

An alpha version available for testing at [https://bse-test.herokuapp.com/]

# For Development


1- Create conda environment
```
conda create -n bse_env python=3.5 pip
source acivate bse_env
```

2- Clone and install the basis_set_exchange library if you want to use it as a python library (optional)
```
pip install basis_set_exchang
```

3- Clone the website project
```
git clone  https://github.com/MolSSI-BSE/BSE_website.git
cd BSE_website
```

4- Install the requirements of the project for development (it will install requirements from requirements.txt)
```
pip install -e .[tests]
```

6. Set environment variables in a file, then export it
```bash
export FLASK_CONFIG='production'
export SECRET_KEY='SomeSecretKey'
export APP_ADMIN='email@email.com'
# The logging database uri
export MONGO_URI='mongodb://<user>:<password>@<database_url>:43231/bse_logging'
# or run a script with the exports
source private_env.sh
```


7. Run the server (for development)
```
python bse_website.py
```

8. Then access the website in the browser:
```
http://localhost:5000
```

