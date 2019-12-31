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
- It used boto3 and click to create a cli interface for these functions
