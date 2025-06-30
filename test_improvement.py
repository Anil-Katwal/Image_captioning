import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import improve_caption

def test_caption_improvement():
    """Test the caption improvement function"""
    
    test_captions = [
        "black and white dog is running in the grass",
        "man with blue shirt and white shirt is sitting on the floor",
        "two people are standing on the side of the mountain",
        "black dog is running through the water",
        "man is standing on the side of the street",
        "man in black shirt is standing on the ground"
    ]
    
    print("Testing Caption Improvement:")
    print("=" * 50)
    
    for caption in test_captions:
        improved = improve_caption(caption)
        print(f"Original:  '{caption}'")
        print(f"Improved:  '{improved}'")
        print("-" * 30)

if __name__ == "__main__":
    test_caption_improvement() 