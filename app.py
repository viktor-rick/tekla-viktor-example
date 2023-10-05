import json
from pathlib import Path

from viktor import ViktorController, File
from viktor.external.generic import GenericAnalysis
from viktor.parametrization import ViktorParametrization, NumberField, LineBreak, Text, AutocompleteField
from viktor.views import IFCResult, IFCView

profiles = ["IPE80", "IPE100", "IPE200", "IPE300", "HEA100", "HEA140", "HEA200", "L20/4", "L50/5", "UNP30", "UNP65"]
footings = ["500*500", "750*750", "1000*1000", "1500*1500"]
materials = ["S235JR", "S275JR", "S355JR"]
foot_mats = ["C20/25", "C30/37", "C45/55"]


class Parametrization(ViktorParametrization):
    # Create the parametrization

    # Sizes of the steel structure
    text_size = Text("Enter the dimensions of the structure")
    length = NumberField("Length of the structure", default=8000)
    width = NumberField("Width of the structure", default=3000)
    br = LineBreak()

    # Height of the roofs
    height_ridge = NumberField("Height of the Ridge", default=4000)
    height_edge = NumberField("Height of the Columns", default=3000)
    br2 = LineBreak()

    # Column spaces between columns
    column_spacing = NumberField("Distance between columns", default=2000)
    br3 = LineBreak()

    # The profile to use
    text_profile = Text("Enter the profiles of the elements")
    profile_columns = AutocompleteField("Profile of the Columns", options=profiles, default="HEA100", flex=25)
    profile_beams = AutocompleteField("Profile of the Beams", options=profiles, default="HEA100", flex=25)
    profile_braces = AutocompleteField("Profile of the Wind Braces", options=profiles, default="L20/4", flex=25)
    profile_footings = AutocompleteField("Profile of the Footings", options=footings, default="750*750", flex=25)
    br4 = LineBreak()

    # Materials
    text_materials = Text("Enter the materials of the elements")
    material_columns = AutocompleteField("Material of the Columns", options=materials, default="S235JR", flex=25)
    material_beams = AutocompleteField("Material of the Beams", options=materials, default="S235JR", flex=25)
    material_braces = AutocompleteField("Material of the Wind Braces", options=materials, default="S235JR", flex=25)
    material_footings = AutocompleteField("Material of the Footings", options=foot_mats, default="C30/37", flex=25)


class Controller(ViktorController):
    label = 'Steel Construction in Tekla'
    parametrization = Parametrization

    @IFCView("IFC Viewer", duration_guess=5)
    def show_ifc(self, params, entity_id, **kwargs):
        # Create empty file to dump the params json in
        file = File()
        params['export_ifc'] = True
        with file.open() as f:
            json.dump(params, f)

        # Run the python script and obtain the output files
        generic_analysis = GenericAnalysis(files=[('input.json', file)],
                                           executable_key="run_tekla",
                                           output_filenames=["output.ifc"])
        generic_analysis.execute(timeout=60)

        return_ifc = generic_analysis.get_output_file("output.ifc", as_file=True)

        return IFCResult(return_ifc)