# Setting up Conda Environment

To set up the Conda environment, follow these steps:

1. Create a Conda environment named `demo_rai` with Python version 3.11.8:
    ```bash
    conda create -n demo_rai python=3.11.8
    ```

2. Activate the `demo_rai` environment:
    ```bash
    conda activate demo_rai
    ```

3. Install required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
# Initialize a RelationalAI project
To initialize a RelationalAI project, run the following command:

```bash
rai init
```
- rai init walks you through setting up a RelationalAI project, connecting to a cloud platform, and saving a configuration file.

- The first time you run rai init, you will be prompted to enter your connection information:
Snowflake username and password. Then, select the Snowflake account and role to use for the project. The account must have the RelationalAI Native App installed and the role must be granted permission to use the app. Finally, select the RelationalAI native app and Snowflake compute warehouse to use with your project.

# Creating Data Stream

To create a data stream and synchronize Snowflake data into the RAI database, run this command:

```bash
rai imports:stream --source TELECOM.TOWER_DEMO.TOWER_DATA_V2 --model network_connectivity
```

- `--source`: This flag specifies the fully-qualified name of a Snowflake table or view.
- `--model`: This flag specifies the name of the model to which the data in the Snowflake table or view is streamed.

# Opening JupyterLab

To open JupyterLab from the terminal, use the following command:

```bash
jupyter lab
```