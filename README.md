[![Build Status](https://travis-ci.org/doaa-altarawy/BSE_website.svg?branch=master)](https://travis-ci.org/doaa-altarawy/BSE_website)
[![codecov](https://codecov.io/gh/doaa-altarawy/BSE_website/branch/master/graph/badge.svg)](https://codecov.io/gh/doaa-altarawy/BSE_website)

# BSE website
Website of the Bases set exchange ver 2.0

# For Development


1. Create conda environment
```
conda create -n bse_env python=3.5 pip
source acivate bse_env
```

2. Clone and install the basis_set_exchange library
```
git clone https://github.com/MolSSI/basis_set_exchange.git
cd basis_set_exchang
pip install -e .
```

3. Clone the website project
```
git clone  https://github.com/doaa-altarawy/BSE_website.git
cd BSE_website
```

4. Install the basis_set_exchange library
```
pip install -e git+https://github.com/MolSSI/basis_set_exchange.git#egg=basis_set_exchange
```

5. Install the website
```
pip install -e .
```

6. Run the server
```
python bse_website.py
```

6. Then access the website at the browser:
```
http://localhost:5000
```

