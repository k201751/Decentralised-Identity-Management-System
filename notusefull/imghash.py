import hashlib

def hash_image(file_path, hash_algorithm='sha256'):
    """Generate a hash for the content of an image file."""
    hash_obj = hashlib.new(hash_algorithm)
    
    with open(file_path, 'rb') as file:
        # Read the file in chunks to handle large files
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

# Example usage
image_file_path = 'D:\Dev projects\IDmanage\img1.png'
hash_value = hash_image(image_file_path)
print(f"Hash of the image: {hash_value}")
