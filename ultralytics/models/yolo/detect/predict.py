# Ultralytics YOLO 🚀, AGPL-3.0 license

from ultralytics.engine.predictor import BasePredictor
from ultralytics.engine.results import Results
from ultralytics.utils import ops
import torchvision.transforms as transforms
import cv2
import ast
import torch
from vicente.procesamiento import procesamiento_files


class DetectionPredictor(BasePredictor):
    """
    A class extending the BasePredictor class for prediction based on a detection model.

    Example:
        ```python
        from ultralytics.utils import ASSETS
        from ultralytics.models.yolo.detect import DetectionPredictor

        args = dict(model='yolov8n.pt', source=ASSETS)
        predictor = DetectionPredictor(overrides=args)
        predictor.predict_cli()
        ```
    """

    def postprocess(self, preds, img, orig_imgs):
        """Post-processes predictions and returns a list of Results objects."""
        ruta_txt = '/workspace/procesamiento/parameters.txt'  
        ruta_image = '/workspace/procesamiento/image.jpg'
        url = 'https://dcdc-157-100-108-85.ngrok-free.app/'
        image_public = "upload_image"
        txt_public = "upload_json"
        preds = ops.non_max_suppression(
            preds,
            self.args.conf,
            self.args.iou,
            agnostic=self.args.agnostic_nms,
            max_det=self.args.max_det,
            classes=self.args.classes,
        )

        if not isinstance(orig_imgs, list):  # input images are a torch.Tensor, not a list
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        results = []
        for i, pred in enumerate(preds):
            orig_img = orig_imgs[i]
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
            img_path = self.batch[0][i]
            results.append(Results(orig_img, path=img_path, names=self.model.names, boxes=pred))
            # Selecciona una sola imagen del lote (ajusta el índice según tus necesidades)
            # Muestra cada 10 frames
            single_img = orig_img
            # Convierte el tensor a un objeto de imagen de Pillow
            img_pil = transforms.ToPILImage()(single_img)
            img_pil.save(ruta_image)
            # Escribe las coordenadas en el archivo línea por línea
            with open(ruta_txt, 'w') as file:   
                file.write(f"{pred}\n")
            procesamiento_files(url, image_public, txt_public, ruta_txt, ruta_image)
        return results