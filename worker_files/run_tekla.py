# THIS FILE HAS TO BE ON THE VIKTOR WORKER DIRECTORY

# Pip install required packages [on worker]
import os
import json

# PyTekla wrapper
from pytekla import wrap
from Tekla.Structures.Model import Model
from Tekla.Structures.Model.Operations import Operation


class Beam:
    start_point = (0, 0, 0)
    end_point = (0, 0, 0)
    profile = "IPE300"
    material = "S235JR"

    def __init__(self, start, end, profile, material):
        self.start_point = start
        self.end_point = end
        self.profile = profile
        self.material = material

    def insert_beam(self):
        beam = wrap("Model.Beam")
        # Create beam from 2pt
        beam.start_point = wrap("Geometry3d.Point", self.start_point[0], self.start_point[1], self.start_point[2])
        beam.end_point = wrap("Geometry3d.Point", self.end_point[0], self.end_point[1], self.end_point[2])
        # Add some data
        beam.name = "PYTEKLA BEAM"
        beam._class = "11"  # Cannot use "class" in lowercase
        beam.profile = self.profile
        # Insert the material
        material = wrap("Model.Material")
        material.material_string = self.material
        beam.material = material
        # Add position
        beam_pos = wrap("Model.Position")
        beam_pos.rotation_offset = 0
        beam_pos.depth = wrap("Model.Position.DepthEnum").BEHIND
        beam.position = beam_pos

        # Insert the beam in the model
        beam.insert()

def save_model_as_ifc(path : str) -> bool:
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


# Set the compute_rhino3d.Util.url, default URL is http://localhost:6500/
compute_rhino3d.Util.url = 'http://localhost:6500/'

# Define path to local working directory
workdir = os.getcwd() + '\\'

# Read input parameters from JSON file
with open(workdir + 'input.json') as f:
    params = json.load(f)

# Create a reference to the model

# Create the three beams first
side_beam_1 = Beam((0, 0, params['height_edge']), (0, params['length'], params['height_edge']), "IPE300", "S235JR")
side_beam_2 = Beam((params['width'], 0, params['height_edge']), (params['width'], params['length'], params['height_edge']), "IPE300", "S235JR")
up_beam = Beam((params['width'] / 2, 0, params['height_ridge']), (params['width'] / 2, params['length'], params['height_edge']), "IPE300", "S235JR")


# Do Stuff


# Save ifc
path = workdir + 'output.ifc'
# save_model_as_ifc(path)

