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

## Use Tekla through Grasshopper
A powerful connection can also be made with the Grasshopper-Tekla link. Tekla structures are easily created with Grasshopper and the GH-components available. When creating a VIKTOR - Tekla app, Grasshopper can also be used. The main issue is that we want a .ifc from the Tekla model; and Grasshopper nodes don't allow for saving / export Tekla files. This can be solved like this:
- Follow [this tutorial](https://docs.viktor.ai/docs/create-apps/software-integrations/rhino-grasshopper/) to set up your VIKTOR app that communicates with GH.
- Have your worker look for an `output.ifc ` in your worker-directory
- Use [these Grasshopper nodes](https://www.food4rhino.com/en/resource/rhinoinside-tekla-structures) to create a Tekla model
- Add the following C# component to your Grasshopper file (feel free to replace some defaults, documentation [here](https://developer.tekla.com/tekla-structures/api/28/26130):
```
if (run){
  Model model = new Model();
  success = Operation.CreateIFC4ExportFromAll(
    ifc_path,
    Operation.IFCExportViewTypeEnum.REFERENCE_VIEW,
    new List<string> { @"..\\default\\General\\Shared\\IFC\\AdditionalPSets\\CIP Construction data.xml" },
    Operation.ExportBasePoint.GLOBAL,
    "__Name__",
    "ByObjectClass",
    new Operation.IFCExportFlags { IsLocationFromOrganizer = true, IsPoursEnabled = true},
    string.Empty);
  }
  success = true;
```
- Add the success output to a context print (so the worker knows the script is finished)


Example:
![image](https://github.com/viktor-rick/tekla-viktor-example/assets/145433945/16edad97-1578-487f-bb50-024d213c962b)
