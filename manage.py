#!/usr/bin/env python
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_PATH=os.path.dirname(os.path.realpath(__file__))

sys.path.append(REPO_PATH +os.sep+"apps")
sys.path.append(REPO_PATH+os.sep+"packages")
sys.path.append(REPO_PATH+os.sep+"packages/pkg_quicky")
sys.path.append(REPO_PATH+os.sep+"packages/pkg_qmongo")
sys.path.append(REPO_PATH+os.sep+"packages/pkg_qtracking")
sys.path.append(REPO_PATH+os.sep+"packages/pkg_qobjects")
sys.path.append(REPO_PATH+os.sep+"packages/django")
if __name__ == "__main__":
    from quicky import config_loader
    config_loader.set_base_dir(BASE_DIR)
    config_loader.start_app("config")

