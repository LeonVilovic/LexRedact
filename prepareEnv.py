import os, sys, shutil

def prepareClasslaResourcesIfNeeded():
    if getattr(sys, 'frozen', False):  # running from PyInstaller bundle
        bundle_dir = sys._MEIPASS
        resource_src = os.path.join(bundle_dir, "classla_resources")
        resource_dst = os.path.join(os.path.expanduser("~"), "classla_resources") #copy classla_resources folder to expected path

        if not os.path.exists(resource_dst):
            shutil.copytree(resource_src, resource_dst)