# Product Config Portal Client
The Product Config Portal Client is the client-side component of the Product Config Portal application. This client is built using Streamlit and is responsible for visualizing configuration data from the database. It also provides form inputs for creating and editing entries in the table.

## Steps to Run the Streamlit Client
Before running the Streamlit client, make sure you have Python 3.7+ installed.

## Using the Command Line
1. Install the required Python packages using pip:
```bash
python -m pip install -r ./requirements.txt
```

2. Navigate to the source directory:
```bash
cd ./src/
```
3. Run the Streamlit application with the desired server port (e.g., 8051):
```bash
streamlit run app.py --server.port=8051
```
4. Open your web browser and enter the address of the application.

The application should now be live and accessible in your web browser.