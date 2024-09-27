import time
import sys

def main():
    try:
        # Simulate some processing
        print("Processing started...")
        time.sleep(2)  # Simulate a delay
        print("Processing completed successfully.", file=sys.stdout)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
