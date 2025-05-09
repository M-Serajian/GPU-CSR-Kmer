import os
import subprocess

# Find the directory where run_gerbil.py is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURRENT_DIR)
# Move two levels up (from src/ -> GPU_CSR_Kmer/ -> include/gerbil-DataFrame/build/gerbil)
GERBIL_EXECUTABLE = os.path.join(CURRENT_DIR, '..', 'include', 'gerbil-DataFrame', 'build', 'gerbil')
GERBIL_EXECUTABLE = os.path.abspath(GERBIL_EXECUTABLE)


def set_of_all_unique_kmers_extractor(genome_file, output_directory, kmer_length, min_threshold, max_threshold, temp_directory, disable_normalization=False, enable_gpu=True):
    """Run the gerbil-DataFrame tool to extract unique k-mers from the given genome file."""
    command = [
        GERBIL_EXECUTABLE,
        "-k", str(kmer_length),
        "-o", "csv",
        "-l", str(min_threshold),
        "-z", str(max_threshold)]
    
    if enable_gpu:
        command.append("-g")
    
    # Add the -d flag if disable_normalization is True
    if disable_normalization:
        command.append("-d")
    
    command.extend([genome_file, temp_directory, output_directory])
    
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Unique k-mers successfully extracted and stored at: {output_directory}")
    except subprocess.CalledProcessError as error:
        print(f"Error: Extraction of unique k-mers failed with return code {error.returncode}.")
        print(f"Standard Output:\n{error.stdout}")
        print(f"Standard Error:\n{error.stderr}")


def single_genome_kmer_extractor(kmer_size, tmp_dir, output_file, genome_dir, disable_normalization=False, enable_gpu=True):
    """Extract k-mers from a single genome using the gerbil-DataFrame tool."""
    
    command = [
        GERBIL_EXECUTABLE,
        "-k", str(kmer_size),
        "-o", "csv",
        "-l", str(1),
        "-z", str(10**9)]
    
    
    if enable_gpu:
        command.append("-g")

    # Add the -d flag if disable_normalization is True
    if disable_normalization:
        command.append("-d")
    
    command.extend([genome_dir, tmp_dir, output_file])
    
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    
    return output_file
