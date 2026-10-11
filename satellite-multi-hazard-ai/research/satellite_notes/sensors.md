# Satellite and Environmental Sensor Research Notes

## 1. Purpose

This document records the technical information gathered from
official satellite and environmental-data documentation relevant to
the Satellite-Based Multi-Hazard Intelligence System.

The purpose is not simply to describe satellites.

The purpose is to understand:

- What each sensor actually measures.
- How the observation is produced.
- What type of information it provides.
- What spatial and temporal characteristics it has.
- Which hazards it is suitable for.
- What advantages it provides.
- What limitations must be considered.
- How different observations can complement each other.
- Which observations may be useful for future experiments.

The information in this document is based primarily on official
documentation from the European Space Agency (ESA) and NASA.

---

# 2. Why Multiple Satellite Observations Are Needed

Earth-observation satellites do not all observe the Earth in the same
way.

Different sensors measure different physical characteristics.

For example:

- SAR measures the interaction of radar signals with the Earth's
  surface.
- Optical sensors measure reflected sunlight across different
  wavelengths.
- Thermal observations detect information related to surface
  temperature and heat anomalies.
- Precipitation products estimate rainfall.
- Digital Elevation Models provide terrain information.

Therefore, two satellites observing the same geographic location can
provide different information.

This is important for our project because a single observation may not
always provide enough information to correctly interpret an
environmental event.

The research question is therefore not simply:

> Which satellite is the best?

Instead, we investigate:

> Can complementary observations provide additional information that
> reduces missed detections or false alarms under particular
> conditions?

This must be tested experimentally.

---

# 3. Sentinel-1

## 3.1 What Is Sentinel-1?

Sentinel-1 is a Copernicus Earth-observation mission operated within
the European Union's Copernicus programme.

The mission uses Synthetic Aperture Radar (SAR).

Unlike passive optical sensors, Sentinel-1 actively transmits radar
signals toward the Earth's surface and measures the returned signal.

The Sentinel-1 radar operates in the C-band.

### Official source

European Space Agency (ESA):

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/Introducing_the_Sentinel-1_mission

---

## 3.2 What Is SAR?

Synthetic Aperture Radar is an active remote-sensing technique.

A radar instrument transmits electromagnetic energy toward the Earth
and records the signal that is scattered back toward the sensor.

The returned signal depends on characteristics of the observed
surface, including properties related to:

- Surface roughness
- Geometry
- Moisture
- Vegetation structure
- Orientation
- Radar wavelength
- Observation angle

Therefore, SAR imagery is fundamentally different from a normal
photograph.

The brightness of a SAR pixel does not directly represent visible
colour.

Instead, it represents information related to the radar backscatter
received from the surface.

---

## 3.3 Why Sentinel-1 Is Important

ESA describes Sentinel-1 as providing all-weather, day-and-night
imagery.

This is important because optical satellite imagery depends strongly
on reflected sunlight and can be affected by cloud cover.

Therefore, Sentinel-1 can provide observations in situations where
optical imagery may be unavailable or unsuitable.

This makes Sentinel-1 particularly relevant to:

- Flood mapping
- Disaster monitoring
- Forest monitoring
- Surface-change detection

### Research interpretation

For our project, Sentinel-1 should be considered a complementary
observation source rather than automatically assuming it is superior
to optical imagery.

---

## 3.4 Sentinel-1 and Floods

Water surfaces can produce radar responses that differ from
surrounding land surfaces.

Under suitable conditions, this difference can be used to identify
flooded areas in SAR imagery.

This is one reason Sentinel-1 has become important for satellite-based
flood mapping.

Operational systems such as Copernicus Global Flood Monitoring use
Sentinel-1 SAR observations for flood monitoring.

### Research question

Instead of asking:

> Can Sentinel-1 detect floods?

which is already well established, our research should investigate:

> Under which environmental and observational conditions does
> Sentinel-1 flood detection become difficult or ambiguous?

Potential factors include:

- Urban areas
- Vegetation
- Complex terrain
- Permanent water
- Soil moisture
- Radar geometry
- Surface roughness

These conditions should be investigated using actual events and
reference data.

---

## 3.5 Sentinel-1 and Forests

Radar interacts with vegetation structure.

Therefore, changes in forest structure can sometimes produce changes in
SAR observations.

Sentinel-1 can also provide observations when optical imagery is
limited by clouds.

This makes Sentinel-1 useful for forest disturbance monitoring.

However, radar observations can also be affected by:

- Vegetation structure
- Soil conditions
- Moisture
- Terrain
- Observation geometry

Therefore, a change in radar response should not automatically be
interpreted as deforestation.

### Research implication

The project should distinguish between:

- Detecting a surface/forest disturbance.
- Determining the cause of that disturbance.

The second problem may require additional evidence.

---

## 3.6 Sentinel-1 Limitations

Important limitations to consider include:

- SAR interpretation is more complex than visual imagery.
- Radar backscatter depends on multiple physical factors.
- Speckle noise can affect SAR imagery.
- Terrain and observation geometry can influence measurements.
- Some land-cover types can produce ambiguous radar responses.
- A radar change does not automatically identify the cause of change.

Therefore, preprocessing and contextual information may be important.

---

# 4. Sentinel-2

## 4.1 What Is Sentinel-2?

Sentinel-2 is a Copernicus multispectral optical Earth-observation
mission.

The Sentinel-2 instrument is a Multispectral Imager (MSI).

ESA documentation states that the instrument contains 13 spectral bands
covering wavelengths from approximately 443 nm to 2190 nm.

The bands have spatial resolutions of:

- 10 m
- 20 m
- 60 m

depending on the spectral band.

### Official source

European Space Agency:

https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Facts_and_figures

---

## 4.2 What Does Multispectral Mean?

A normal visible image records a limited number of colour channels.

A multispectral sensor records information in several wavelength
ranges.

Sentinel-2 includes:

- Visible bands
- Near-infrared bands
- Red-edge bands
- Shortwave-infrared bands
- Atmospheric-correction bands

Different materials reflect electromagnetic radiation differently at
different wavelengths.

Therefore, spectral information can help distinguish:

- Vegetation
- Water
- Bare soil
- Burned areas
- Different land-cover types

---

## 4.3 Sentinel-2 and Forest Monitoring

Sentinel-2 is particularly useful for vegetation monitoring.

Changes in vegetation can produce changes in spectral measurements.

This allows Sentinel-2 data to be used for:

- Vegetation indices
- Forest monitoring
- Land-cover classification
- Forest disturbance detection
- Vegetation-health analysis

### Research implication

Sentinel-2 can provide detailed spectral information for forest
disturbance analysis.

However, cloud cover can reduce the availability of useful optical
observations.

This is one reason SAR can potentially provide complementary
information.

---

## 4.4 Sentinel-2 and Floods

Sentinel-2 can also be used for water and land-cover analysis.

In clear conditions, optical imagery can provide useful visual and
spectral information about water bodies and surrounding land.

However, cloud cover can obscure the surface.

Therefore, Sentinel-2 should not automatically be treated as a
replacement for Sentinel-1 in flood monitoring.

A useful research question is:

> When does optical information provide useful additional information
> beyond SAR?

---

## 4.5 Sentinel-2 and Wildfires

Sentinel-2 can be useful for post-fire analysis because burned
vegetation can produce spectral changes.

Potential applications include:

- Burned-area mapping
- Vegetation damage assessment
- Post-fire land-cover analysis

This is different from active-fire detection.

Sentinel-2 should therefore mainly be considered as a potential
supporting observation for post-fire assessment rather than treating
it as the same type of data as VIIRS active-fire detections.

---

## 4.6 Sentinel-2 Limitations

Important limitations include:

- Cloud cover
- Atmospheric effects
- Dependence on sunlight
- Possible shadows
- Different spatial resolutions among bands
- Temporal gaps caused by unusable observations

Therefore, optical data quality must be considered during experiment
design.

---

# 5. Sentinel-1 and Sentinel-2 Together

Sentinel-1 and Sentinel-2 observe the Earth differently.

| Characteristic | Sentinel-1 | Sentinel-2 |
|---|---|---|
| Observation type | SAR | Multispectral optical |
| Active/passive | Active | Passive |
| Main information | Radar backscatter | Spectral reflectance |
| Day/night | Yes | Daylight |
| Cloud sensitivity | Much less affected by clouds | Strongly affected by clouds |
| Major applications | Floods, surface change, forests | Vegetation, forests, land cover, water |
| Main challenge | SAR interpretation and speckle | Clouds and atmospheric effects |

The important research idea is therefore not:

> Sentinel-1 is better than Sentinel-2.

Instead:

> Sentinel-1 and Sentinel-2 provide different and potentially
> complementary information.

Previous forest-disturbance research has already investigated
combining Landsat, Sentinel-2 and Sentinel-1.

Therefore, sensor fusion itself cannot be claimed as novel.

Our experiments must identify a specific condition where additional
information provides measurable value.

---

# 6. VIIRS

## 6.1 What Is VIIRS?

VIIRS stands for:

Visible Infrared Imaging Radiometer Suite.

It is an instrument used on satellites including Suomi NPP and
NOAA-20/21.

NASA FIRMS provides VIIRS active-fire and thermal-anomaly products.

### Official source

NASA FIRMS:

https://firms.modaps.eosdis.nasa.gov/

---

## 6.2 VIIRS Active-Fire Detection

VIIRS active-fire products identify locations associated with
thermal anomalies.

NASA FIRMS provides VIIRS active-fire data at approximately 375 m
spatial resolution.

The data can be used to study the spatial and temporal distribution
of active-fire detections.

FIRMS provides information such as:

- Detection location
- Detection time
- Detection confidence
- Fire Radiative Power
- Pixel information

---

## 6.3 What Does a VIIRS Fire Detection Mean?

A critical point from NASA FIRMS documentation is that a satellite
thermal anomaly does not automatically mean that the entire detected
pixel is burning.

A detection may correspond to:

- A small intense fire.
- A larger fire covering part of a pixel.
- Hot smoke.
- Agricultural activity.
- Other hot sources.

NASA also notes that cloud cover can obscure active-fire detections.

Therefore, a VIIRS detection should be treated as satellite-derived
evidence rather than perfect ground truth.

### Research importance

This creates a measurable research problem:

> Can additional contextual information help distinguish actual
> wildfire activity from other thermal anomalies?

---

## 6.4 VIIRS Advantages

Potential advantages include:

- Large-area coverage
- Active-fire monitoring
- Day/night fire observations
- Approximately 375 m spatial resolution
- Availability through NASA FIRMS
- Long historical coverage

NASA documentation states that VIIRS 375 m products are available
for S-NPP from January 2012 onward and for NOAA-20 and NOAA-21 from
later dates.

---

## 6.5 VIIRS Limitations

Important limitations include:

- Spatial resolution is much coarser than Sentinel-2.
- Small fires can be difficult to characterize.
- Thermal anomalies are not always actual wildfires.
- Cloud cover can hide fire detections.
- Detection depends on observation geometry and confidence.
- A detected pixel is not necessarily completely burned.

These limitations are directly relevant to our wildfire research.

---

# 7. MODIS

## 7.1 What Is MODIS?

MODIS stands for:

Moderate Resolution Imaging Spectroradiometer.

MODIS has been used extensively for Earth-observation applications
including active-fire monitoring.

NASA FIRMS provides MODIS active-fire products.

MODIS active-fire products have approximately 1 km spatial
resolution.

---

## 7.2 MODIS Compared with VIIRS

| Characteristic | MODIS | VIIRS |
|---|---|---|
| Active-fire monitoring | Yes | Yes |
| Approximate fire-pixel resolution | 1 km | 375 m |
| Historical availability | Very long | From 2012 for S-NPP |
| Main use | Large-scale fire monitoring | Improved spatial detail for fire detection |
| Provider | NASA | NASA |

NASA FIRMS currently provides MODIS Collection 6.1 and VIIRS 375 m
active-fire products.

### Research implication

VIIRS may provide finer spatial information than MODIS for active-fire
analysis, but this does not mean every detection is automatically
correct.

Both products require careful interpretation.

---

# 8. NASA FIRMS

## 8.1 What Is FIRMS?

FIRMS stands for:

Fire Information for Resource Management System.

NASA FIRMS provides access to satellite-derived active-fire and
thermal-anomaly information.

Available products include observations from:

- MODIS
- VIIRS
- Landsat

### Official source

https://firms.modaps.eosdis.nasa.gov/

---

## 8.2 FIRMS Data Availability

NASA provides active-fire data in formats including:

- CSV
- Shapefile
- KML/KMZ
- Web services

NASA also provides archive access for older observations.

For scientific analysis, NASA advises users to use standard
science-quality data rather than relying only on near-real-time
products.

### Research implication

When we eventually download wildfire data, we must document:

- Product type
- Collection/version
- Date
- Satellite
- Processing level
- Geographic area

This is important for reproducibility.

---

# 9. GPM IMERG

## 9.1 What Is GPM?

GPM stands for:

Global Precipitation Measurement.

NASA's GPM mission provides precipitation observations and
precipitation products.

One important product is:

Integrated Multi-satellitE Retrievals for GPM (IMERG).

---

## 9.2 IMERG Resolution

NASA documentation states that common GPM IMERG products have:

- 0.1° × 0.1° spatial resolution
- Approximately 10 km × 10 km grid spacing
- 30-minute temporal resolution

### Official source

NASA GPM:

https://gpm.nasa.gov/data/imerg

---

## 9.3 Why Rainfall Matters to Our Flood Research

Rainfall is not a direct measurement of flood extent.

Instead, rainfall provides environmental context.

For example:

```text
Heavy rainfall
      ↓
Increased water input
      ↓
Potential runoff / river response
      ↓
Possible inundation
      ↓
Satellite observation of actual surface conditions