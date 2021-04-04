from setuptools import setup, find_packages

with open("auto/__init__.py", encoding="utf-8") as f:
    for line in f:
        if (line.startswith("__version__")):
            VERSION = line.strip().split()[-1][1:-1]
            break
      
setup(name="auto",
      version=VERSION,
      description="Automatic data analysis every time a new file is saved.",
      author="Hanjin Liu",
      author_email="liuhanjin-sc@g.ecc.u-tokyo.ac.jp",
      packages=find_packages(),
      python_requires=">=3",
      )