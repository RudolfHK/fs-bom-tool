# Update 
Currently unfinished, i will shift the focus from clickup to excel. Goal is to have something finished by the end of 2025.
Working on dev branch.


# fs-bom-tool

This tool is designed for Formula Student Teams that use Excel fpr their internal bom. When finished it should enable users to automatically import their vehicle modules and parts into the FSG BOM Tool.

## Features

- **Automated Import**: Seamlessly import vehicle modules and parts from Excel.
- **CLI Tool**: Easy to set up and use with commands 
- **Efficient Management**: Streamline your BOM management process.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/RudolfHK/fs-clickup-bom-tool.git
    ```
2. Navigate to the project directory:
    ```sh
    cd fs-clickup-bom-tool
    ```
3. Install the required dependencies:
    ```sh
    pip install fs-clickup-bom-tool
    ```

## Usage
1. Create .env file in head dir

2. write your FSG BOM tool credentials in the .env file like this
    ```sh
    FSGUSER = name
    FSGPASSWD = password
    ```

3. Run the tool:
    ```sh
    python fs-clickup-bom-tool
    ```

4. Use help for commands (Work in progress).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact me by email: [EMAIL](mailto:s0583210@htw-berlin.de).

