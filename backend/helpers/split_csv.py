import os

script_dir = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(script_dir, "..", "data", "movies.csv")
preprocessed_movies_path = os.path.join(script_dir, "..", "data", "preprocessed_movies.csv")

INPUT_FILE = preprocessed_movies_path
OUTPUT_PREFIX = 'split_part_'
MAX_LINES = 3250

def split_csv_by_lines(input_file, output_prefix, max_lines):
    """Splits a CSV file into smaller parts based on a maximum number of lines."""
    try:
        with open(input_file, 'r') as f:
            # 1. Read and save the header line
            header = f.readline()
            if not header:
                print("Error: Input file is empty.")
                return

            file_count = 1
            lines_in_current_file = 0
            outfile = None

            for line in f:
                # 2. Check if a new file needs to be started
                if outfile is None or lines_in_current_file >= max_lines:
                    if outfile:
                        outfile.close()
                    
                    # Define the new output file name
                    output_file_name = f'{output_prefix}{file_count}.csv'
                    outfile = open(output_file_name, 'w')
                    
                    # Write the header to the new file
                    outfile.write(header)
                    
                    lines_in_current_file = 0
                    file_count += 1
                
                # 3. Write the data line
                outfile.write(line)
                lines_in_current_file += 1

            # 4. Close the last file
            if outfile:
                outfile.close()

            print(f"Successfully split '{input_file}' into {file_count - 1} files.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    split_csv_by_lines(INPUT_FILE, OUTPUT_PREFIX, MAX_LINES)