# fs-clickup-bom-tool

This tool is designed for Formula Student Teams that use ClickUp as their project management tool. It allows users to automatically import their vehicle modules and parts into the FSG BOM Tool.

## Features

- **Automated Import**: Seamlessly import vehicle modules and parts from ClickUp.
- **User-Friendly Interface**: Easy to use with a clean and intuitive interface.
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

2. write your Clickup API KEY and FSG BOM tool credentials in the .env file like this
    ```sh
    CLICKUPAPIKEY = xxxxxxxxx
    FSGUSER = name
    FSGPASSWD = password
    ```

3. Run the tool:
    ```sh
    python fs-clickup-bom-tool
    ```

4. Follow the on-screen instructions to import your data from ClickUp.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or contact us.

