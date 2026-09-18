"""
========================================================================
RE4 FEN Modern Python Tool (Extract & Repack Utility)
------------------------------------------------------------------------
- Original Concept & QuickBMS Script: 're4_lfs_fen.bms' (v0.1.2)
- Author of Original Script: Luigi Auriemma (https://aluigi.altervista.org/)
- Modern Python Adaptation & Optimization: 3rfaja (ARFAJA)
- Features: Drag-and-Drop support, Report generation, Backup cleanup.
========================================================================
"""

import os
import zlib
import glob
import sys
import time
from datetime import datetime

def print_banner():
    print("=" * 65)
    print("      RE4 FEN Advanced Python Tool (PS4 / Switch)")
    print("      Adapted & Developed by: 3rfaja (ARFAJA)")
    print("      Based on Luigi Auriemma's QuickBMS re4_lfs_fen script")
    print("=" * 65)

def write_report(log_lines):
    report_path = "process_report.txt"
    try:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            for line in log_lines:
                f.write(line + "\n")
    except Exception as e:
        print(f"[!] Could not write report: {e}")

def extract_fen_files(specific_file=None):
    print_banner()
    print("[*] Starting extraction process...")
    start_time = time.time()
    logs = []
    
    if specific_file:
        fen_files = [specific_file] if specific_file.endswith(".fen") else []
    else:
        fen_files = glob.glob("**/*.fen", recursive=True)
        
    if not fen_files:
        print("[!] No .fen files found for extraction.")
        return

    success_count = 0
    fail_count = 0
    
    for fen_path in fen_files:
        if not os.path.exists(fen_path):
            print(f"[!] File not found: {fen_path}")
            continue
        try:
            print(f"[-] Extracting: {fen_path}")
            with open(fen_path, "rb") as f:
                content = f.read()
                
            if len(content) < 4:
                print(f"    [!] Warning: File too small, skipping.")
                logs.append(f"FAILED: {fen_path} (Too small)")
                fail_count += 1
                continue
                
            compressed_data = content[4:]
            decompressed_data = zlib.decompress(compressed_data)
            
            out_path = fen_path[:-4]
            with open(out_path, "wb") as out_f:
                out_f.write(decompressed_data)
                
            print(f"    [✔] Extracted successfully -> {out_path}")
            logs.append(f"SUCCESS EXTRACT: {fen_path} -> {out_path}")
            success_count += 1
        except Exception as e:
            print(f"    [!] Error extracting {fen_path}: {e}")
            logs.append(f"ERROR EXTRACT: {fen_path} - {e}")
            fail_count += 1
            
    elapsed = time.time() - start_time
    summary = f"Extraction Complete. Success: {success_count} | Failed: {fail_count} | Time: {elapsed:.2f}s"
    print("-" * 65)
    print(f"[✔] {summary}")
    logs.append(summary)
    write_report(logs)

def repack_fen_files(specific_file=None):
    print_banner()
    print("[*] Starting repack & compression process...")
    start_time = time.time()
    logs = []
    
    if specific_file:
        if specific_file.endswith(".fen"):
            target_file = specific_file[:-4]
            fen_path = specific_file
        else:
            target_file = specific_file
            fen_path = specific_file + ".fen"
        unpacked_files = [target_file] if os.path.exists(target_file) else []
    else:
        all_files = glob.glob("**/*", recursive=True)
        unpacked_files = [
            f for f in all_files 
            if os.path.isfile(f) 
            and not f.endswith(('.fen', '.py', '.bat', '.txt', '.zip', '.rar', '.bak'))
        ]
    
    if not unpacked_files:
        print("[!] No unpacked files found to repack.")
        return

    success_count = 0
    fail_count = 0
    
    for target_file in unpacked_files:
        if not specific_file:
            fen_path = target_file + ".fen"
        
        try:
            print(f"[-] Processing: {target_file}...", end="", flush=True)
            
            if os.path.exists(fen_path):
                backup_path = fen_path + ".bak"
                if not os.path.exists(backup_path):
                    os.replace(fen_path, backup_path)
            
            with open(target_file, "rb") as f:
                raw_data = f.read()
                
            uncompressed_size = len(raw_data)
            compressed_data = zlib.compress(raw_data, level=6)
            header = uncompressed_size.to_bytes(4, byteorder='little')
            
            with open(fen_path, "wb") as f:
                f.write(header + compressed_data)
                
            print(" [✔] Done!")
            logs.append(f"SUCCESS REPACK: {target_file} -> {fen_path} (Size: {uncompressed_size} bytes)")
            success_count += 1
        except Exception as e:
            print(f" [!] Error: {e}")
            logs.append(f"ERROR REPACK: {target_file} - {e}")
            fail_count += 1
            
    elapsed = time.time() - start_time
    summary = f"Repack Complete. Updated: {success_count} | Failed: {fail_count} | Time: {elapsed:.2f}s"
    print("-" * 65)
    print(f"[✔] {summary}")
    logs.append(summary)
    write_report(logs)

def clean_backups():
    print_banner()
    print("[*] Cleaning up backup (.bak) files...")
    bak_files = glob.glob("**/*.bak", recursive=True)
    if not bak_files:
        print("[!] No backup files found.")
        return
    
    count = 0
    for bak in bak_files:
        try:
            os.remove(bak)
            print(f"[-] Removed backup: {bak}")
            count += 1
        except Exception as e:
            print(f"[!] Could not remove {bak}: {e}")
    print(f"\n[✔] Cleaned up {count} backup file(s).")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        target_arg = sys.argv[2] if len(sys.argv) > 2 else None
        
        if mode == "extract":
            extract_fen_files(target_arg)
        elif mode == "repack":
            repack_fen_files(target_arg)
        elif mode == "clean":
            clean_backups()
    else:
        print("[!] Please run this script using the provided batch (.bat) files.")