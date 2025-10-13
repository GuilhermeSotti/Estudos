"""
timeit_inference.py
- Mede tempo médio de inferência (ms) e FPS estimado
- Para YOLO (ultralytics) e para CNN (PyTorch)
"""
import time
import torch
import numpy as np

def measure_cnn_inference(model, dataloader, n=100, device='cuda'):
    model.to(device)
    model.eval()
    times = []
    it = iter(dataloader)
    for i in range(n):
        imgs, _ = next(it)
        imgs = imgs.to(device)
        t0 = time.time()
        with torch.no_grad():
            _ = model(imgs)
        t1 = time.time()
        times.append((t1-t0)*1000)
    times = np.array(times)
    return times.mean(), times.std()

def measure_yolo_inference(yolo_model, images_list, n=100):
    import time
    times = []
    for i in range(n):
        img = images_list[i % len(images_list)]
        t0 = time.time()
        _ = yolo_model(img)
        t1 = time.time()
        times.append((t1-t0)*1000)
    return np.mean(times), np.std(times)
