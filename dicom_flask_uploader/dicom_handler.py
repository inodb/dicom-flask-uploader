from PIL import Image as pillow
import mudicom


def create_thumbnail(dcm_fn, output_fn, size=(128, 128), output_format=None):
    if not output_format:
        output_format = output_fn.split(".")[-1].upper()

    mu = mudicom.load(dcm_fn)
    mu.read()
    #TODO: Validate mu, requires extra dciodvfy dep
    # mu.validate()
    im = pillow.fromarray(mu.image.numpy.astype('uint8'))
    im.thumbnail(size)
    im.save(output_fn, output_format)
