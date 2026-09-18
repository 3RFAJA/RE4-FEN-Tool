import os
import zlib
import glob

def auto_repack_fen():
    print("[*] Starting FEN Auto-Packer & Fixer...")
    
    # Search for all .fen files in the directory and subdirectories
    fen_files = glob.glob("**/*.fen", recursive=True)
    
    if not fen_files:
        print("[!] No .fen files found in the directory.")
        return

    for fen_path in fen_files:
        # Extract the base target name (e.g., 000000a0.pack from 000000a0.pack.fen)
        base_target = fen_path[:-4] if fen_path.endswith(".fen") else fen_path
        
        # Search for the corresponding unpacked modified file
        if not os.path.exists(base_target):
            # Try alternative formats if the extension differs slightly
            alt_target = base_target.replace(".pack", "")
            if os.path.exists(alt_target):
                base_target = alt_target
            else:
                print(f"[!] Skipping: Unpacked file not found for: {fen_path}")
                continue
        
        # 1 & 2. Read the modified file regardless of original name or size
        with open(base_target, "rb") as f:
            raw_data = f.read()
            
        uncompressed_size = len(raw_data)
        
        # 3. Compress data and generate new size dynamically (bypassing padding/HxD limits)
        compressed_data = zlib.compress(raw_data, level=9)
        
        # 4. Build the FEN header automatically (first 4 bytes represent uncompressed size)
        header = uncompressed_size.to_bytes(4, byteorder='little')
        
        # Write the new FEN file completely, bypassing larger/smaller size restrictions
        with open(fen_path, "wb") as f:
            f.write(header + compressed_data)
            
        print(f"[✔] Successfully repacked and processed: {fen_path}")

    print("\n[✔] Repack process completed for all files successfully!")

if __name__ == "__main__":
    auto_repack_fen()
    input("Press Enter to exit...")