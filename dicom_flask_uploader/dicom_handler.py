import dicom
import mudicom
from dicom.UID import NotCompressedPixelTransferSyntaxes
from dicom.contrib.pydicom_PIL import get_LUT_value
from PIL import Image as pillow


# From pydicom/contrib/pydicom_PIL
# Waiting for PR merge: https://github.com/darcymason/pydicom/pull/283
def get_PIL_image(dataset):
    """Get Image object from Python Imaging Library(PIL)"""
    if ('PixelData' not in dataset):
        raise TypeError("Cannot show image -- DICOM dataset does not have "
                        "pixel data")
    # can only apply LUT if these window info exists
    if ('WindowWidth' not in dataset) or ('WindowCenter' not in dataset):
        bits = dataset.BitsAllocated
        samples = dataset.SamplesPerPixel
        if bits == 8 and samples == 1:
            mode = "L"
        elif bits == 8 and samples == 3:
            mode = "RGB"
        elif bits == 16:
            # not sure about this -- PIL source says is 'experimental'
            # and no documentation. Also, should bytes swap depending
            # on endian of file and system??
            mode = "I;16"
        else:
            raise TypeError("Don't know PIL mode for %d BitsAllocated "
                            "and %d SamplesPerPixel" % (bits, samples))

        # PIL size = (width, height)
        size = (dataset.Columns, dataset.Rows)

        # Recommended to specify all details
        # by http://www.pythonware.com/library/pil/handbook/image.htm
        im = PIL.Image.frombuffer(mode, size, dataset.PixelData,
                                  "raw", mode, 0, 1)

    else:
        image = get_LUT_value(dataset.pixel_array, dataset.WindowWidth,
                              dataset.WindowCenter)
        # Convert mode to L since LUT has only 256 values:
        #   http://www.pythonware.com/library/pil/handbook/image.htm
        im = PIL.Image.fromarray(image).convert('L')

    return im


def create_thumbnail(dcm_fn, output_fn, size=(128, 128), output_format=None):
    """Crete a thumbnail from a dicom file"""
    # if no output format is given, extension of file is used to determine
    # format
    if not output_format:
        output_format = output_fn.split(".")[-1].upper()

    dcm = dicom.read_file(dcm_fn)
    im = get_PIL_image(dcm)
    im.thumbnail(size)
    im.save(output_fn, output_format)

def create_thumbnail_mudicom(dcm_fn, output_fn, size=(128, 128), output_format=None):
    if not output_format:
        output_format = output_fn.split(".")[-1].upper()

    mu = mudicom.load(dcm_fn)
    mu.read()
    mu.validate()
    im = pillow.fromarray(mu.image.numpy.astype('uint8'))
    im.thumbnail(size)
    im.save(output_fn, output_format)

def is_compressed(dcm):
    return dcm.file_meta.TransferSyntaxUID not in NotCompressedPixelTransferSyntaxes
