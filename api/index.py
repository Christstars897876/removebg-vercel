from transparent_background import Remover
import base64
import io
import json
from PIL import Image

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        body = request.get_json()
        image_b64 = body.get("image_base64")
        if not image_b64:
            return {"statusCode": 400, "body": "Missing image_base64"}

        # Decode base64 to image
        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data))

        # Remove background
        remover = Remover()
        result = remover.remove(image)

        # Resize to max 512x512 to reduce response size
        # Note: Image.ANTIALIAS est obsolète dans les versions récentes de Pillow,
        # on utilise Image.Resampling.LANCZOS ou Image.LANCZOS pour éviter les bugs.
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.LANCZOS
            
        result.thumbnail((512, 512), resample_filter)

        # Convert to PNG + base64
        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # If base64 too large, return error
        if len(result_b64) > 5 * 1024 * 1024:  # 5MB limit
            return {
                "statusCode": 400,
                "body": "Processed image is too large to return as base64."
            }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"image_base64": result_b64})
        }

    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

# Variable globale pour que Vercel trouve l'entpoint (Point d'entrée)
app = handler
