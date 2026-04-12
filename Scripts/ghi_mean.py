
import numpy as np
import rasterio

input_raster = r"C:\Users\Ferryadmin\miniforge3\Projects\Solar_Suitability_PTL\Processed Data\GHI_7_CLEANFINALCLIP328.tif"
output_raster = r"C:\Users\Ferryadmin\miniforge3\Projects\Solar_Suitability_PTL\Processed Data\GHI_7_MEAN.tif"

nodata_value = 255

with rasterio.open(input_raster) as src:
    data = src.read().astype("float32")   # (bands, rows, cols)

    print("Band count:", src.count)
    print("Shape:", data.shape)
    print("Using nodata value:", nodata_value)

    data[data == nodata_value] = np.nan

    mean_ghi = np.nanmean(data, axis=0)

    profile = src.profile.copy()
    profile.update(
        count=1,
        dtype="float32",
        nodata=nodata_value
    )

    output_array = np.where(np.isnan(mean_ghi), nodata_value, mean_ghi).astype("float32")

    with rasterio.open(output_raster, "w", **profile) as dst:
        dst.write(output_array, 1)

print("Done. Mean raster saved to:")
print(output_raster)
