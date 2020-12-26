from ogabog.cores import argutils, controller
import modules

args = argutils.core_args()
args.description = "Generate shell" # TODO improve description here
controller.program_handler(modules, args)
