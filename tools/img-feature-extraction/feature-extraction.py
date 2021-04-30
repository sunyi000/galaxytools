#!/usr/bin/env python
from skimage.io import imread
from skimage import util,measure
from skimage.segmentation import clear_border
import numpy as np
import pandas as pd

def get_properties(regionprops):
    for prop in regionprops[0]:
        try:
            regionprops[0][prop]
            supported.append(prop)
        except NotImplementedError:
            unsupported.append(prop)
    return supported,unsupported


def extract_features(org_data,lbl_data):
    supported=[]
    unsupported=[]

    regionprops = measure.regionprops(lbl_data,intensity_image=org_data)

    input_vals=[]
    output_vals=[]

    for r in regionprops:
    msg = ""
    input_vals.append(r.label)
    if 1 in r.image.shape:
        print(f"object with label {r.label} has singleton dimension and cannot support convex hull in 3d")
        output_vals.append(0)
    else:
        output_vals.append(r.label)

    lbl_data = util.map_array(lbl_data, input_vals=np.array(input_vals), output_vals=np.array(output_vals))

    supported,unsupported = get_properties(regionprops)

    features = measure.regionprops_table(lbl_data,org_data,properties=supported)

    data=pd.DataFrame(features)

    data.to_csv('features.csv',index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--org_img',
        help='Original image'
    )
    parser.add_argument(
        '-l', '--labelled_img',
        help='Labelled image'
    )
    args = parser.parse_args()

    lbl_data = np.asarray(args.labelled_img)
    org_data = np.asarray(args.org_img)

    lbl_data=clear_border(lbl_data)
    
    extract_features(org_data,lbl_data)
