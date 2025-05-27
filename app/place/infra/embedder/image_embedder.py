import clip
from PIL import Image
import torch
import io


# 해당 코드는 gpu는 고려되지 않고, 개발 되었음. 이후에 gpu를 넣을 수 있는 상황이 오면 고려해보자.
class ImageEmbedder:
    def __init__(self, model_name: str = "ViT-B/32"):
        self.model, self.preprocess = clip.load(model_name)

    def embed(self, image: bytes) -> list[float]:
        pil_image = Image.open(io.BytesIO(image)).convert("RGB")
        image_tensor = self.preprocess(pil_image).unsqueeze(0)
        with torch.no_grad():
            feat = self.model.encode_image(image_tensor)
            features = torch.nn.functional.normalize(feat, dim=-1)
        return features[0].cpu().tolist()  # ✅ GPU 환경에서도 안전하게 리스트 변환
