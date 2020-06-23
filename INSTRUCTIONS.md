right click on root folder > select open in terminal
python -m venv .venv to setup python virtual environment for this project. TIP: copy from here and right click in terminal to paste-and-execute.
Dialog should come up asking you want this env as interpreter for project: answer yes.
If no to (3) on blue ribbon at bottom of VSCODE, on left click on interpreter, chose the venv one you just created.
Might get some bits and both e.g. 'install pylint' etc. click install for them.
pip install -e . to put project in editable state. This fixes import issues.
TIP: If things break it may be easiect to just delete the whole project folder on your local drive and start over, cloning from repo.-m venx