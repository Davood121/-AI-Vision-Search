import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class ImageAnalyzer:
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        print(f"Loading image analysis model: {model_name}...")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"Model loaded on {self.device}.")

    def analyze(self, image_path):
        """
        Analyzes the image and returns a text description.
        """
        try:
            raw_image = Image.open(image_path).convert('RGB')
            
            # Unconditional image captioning
            inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
            
            out = self.model.generate(**inputs)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            return caption
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    # Test block
    import sys
    if len(sys.argv) > 1:
        analyzer = ImageAnalyzer()
        print("Caption:", analyzer.analyze(sys.argv[1]))
    else:
        print("Please provide an image path to test.")
