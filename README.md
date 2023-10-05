# Viktor app for Tekla Integration

## Requirements
- Tekla Structures (with an active model on the worker)
- VIKTOR Generic Worker
- PyTekla

## Set-up
Install the VIKTOR app. Configure a Generic Worker (see our docs) and place the run_tekla.py in the Workers directory.

Before running the worker; open up the Python Environment your worker also uses and run the following commands:

`import pytekla`

`pytekla.config.set_tekla_path("C:/Program Files/Tekla Structures/2023.0/bin")`

Make sure the Tekla Path is set to the bin folder of your Tekla Structures.


Now you can run the VIKTOR worker and connect it to your workspace. You can now access Tekla from the VIKTOR app.

## Run Tekla from VIKTOR app
You could use the PyTekla wrapper to open, save and close Tekla models as well. First open Tekla in a .bat script; then, with Python, use the following commands, by utilizing the PyTekla wrapper:

Open a model:

`model_handler = wrap('Model.ModelHandler')`

`model_handler.CreateNewSingleUserModel("model_name", "path_to_model", "template_name")`

Save a model

`model_handler.Save("comment", "user_name")`

Close a model

`model_handler.Close()`
