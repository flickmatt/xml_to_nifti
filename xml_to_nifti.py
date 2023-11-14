import xml.etree.ElementTree as ET
import numpy as np
import nibabel as nib

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    coordinates = []

    for element in root.iter():
        if element.text is not None and '\\' in element.text:
            coordinates.append(element.text.split('\\'))

    return coordinates

def create_dicom_map(coordinates, image_shape, biopsy_size):
    dicom_map = np.zeros(image_shape, dtype=np.uint8)

    for coord_set in coordinates:
        x, y, z = map(float, coord_set)
        x, y, z = int(x), int(y), int(z)

        # Set a cube of values around the coordinate
        x_start, x_end = max(0, x - biopsy_size // 2), min(image_shape[0], x + biopsy_size // 2 + 1)
        y_start, y_end = max(0, y - biopsy_size // 2), min(image_shape[1], y + biopsy_size // 2 + 1)
        z_start, z_end = max(0, z - biopsy_size // 2), min(image_shape[2], z + biopsy_size // 2 + 1)

        dicom_map[x_start:x_end, y_start:y_end, z_start:z_end] = 1

    return dicom_map

def save_dicom_map_as_nifti(dicom_map, output_file):
    nifti_image = nib.Nifti1Image(dicom_map, affine=np.eye(4))
    nib.save(nifti_image, output_file)

def main():
    xml_file = '_STEALTH_ROIs_.xml'
    coordinates = parse_xml(xml_file)

    reference_image_path = 'march_9th_94fa1743/26001_GAD_STEALTH_3D_AX_T1_MPRAGE_1MM_C9C1HN021/26001_GAD_STEALTH_3D_AX_T1_MPRAGE_1MM_C9C1HN021.nii'
    reference_image = nib.load(reference_image_path)
    image_shape = reference_image.shape

    # Set the size of each biopsy location (3x3x3 in this case)
    biopsy_size = 3

    dicom_map = create_dicom_map(coordinates, image_shape, biopsy_size)

    output_file = '_STEALTH_ROIs_.nii.gz'
    save_dicom_map_as_nifti(dicom_map, output_file)

if __name__ == "__main__":
    main()
