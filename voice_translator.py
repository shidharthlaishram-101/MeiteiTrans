import subprocess
import sys
import os


# ==========================================================
# SETTINGS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ENGLISH_TO_MEITEI = os.path.join(
    BASE_DIR,
    "english_voice_to_meitei_voice.py"
)

MEITEI_TO_ENGLISH = os.path.join(
    BASE_DIR,
    "meitei_to_english_voice.py"
)


# ==========================================================
# HEADER
# ==========================================================

def show_header():

    print()
    print("=" * 60)
    print("       MEITEI <-> ENGLISH VOICE TRANSLATOR")
    print("=" * 60)
    print()


# ==========================================================
# ENGLISH -> MEITEI
# ==========================================================

def english_to_meitei():

    print()
    print("=" * 60)
    print("             ENGLISH -> MEITEI")
    print("=" * 60)
    print()

    print("Starting English -> Meitei pipeline...")
    print()

    result = subprocess.run(
        [
            sys.executable,
            "-u",
            ENGLISH_TO_MEITEI
        ]
    )

    print()

    if result.returncode == 0:

        print("=" * 60)
        print("English -> Meitei completed.")
        print("=" * 60)

    else:

        print("=" * 60)
        print("English -> Meitei failed.")
        print("=" * 60)


# ==========================================================
# MEITEI -> ENGLISH
# ==========================================================

def meitei_to_english():

    print()
    print("=" * 60)
    print("             MEITEI -> ENGLISH")
    print("=" * 60)
    print()

    print("Starting Meitei -> English pipeline...")
    print()

    result = subprocess.run(
        [
            sys.executable,
            "-u",
            MEITEI_TO_ENGLISH
        ]
    )

    print()

    if result.returncode == 0:

        print("=" * 60)
        print("Meitei -> English completed.")
        print("=" * 60)

    else:

        print("=" * 60)
        print("Meitei -> English failed.")
        print("=" * 60)


# ==========================================================
# MAIN MENU
# ==========================================================

def main():

    while True:

        show_header()

        print("1. English -> Meitei")
        print("2. Meitei -> English")
        print("3. Exit")

        print()

        choice = input(
            "Enter your choice (1/2/3): "
        ).strip()

        # --------------------------------------------------
        # English -> Meitei
        # --------------------------------------------------

        if choice == "1":

            english_to_meitei()

            input(
                "\nPress Enter to return to the menu..."
            )

        # --------------------------------------------------
        # Meitei -> English
        # --------------------------------------------------

        elif choice == "2":

            meitei_to_english()

            input(
                "\nPress Enter to return to the menu..."
            )

        # --------------------------------------------------
        # Exit
        # --------------------------------------------------

        elif choice == "3":

            print()
            print("Exiting translator...")
            print("Goodbye!")

            break

        # --------------------------------------------------
        # Invalid choice
        # --------------------------------------------------

        else:

            print()
            print(
                "Invalid choice. "
                "Please select 1, 2, or 3."
            )

            input(
                "\nPress Enter to continue..."
            )


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":
    main()