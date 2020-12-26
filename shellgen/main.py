from ogabog.cores import argutils, controller
import modules

args = argutils.core_args()
args.description = "Generate shell"
controller.program_handler(modules, args)
