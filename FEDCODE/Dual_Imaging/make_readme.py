import os

with open('README.md', 'w') as wf:
    wf.write(
        """
# Static Renderings of These Notebooks
___
\n"""
    )
    for f in os.listdir():
        if 'ipynb' in f and 'checkpoints' not in f:
            wf.write(
                "## [{}](https://nbviewer.jupyter.org/github/ubcbraincircuits/Dual_Imaging/blob/master/FEDCODE/Dual_Imaging/{})\n".format(f, f.replace(" ", "%20"))) 
