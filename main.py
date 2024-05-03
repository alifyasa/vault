#!/usr/bin/python3
import subprocess
import argparse


def encrypt_file(file_path):
    """
    Encrypt a file with GPG.

    Uses subprocess to call GPG to encrypt a file.
    """
    # Get file name from file path
    file_name = file_path.split("/")[-1]
    # Get file path without file name
    file_directory = "/".join(file_path.split("/")[:-1])

    try:
        subprocess.run(
            [
                "gpg",
                "--output",
                f"{file_directory}/encrypted-{file_name}",
                "--symmetric",
                file_path,
            ]
        )
    except subprocess.CalledProcessError as e:
        print(f"Encryption failed: {e}")


def decrypt_file(file_path):
    """
    Decrypt a file with GPG.
    """
    # Get file name from file path
    file_name = file_path.split("/")[-1]
    # Get file path without file name
    file_directory = "/".join(file_path.split("/")[:-1])

    # If file name does not start with "encrypted-", return an error
    if not file_name.startswith("encrypted-"):
        print("File is not encrypted.")
        return

    # Remove "encrypted-" from file name
    file_name = file_name.replace("encrypted-", "")

    try:
        subprocess.run(
            ["gpg", "--output", f"{file_directory}/{file_name}", "--decrypt", file_path]
        )
    except subprocess.CalledProcessError as e:
        print(f"Decryption failed: {e}")


def main():
    """
    Main function to run the CLI using argparse.
    """

    parser = argparse.ArgumentParser(description="Encrypt and decrypt files with GPG.")
    parser.add_argument("file", type=str, help="File to encrypt or decrypt.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the file.")
    group.add_argument(
        "-d",
        "--decrypt",
        action="store_true",
        help="Decrypt the file.",
    )

    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.file)
    elif args.decrypt:
        decrypt_file(args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
