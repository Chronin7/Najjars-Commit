from direct.showbase.ShowBase import ShowBase
import sys
import os

# 1. We use a hidden ShowBase to initialize the engine without a window
base = ShowBase(windowType='none')

def convert(input_path, output_path):
    print(f"Loading {input_path}...")
    
    # 2. Load the model. 
    # This works if you have panda3d-gltf installed
    model = base.loader.loadModel(input_path)
    
    if model:
        # 3. Save as .bam
        model.write_bam_file(output_path)
        print(f"Success! Saved as: {output_path}")
    else:
        print("Failed to load model.")

if __name__ == "__main__":
    # You can change these filenames here:
    source = "src/mple.glb"
    destination = "src/placeholder_player.glb"
    
    if os.path.exists(source):
        convert(source, destination)
    else:
        print(f"Error: Could not find {source}")