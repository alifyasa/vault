#!/usr/bin/python3
import subprocess
import argparse


def main():
    """
    Main function to run the CLI using argparse.
    """

    parser = argparse.ArgumentParser(description="Encrypt and decrypt files with GPG.")
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument(
        "-e", "--encrypt", type=str, metavar="FILE", help="Encrypt the file."
    )
    mutex_group.add_argument(
        "-d",
        "--decrypt",
        type=str,
        metavar="FILE",
        help="Decrypt the file.",
    )
    mutex_group.add_argument(
        "--clean",
        action="store_true",
        help="Clean Vault. Delete all files untracked by git.",
    )

    args = parser.parse_args()

    if args.encrypt:
        encrypt_file(args.encrypt)
    elif args.decrypt:
        decrypt_file(args.decrypt)
    elif args.clean:
        clean_vault()
    else:
        parser.print_help()


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


def clean_vault():
    """
    Delete all files that are not tracked by git.
    """
    try:
        subprocess.run(["git", "clean", "-f", "-d", "-x"])
    except subprocess.CalledProcessError as e:
        print(f"Failed cleaning Vault: {e}")


if __name__ == "__main__":
    main()
