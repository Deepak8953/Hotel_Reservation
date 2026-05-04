from setuptools import setup, find_packages

# reading requirements.txt file line by line (each line have a different library name) then saving it in a var requirements
with open("requirements.txt") as f:
    HYPEN_E_DOT='-e .'
    requirements=f.readlines()
    requirements=[req.replace("\n","") for req in requirements]
    if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    setup(name='HOTEL-RESERVATION-PREDICTION', 
          version='0.1',
          author='Deepak',
          packages=find_packages(),
          install_requires=requirements,
          
        )
    

    # find_packages() will automatically detect all directories with __init__.py declared in it and convert them into a package. 
    # 'install_requires' this will install all the packages inside requirements.

    # to run setup.py 'pip install -e .'  This command automatically detect setup.py and runs it. 

    # Once you run above command you will notice "HOTEL_RESERVATION_PREDICTION.egg-info"  this folder is automatically created.
