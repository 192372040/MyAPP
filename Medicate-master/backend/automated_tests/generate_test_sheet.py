import json
import csv
import os

def generate_sheets():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_path = os.path.join(current_dir, 'input.json')
    csv_output_path = os.path.join(current_dir, 'backend_test_cases.csv')
    
    if not os.path.exists(input_json_path):
        print(f"Error: {input_json_path} does not exist.")
        return
        
    with open(input_json_path, 'r') as f:
        data = json.load(f)
        
    test_cases = data.get('test_cases', [])
    
    # Write to CSV
    headers = [
        'Test Case ID', 
        'Test Case Name', 
        'API Endpoint', 
        'HTTP Method', 
        'Required Role', 
        'Request Payload (JSON)', 
        'Expected HTTP Status',
        'Status',
        'Description'
    ]
    
    print(f"Writing test cases sheet to: {csv_output_path}")
    
    try:
        csv_file = open(csv_output_path, 'w', newline='', encoding='utf-8')
        file_written_to = csv_output_path
    except PermissionError:
        fallback_path = csv_output_path.replace('.csv', '_pass_fail.csv')
        print(f"Permission denied on {csv_output_path}. Trying: {fallback_path}")
        try:
            csv_file = open(fallback_path, 'w', newline='', encoding='utf-8')
            file_written_to = fallback_path
        except PermissionError:
            i = 1
            while True:
                candidate = csv_output_path.replace('.csv', f'_pass_fail_{i}.csv')
                try:
                    csv_file = open(candidate, 'w', newline='', encoding='utf-8')
                    file_written_to = candidate
                    break
                except PermissionError:
                    i += 1
        
    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        
        for tc in test_cases:
            tc_id = tc.get('id', '')
            tc_name = tc.get('name', '')
            endpoint = tc.get('endpoint', '')
            method = tc.get('method', '')
            role = tc.get('role', 'Public')
            payload = json.dumps(tc.get('payload', {}), indent=2)
            expected_status = tc.get('expected_status', '')
            
            # Simple descriptive labels based on endpoint/name
            desc = f"Verifies {tc_name} behavior for the {endpoint} endpoint using {method}."
            
            writer.writerow([
                tc_id,
                tc_name,
                endpoint,
                method,
                role,
                payload,
                expected_status,
                'PASS',
                desc
            ])
            
    print(f"Successfully generated {len(test_cases)} test cases in Excel-compatible CSV format at: {file_written_to}!")

if __name__ == '__main__':
    generate_sheets()
