# Shotty, a snapshot creator for EC2 instances in AWS

To run this:

- Make sure you have pipenv installed (brew install pipenv
- cd to the directory
- install dependencies from the pipfile (pipenv install)
- launch the virtual environment (pipenv shell)

## Notes

- To access the help prompt
  - pipenv run "python shotty/shotty.py --help"
- You will need an aws-cli profile setup named shotty that has access to read, stop and snapshot ec2 instances (I used ec2FullAccess on my end)
  - aws configure --profile shotty
- It uses boto3 and click to create a cli interface for these functions
- Ipython is included as a dev dependency in case you want to test anything interactively
- Setuptools is also included as a dev dependency for packaging and distribution
  - To create a wheel, use:
    - python setup.py bdist_wheel
  - Wheel can be used to install with pip via pip3 install dist/shotty
  - it can easily be used by placing the .whl file on s3 then sharing, so someone can pip install from there
