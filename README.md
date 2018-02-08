[![Build Status](https://travis-ci.org/doaa-altarawy/BSE_website.svg?branch=master)](https://travis-ci.org/doaa-altarawy/BSE_website)

# BSE website
Website of the Bases set exchange Ver 2.0

# Development

```
cd BSE_website
conda create -n bse_env python=3.5 pip
source acivate bse_env
pip install pip install -e git+https://github.com/bennybp/bse-scratch.git#egg=bse-scratch
pip install -e .
python bse_website.py
```

Then access server on the browser at:
```
http://localhost:5000
```

