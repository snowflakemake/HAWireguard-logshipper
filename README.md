# Wireguard Logshipper

This project provides tools for managing and parsing Wireguard VPN logs from the Home assistan add-on to an Elastic server.

## Project Structure

- `main.py`: Entry point for running log management tasks.
- `parser.py`: Contains functions for parsing Wireguard logs.
- `.env`: Environment variables for configuration.

## Getting Started

1. **Clone the repository**  
   ```sh
   git clone https://github.com/snowflakemake/HAWireguard-logshipper.git
   cd HAWireguard-logshipper
   ```

2. **Set up environment variables**  
   Edit the `.env` file to configure your environment.

```
HA_TOKEN=your_home_assistant_token
HA_URL=http://localhost:8123/api/hassio/addons/a0d7b954_wireguard/logs
ES_PASS=your_elastic_password
ES_USER=your_elastic_user
ES_HOST="http://localhost:9200"
```

3. **Run the main script**  
   ```sh
   python3 main.py
   ```

## Requirements

- Python 3.12+
- See [requirements file](requirements.txt).

## Usage

- Configure the `.env` file with your Home Assistant and Elasticsearch details.
- Install dependencies using `pip install -r requirements.txt`.
- Run `main.py` to process and analyze logs.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome, please submit your bugs or ideas with an issue!