[![Build Status](https://travis-ci.org/doaa-altarawy/BSE_website.svg?branch=master)](https://travis-ci.org/doaa-altarawy/BSE_website)

# BSE website
Website of the Bases set exchange Ver 2.0

# Clone and run for Development

1. Clone the project including its submodules
```
git clone --recursive https://github.com/doaa-altarawy/BSE_website.git
```

Or do it in two steps
```
git clone https://github.com/doaa-altarawy/BSE_website.git
git submodule init
git submodule update
```

**Note:** The subbmodule was added to the repo using:
`git submodule add https://github.com/MolSSI/basis_set_exchange.git bse
`

**Useful:**
Run recursice commands such as `git submodule foreach 'git diff'`. 
Fetch and update each submodule by
`git submodule update --remote`.

2. Create conda environment
```
conda create -n bse_env python=3.5 pip
source acivate bse_env
```

3. Install the project and run tests
```
cd BSE_website
# pip install pip install -e git+https://github.com/bennybp/bse-scratch.git#egg=bse-scratch
pip install -e .
```


4. Run the server
```
python bse_website.py
```

6. Then access the website at the browser:
```
http://localhost:5000
```

