## Raster Calculator Formulas Used

### 1. Standardized raster inputs

The following rasters were normalized to a common **0–1 scale** before building the weighted overlay model:

- `GHI_MEAN_STANDARD330`
- `POP_STANDARD330`
- `SLOPE_STANDARD330`

#### Standard min-max normalization
Used for:
- `GHI_MEAN_STANDARD330`
- `POP_STANDARD330`

Formula structure:

```text
("input_raster@1" - min) / (max - min)

This transformation assigns values closer to 1 to higher raw values and values closer to 0 to lower raw values.

Inverted min-max normalization

Used for:

SLOPE_STANDARD330

Formula structure:

(max - "input_raster@1") / (max - min)

This transformation assigns values closer to 1 to lower slope values, meaning flatter terrain is treated as more suitable.

2. Weighted overlay model

The base suitability model was created by combining the normalized rasters with the following weights:

Solar irradiance (GHI_MEAN_STANDARD330) = 0.5
Population (POP_STANDARD330) = 0.3
Slope (SLOPE_STANDARD330) = 0.2

Raster Calculator formula:

("GHI_MEAN_STANDARD330@1" * 0.5) + ("POP_STANDARD330@1" * 0.3) + ("SLOPE_STANDARD330@1" * 0.2)

This produced the base solar suitability raster used in the project.

3. Distance-to-grid rasters

The following rasters were generated from the rasterized infrastructure layers using the Proximity tool:

grid_distance46
Substations_distance46

These rasters store the distance from each pixel to the nearest relevant infrastructure feature.

4. Grid-constrained suitability filter

The focused suitability output was created by retaining only pixels that met both of the following conditions:

within 10 km of a substation
within 20 km of grid infrastructure

Raster Calculator formula used to generate Focused_Overlay46:

(("Substations_distance46@1"<=10000)*("grid_distance46@1"<=20000)*("OVERLAY_MODEL331@1">0))*"OVERLAY_MODEL331@1"

This formula keeps the original overlay model value only where:

Substations_distance46 is less than or equal to 10,000 meters
grid_distance46 is less than or equal to 20,000 meters
the overlay model value is greater than 0

All cells that do not meet these criteria are set to 0.