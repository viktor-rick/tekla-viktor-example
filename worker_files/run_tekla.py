# THIS FILE HAS TO BE ON THE VIKTOR WORKER DIRECTORY

# Run these in command line (and restart the worker) before running this script!
# import pytekla
# pytekla.config.set_tekla_path("C:/Program Files/Tekla Structures/2023.0/bin") <- set to your bin folder

# Pip install required packages [on worker]
import os
import json
import math

import ctypes  # An included library with Python install.

# PyTekla wrapper
from pytekla import wrap
from Tekla.Structures.Model import Model
from Tekla.Structures.Model.Operations import Operation
from Tekla.Structures.Drawing import Connection
from System.Collections.Generic import List
from System import String


class Beam:
    """"Please note that beams/footers/columns are all Beams under Tekla Open API"""

    # Standard values
    start_point = (0, 0, 0)
    end_point = (0, 0, 0)
    profile = "IPE300"
    material = "S235JR"
    beam_type = "BEAM"

    def __init__(self, beam_type, start, end, profile, material):
        self.start_point = start
        self.end_point = end
        self.profile = profile
        self.material = material
        self.beam_type = beam_type  # Either "BEAM" or "COLUMN" or "FOOTING"
        self.insert_beam()

    def insert_beam(self):
        beam = wrap("Model.Beam")
        # Create beam from 2pt
        beam.start_point = wrap("Geometry3d.Point", self.start_point[0], self.start_point[1], self.start_point[2])
        beam.end_point = wrap("Geometry3d.Point", self.end_point[0], self.end_point[1], self.end_point[2])
        # Add some data
        beam.name = "PYTEKLA " + self.beam_type
        if self.beam_type == "BEAM":
            beam._class = "11"
        elif self.beam_type == "COLUMN":
            beam._class = "2"
        elif self.beam_type == "FOOTING":
            beam._class = "8"

        # Insert the profile
        beam_profile = wrap("Model.Profile")
        beam_profile.profile_string = self.profile
        beam.profile = beam_profile

        # Insert the material
        material = wrap("Model.Material")
        material.material_string = self.material
        beam.material = material
        # Add position
        beam_pos = wrap("Model.Position")
        beam_pos.rotation_offset = 0
        if self.beam_type == "BEAM":
            beam_pos.depth = wrap("Model.Position.DepthEnum").BEHIND
        else:
            beam_pos.depth = wrap("Model.Position.DepthEnum").MIDDLE
        beam_pos.plane = wrap("Model.Position.PlaneEnum").MIDDLE
        beam.position = beam_pos

        # Insert the beam in the model
        beam.insert()


def save_model_as_ifc(path: str) -> bool:
    """This is a function to save the active Tekla model as IFC"""
    model = wrap("Model.Model")
    myie = List[String]()
    myie.Add("..//default//General//Shared//IFC//AdditionalPSets//CIP Construction data.xml")
    flags = Operation.IFCExportFlags()
    flags.IsLocationFromOrganizer = True
    flags.IsPoursEnabled = True

    success = Operation.CreateIFC4ExportFromAll(
        path,
        Operation.IFCExportViewTypeEnum.REFERENCE_VIEW,
        myie,
        Operation.ExportBasePoint.GLOBAL,
        "__Name__",
        "ByObjectClass",
        flags,
        "")
    return success


# Define path to local working directory
workdir = os.getcwd() + '\\'

# Read input parameters from JSON file
with open(workdir + 'input.json') as f:
    params = json.load(f)

# Clear the model
model = wrap('Model.Model')
for tekla_obj in model.get_objects_with_types(["Beam"]):
    if tekla_obj:
        tekla_obj.Delete()

# Assign params to variables
w, l = params["width"], params["length"]
h1, h2 = params["height_edge"], params["height_ridge"]
p_col, p_beam, p_brace, p_foot = params["profile_columns"], params["profile_beams"], params["profile_braces"], params[
    "profile_footings"]
mat_col, mat_beam, mat_brace, mat_foot = params["material_columns"], params["material_beams"], params[
    "material_braces"], params["material_footings"]

# Create the three beams first
Beam("BEAM", (0, 0, h1), (0, l, h1), p_beam, mat_beam)
Beam("BEAM", (w, 0, h1), (w, l, h1), p_beam, mat_beam)
Beam("BEAM", (w / 2, 0, h2), (w / 2, l, h2), p_beam, mat_beam)

# Now loop through the x positions (on the length) and create 2 columns and 3 beams (/ & \ and __)
n_col = int(math.ceil(l / params["column_spacing"]))
for n in range(n_col + 1):
    # Calculate x position
    x = n * (l / n_col)

    # Generate columns
    Beam("COLUMN", (0, x, 0), (0, x, h1), p_col, mat_col)
    Beam("COLUMN", (w, x, 0), (w, x, h1), p_col, mat_col)

    # Genearte cross beams
    Beam("BEAM", (0, x, h1), (w, x, h1), p_beam, mat_beam)
    Beam("BEAM", (0, x, h1), (w / 2.0, x, h2), p_beam, mat_beam)
    Beam("BEAM", (w / 2.0, x, h2), (w, x, h1), p_beam, mat_beam)

    # Generate Footings
    Beam("FOOTING", (0, x, 0), (0, x, -500.0), p_foot, mat_foot)
    Beam("FOOTING", (w, x, 0), (w, x, -500.0), p_foot, mat_foot)

    # Generate Wind Braces
    if n != 0:
        x1 = (n - 1) * (l / n_col)
        Beam("BEAM", (0, x, 0), (0, x1, h1), p_brace, mat_brace)
        Beam("BEAM", (0, x, h1), (0, x1, 0), p_brace, mat_brace)

        Beam("BEAM", (w, x, 0), (w, x1, h1), p_brace, mat_brace)
        Beam("BEAM", (w, x, h1), (w, x1, 0), p_brace, mat_brace)

model.commit_changes("Viktor changes")  # Delete this line if you dont want Tekla visualization

# Save ifc
path = workdir + 'output.ifc'
success = save_model_as_ifc(path)