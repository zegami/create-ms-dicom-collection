# Zegami MS-DICOM collection creation script
This script provides a simple way to create a Zegami collection comprising the set of DICOM images available from an instance of Microsoft Medical Imaging Server for DICOM.

## Instructions for use

### Prerequisites
* Sign up for a free Zegami trail account at https://zegami.com
* Install python requirements for this script
```
pip install -r requirements.txt
```

### Generate the csv file
```
python generate_collection_csv.py <servername>
```
replacing `<servername>` with the origin of the server

This will generate a file named `dicom_instances.csv`, containing a set of URLs at which each instance on the server can be found.

### Creating the Zegami collection
In order to use this file to create a Zegami collection, you will first need to sign up for a free Zegami trial account.

*NOTE* `zegami-cli` version `1.4.0` or greater is required

With a valid account use the cli to log in:
```
zeg login
```

Then create the collection using the CLI and the yaml config file provided in this repository:
```
zeg create collections --project <your project id> --config dicom_collection.yml
```

Replacing `<your project id>` with your own 8 character ID, which can be found on your Zegami workspace page.

### Await processing
If you now log into zegami.com, the collection should be visible in the selected workspace, and should be in a state of `Fetching Images`
Zegami's cloud processing platform will now begin fetching the DICOM images from the archive and will proceed to extract and process them ready for viewing.
Depending on the size of the collection, it will be ready to view in anything from a few minutes to a couple of hours.
