# snapman

# initial checkout
clone --depth=1 ...
cd snapman
python -m venv env
source env/bin/activate
pip install -r requirements.txt

# (re) activating venv
source env/bin/activate

# Dependency Management
New dependencies
(env) pip install

Save dependencies
(env) pip freeze >  requirements.txt
