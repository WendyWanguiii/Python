import requests
import os
import hashlib
from urllib.parse import urlparse

def fetch_image(url, saved_hashes):
    try:
        # Make the request
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Check content-type header
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"✗ Skipped (Not an image): {url}")
            return

        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        # Generate full path
        filepath = os.path.join("Fetched_Images", filename)

        # Read the content into memory for hashing
        content = response.content
        image_hash = hashlib.md5(content).hexdigest()

        # Prevent duplicates based on content hash
        if image_hash in saved_hashes:
            print(f"✗ Skipped (Duplicate image): {filename}")
            return

        # Save the image
        with open(filepath, 'wb') as f:
            f.write(content)

        saved_hashes.add(image_hash)
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error while fetching {url}: {e}")
    except Exception as e:
        print(f"✗ Error while saving image: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create the directory for saving images
    os.makedirs("Fetched_Images", exist_ok=True)

    # Predefined nature image URLs (feel free to add more!)
    urls = [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "https://cdn2.thecatapi.com/images/MTY3ODIyMQ.jpg",
        "https://images.unsplash.com/photo-1470770903676-69b98201ea1c",
    ]

    print("Fetching predefined nature images...\n")

    saved_hashes = set()

    for url in urls:
        fetch_image(url, saved_hashes)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
