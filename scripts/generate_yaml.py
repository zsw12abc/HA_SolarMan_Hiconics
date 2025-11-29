# -*- coding: utf-8 -*-
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Matches scan results with screenshot data to generate a custom_hiconics.yaml file."
    )
    parser.add_argument(
        "--scan-file",
        type=str,
        required=True,
        help="Path to the scan_result.txt file from the inverter."
    )
    parser.add_argument(
        "--screenshot-data-file",
        type=str,
        required=True,
        help="Path to a text file containing key-value pairs of data extracted from the screenshot."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="custom_hiconics.yaml",
        help="Path for the output YAML file."
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    logging.info(f"Starting YAML generation process...")
    logging.info(f"Scan result file: {args.scan_file}")
    logging.info(f"Screenshot data file: {args.screenshot_data_file}")
    logging.info(f"Output YAML file: {args.output_file}")

    # TODO:
    # 1. Read and parse scan_file
    # 2. Read and parse screenshot_data_file
    # 3. Implement matching logic
    # 4. Generate YAML file


if __name__ == "__main__":
    main()
