import glob
import json

from haralyzer import HarParser


def process_har_file(input_file):
    with open(input_file, 'rb') as f:
        content = f.read().decode('utf-8')
        har_parser = HarParser(json.loads(content))

    json_data = []

    for page in har_parser.pages:
        for entry in page.entries:
            mime_type = entry['response']['content'].get('mimeType', '')
            if mime_type == "application/json":
                raw_response = entry['response']['content'].get('text', '')
                if raw_response:
                    json_data.append(json.loads(raw_response))

    return json_data

def write_json_to_file(json_objects, output_file_name):
    with open(output_file_name, "w") as out_file:
        json.dump(json_objects, out_file, indent=6)


if __name__ == '__main__':
    har_files = glob.glob('*.har')

    for input_file in har_files:
        json_objects = process_har_file(input_file)
        if json_objects:
            output_file_name = input_file + '.json'
            write_json_to_file(json_objects, output_file_name)
            print(f"Processed {input_file} and saved to {output_file_name}")
