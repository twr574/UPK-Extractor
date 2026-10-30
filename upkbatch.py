import subprocess
import pathlib
import os
import shutil
import time

def process_upk_batch(exe_path, upk_dir=".", max_files=None, target_extensions=None):
    """
    Processes .upk files and moves ONLY specific extension files to EXE's directory
    
    Args:
        exe_path: Path to the EXE (e.g., "D:/extract.exe")
        upk_dir: Directory containing .upk files
        max_files: Max .upk files to process (default: all)
        target_extensions: List of extensions to move (e.g., [".SOUNDNODEWAVE"])
    
    Returns:
        Dictionary with:
        - "success": Total processed .upk files
        - "failures": Count of failed .upk files
        - "moved_files": List of moved files
    """
    
    # Get all .upk files
    upk_files = [f for f in os.listdir(upk_dir) if f.endswith(".upk")]
    if max_files:
        upk_files = upk_files[:max_files]

    results = {
        "success": 0,
        "failures": 0,
        "moved_files": []
    }

    for upk_file in upk_files:
        upk_path = os.path.join(upk_dir, upk_file)
        try:
            # Run EXE with EXE's folder as working directory
            subprocess.run(
                [exe_path, upk_path],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=os.path.dirname(exe_path)
            )

            # ONLY process if target_extensions is provided
            if target_extensions:
                # Extract directory (e.g., "file" from "file.upk")
                extract_dir = os.path.dirname(exe_path)
                output_dir = os.path.join(extract_dir, "OUTPUT")
                os.makedirs(output_dir, exist_ok=True)
                
                # Find ALL files with target extensions (recursively) from the new subfolder
                target_subfolder = os.path.join(extract_dir, pathlib.Path(upk_file).stem)
                
                print(f"Searching folder: {target_subfolder}")
                # print(f" Targeting extensions: {target_extensions}")
                # print(f" Files found in {target_subfolder}: {os.listdir(target_subfolder)}")
                
                for file_path in find_files_with_extensions_recursive(target_subfolder, target_extensions):
                    dest_path = move_file_to_dir(file_path, output_dir)
                    if dest_path:
                        base_name = os.path.splitext(dest_path)[0]
                        new_ogg_path = base_name + '.ogg'
                        
                        # Strategy for dealing with duplicate files: 'delete' discards them, 'rename' retains them.
                        duplicates = 'delete'
                        if duplicates == "delete":
                            if os.path.exists(new_ogg_path):
                                try:
                                    os.remove(dest_path)
                                except Exception as e:
                                    raise RuntimeError(f"Failed to delete original: {e}")
                            else:
                                try:
                                    os.rename(dest_path, new_ogg_path)
                                except Exception as e:
                                    raise RuntimeError(f"Failed to create .ogg: {e}")
                                    
                        elif duplicates == "rename":
                            counter = 1
                            while True:
                                candidate = f"{base_name}({counter}).ogg"
                                if not os.path.exists(candidate):
                                    new_ogg_path = candidate
                                    break
                                counter += 1
                            try:
                                os.rename(dest_path, new_ogg_path)
                            except Exception as e:
                                print(f" Failed to rename {dest_path} → {new_ogg_path}: {str(e)}")
                                
                        results["moved_files"].append(os.path.basename(new_ogg_path))
            try:
                shutil.rmtree(target_subfolder)
            except Exception as e:
                print(f"Failed to delete temporary folder {target_subfolder}: {e}")
    
            results["success"] += 1

        except Exception as e:
            results["failures"] += 1
            print(f"Failed to process {upk_path}: {str(e)}")

    return results


def find_files_with_extensions_recursive(directory, extensions):
    """Recursively finds files with target extensions in all subdirectories"""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Get extension (correctly handles dots in filename)
            file_ext = os.path.splitext(file)[1]
            # Case-insensitive check
            if file_ext.upper() in [ext.upper() for ext in extensions]:
                yield file_path


def move_file_to_dir(file_path, target_dir):
    """Move file to target directory (creates target if needed)"""
    try:
        os.makedirs(target_dir, exist_ok=True)
        dest_path = os.path.join(target_dir, os.path.basename(file_path))
        os.replace(file_path, dest_path)
        return dest_path
    except Exception as e:
        print(f"Failed to move {file_path}: {str(e)}")
        return None

# ====== RUN CODE ======
if __name__ == "__main__":
    # .py script current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # EXE path (e.g., "C:/path/to/extract.exe")
    EXE_PATH = os.path.join(base_dir, "extract.exe")
    
    # Target extensions (e.g., ".SOUNDNODEWAVE")
    TARGET_EXTENSIONS = [".SOUNDNODEWAVE",".RFMODSound"]
    
    # Set UPK_DIR to be the 'INPUT' folder in the script's directory - this contains .upk files
    UPK_DIR = os.path.join(base_dir, "INPUT")
    
    # Process and get results
    results = process_upk_batch(
        exe_path=EXE_PATH,
        upk_dir=UPK_DIR,
        target_extensions=TARGET_EXTENSIONS
    )
    
    print("\n Results:")
    print(f" Success: {results['success']} .upk files processed")
    print(f" Failures: {results['failures']}")
    # print(f" Moved files: {results['moved_files']}")
    time.sleep(2)
